"""Policy designs as reforms on top of the 2026 baseline (spec Section 8). Numbers come from parameters/designs/.

run(design, hh) returns the change versus baseline in yen per year. A design with unpublished numbers returns
status "incomplete", the list of missing parameters, and no number (CLAUDE.md rule 2).
"""
import functools
import math
import pathlib

import yaml

from engine import baseline as b
from engine import household as h

D = pathlib.Path(__file__).resolve().parents[1] / "parameters" / "designs"
COMPONENTS = ("income_tax", "resident_tax", "social_insurance", "credit", "consumption_tax")
# Why a design cannot be calculated yet, by open question, so different reasons are never shown as one
BLOCKERS = {"Q9": {"ja": "政府が支給額や収入の線引きをまだ公表していません（後で政令で決める予定）", "en": "the government hasn't yet published the payment amounts and income limits (they will be set later by Cabinet order)"},
            "Q8": {"ja": "例の世帯H1〜H8の食料品の支出額をまだ用意できていません", "en": "we don't yet have food spending figures for the example households H1–H8"},
            "Q3": {"ja": "連合が消費税還付制度の金額をまだ公表していません", "en": "Rengo hasn't published the amounts for its consumption tax refund"}}


@functools.cache
def design(name):
    return yaml.safe_load((D / f"{name}.yaml").read_text(encoding="utf-8"))


def unresolved(params, path=""):
    out = []
    for key, node in params.items():
        p = f"{path}.{key}" if path else key
        if "status" in node:
            out += [f"{p} ({node['question']})"] if node["status"] == "unresolved" else []
        else:
            out += unresolved(node, p)
    return out


def payment(earned, total_income, n_children, p):
    """就業者負担軽減支援金 shape (outline 第三 一 2(1)①②④⑤, pp.8-10). The temporary 就業促進特例加算 (③) is
    not included: its range and amount are unpublished (Q9)."""
    if earned <= p["earned_income_floor"] or total_income > p["income_ceiling"]:
        return 0
    if earned <= p["phase_in_start"]:
        amount = p["flat_amount_low_income"]
    elif earned < p["phase_in_end"]:
        share = (earned - p["phase_in_start"]) / (p["phase_in_end"] - p["phase_in_start"])
        amount = p["flat_amount_low_income"] + share * (p["basic_amount"] - p["flat_amount_low_income"])
    else:
        amount = p["basic_amount"]
    top = p["basic_amount"] + n_children * p["child_addition_per_child"]
    amount += n_children * p["child_addition_per_child"]
    if total_income > p["phase_out_start"]:
        amount = min(amount, max(0, top - p["phase_out_rate"] * (total_income - p["phase_out_start"])))
    return math.ceil(amount / 1000) * 1000


def food_tax_saving(food_spending, pass_through):
    """Food bought at today's 8%-inclusive prices costs 1.01/1.08 as much at 1%, times the share passed to prices."""
    return round(food_spending * (0.08 - 0.01) / 1.08 * pass_through)


def daiwa_credit(employment_income_minimum=None):
    """(target − employment-income minimum − basic deduction) × lowest rate (Daiwa p.5 図表4 注1), on 2026 rules."""
    p = design("daiwa")["parameters"]
    target = p["target_threshold"]["value"]
    if employment_income_minimum is None:
        employment_income_minimum = target - b.employment_income(target)  # the target salary is in the minimum band
    lowest_rate = b.params("income_tax")["rate_schedule"]["bands"][0][1]
    return round((target - employment_income_minimum - p["income_tax_basic_deduction"]["value"]) * lowest_rate)


def _daiwa(hh):
    p = design("daiwa")["parameters"]
    base = h.compute(hh)
    ref = h.compute(hh, basic_deduction_it=lambda ti: p["income_tax_basic_deduction"]["value"],
                    it_credit=daiwa_credit())
    refund = 0
    for mid, o in ref["members"].items():
        m = next(x for x in hh["members"] if x["id"] == mid)
        if o["scheme"] == "employee":
            labour_si = o["health"] + o["pension"]  # child levy and employment insurance not named by Daiwa (Q18)
        elif m.get("salary", 0) + m.get("business_income", 0) > 0:
            # shortcut: household NHI sits with the head (household.py), so only the head's refund can use it
            labour_si = o["national_pension"] + o["nhi"]
        else:
            labour_si = 0
        refund += min(o["unused_credit"], labour_si)
    tax = lambda res, k: sum(o[k] for o in res["members"].values())
    return {"income_tax": tax(ref, "income_tax") - tax(base, "income_tax"),
            "resident_tax": tax(ref, "resident_tax") - tax(base, "resident_tax"),
            "social_insurance": 0, "credit": refund, "consumption_tax": 0}


def run(name, hh):
    d = design(name)
    if name == "daiwa":
        c = _daiwa(hh)
        change = c["credit"] - c["income_tax"] - c["resident_tax"] - c["social_insurance"] - c["consumption_tax"]
        return {"design": name, "status": "complete", "missing": [], "blocked_by": [], "components": c,
                "disposable_change": change, "approximations": d["approximations"], "site_note": d["site_note"]}
    missing = unresolved(d["parameters"])
    if name == "food_tax_cut" and hh["spending"].get("status") == "unresolved":
        missing.append(f"household food spending ({hh['spending']['question']})")
    if not missing:
        raise NotImplementedError(f"{name}: all parameters now published; wire payment() into run()")
    blocked_by = [BLOCKERS[q] for q in BLOCKERS if any(f"({q})" in m for m in missing)]
    return {"design": name, "status": "incomplete", "missing": missing, "blocked_by": blocked_by,
            "components": dict.fromkeys(COMPONENTS), "disposable_change": None, "approximations": [],
            "site_note": d.get("site_note")}
