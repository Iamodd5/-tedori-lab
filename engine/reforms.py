"""Policy designs as reforms on top of the 2026 baseline (spec Section 8). Numbers come from parameters/designs/.

run(design, hh) returns the change versus baseline in yen per year. A design with unpublished numbers returns
status "incomplete", the list of missing parameters, and no number (project rule 2).
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
BLOCKERS = {"Q9": {"ja": "支給額や収入の線引きは、まだ示されていません。法律案では、後で政令（内閣が定める命令）で決めることになっています", "en": "the payment amounts and income limits haven't been set out yet (under the bill, they will be set later by Cabinet order)"},
            "Q3": {"ja": "消費税還付制度の支給額や収入の線引きは、まだ示されていません", "en": "the payment amounts and income limits for the consumption tax refund haven't been set out yet"},
            "Q8": {"ja": "モデル世帯H1〜H8の食料品の支出額を、まだ用意できていません", "en": "we don't yet have food spending figures for the example households H1–H8"}}


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
    # 1,000 yen, rounded up: the same outline rule (第三 一 2(1)⑥) for both plans; food_tax_cut.yaml repeats it
    unit = design("government_final")["parameters"]["rounding"]["value"]
    return math.ceil(amount / unit) * unit


def food_tax_saving(food_spending, pass_through):
    """Food bought at today's 8%-inclusive prices costs 1.01/1.08 as much at 1%, times the share passed to prices."""
    c = design("food_tax_cut")["parameters"]["consumption_tax_cut"]
    now, cut = c["current_combined_rate_on_food"]["value"], c["combined_rate_on_food"]["value"]
    return round(food_spending * (now - cut) / (1 + now) * pass_through)


def daiwa_credit(employment_income_minimum=None):
    """(target − employment-income minimum − basic deduction) × lowest rate (Daiwa p.5 図表4 注1), on 2026 rules."""
    p = design("daiwa")["parameters"]
    target = p["target_threshold"]["value"]
    if employment_income_minimum is None:
        employment_income_minimum = target - b.employment_income(target)  # the target salary is in the minimum band
    lowest_rate = b.params("income_tax")["rate_schedule"]["bands"][0][1]
    return round((target - employment_income_minimum - p["income_tax_basic_deduction"]["value"]) * lowest_rate)


def daiwa_members(hh):
    """Each member's part of the Daiwa result: income-tax change, resident-tax change and cash refund."""
    p = design("daiwa")["parameters"]
    base = h.compute(hh)
    ref = h.compute(hh, basic_deduction_it=lambda ti: p["income_tax_basic_deduction"]["value"],
                    it_credit=daiwa_credit())
    out = {}
    for mid, o in ref["members"].items():
        m = next(x for x in hh["members"] if x["id"] == mid)
        # child levy and employment insurance not named by Daiwa (Q18). Household NHI is billed to the head
        # (household.py), so it counts only toward the head's cap, and only if the head works
        if m.get("salary", 0) + m.get("business_income", 0) <= 0:
            labour_si = 0
        elif o["scheme"] == "employee":
            labour_si = o["health"] + o["pension"] + o["nhi"] + o["ltc_65"]
        else:
            labour_si = o["national_pension"] + o["nhi"] + o["ltc_65"]  # 65+ care premium: 介護（第1号）, daiwa.yaml
        b = base["members"][mid]
        out[mid] = {"income_tax": o["income_tax"] - b["income_tax"], "resident_tax": o["resident_tax"] - b["resident_tax"],
                    "credit": min(o["unused_credit"], labour_si)}
    return out


def _daiwa(hh):
    parts = daiwa_members(hh).values()
    total = lambda k: sum(x[k] for x in parts)
    return {"income_tax": total("income_tax"), "resident_tax": total("resident_tax"),
            "social_insurance": 0, "credit": total("credit"), "consumption_tax": 0}


def run(name, hh):
    d = design(name)
    if name == "daiwa":
        c = _daiwa(hh)
        change = c["credit"] - c["income_tax"] - c["resident_tax"] - c["social_insurance"] - c["consumption_tax"]
        return {"design": name, "status": "complete", "missing": [], "blocked_by": [], "components": c,
                "disposable_change": change, "approximations": d["approximations"], "site_note": d["site_note"]}
    missing = unresolved(d["parameters"])
    if name in ("food_tax_cut", "rengo") and hh["spending"].get("status") == "unresolved":  # both change the tax on food
        missing.append(f"household food spending ({hh['spending']['question']})")
    if not missing:
        raise NotImplementedError(f"{name}: all parameters now published; wire payment() into run()")
    blocked_by = [BLOCKERS[q] for q in BLOCKERS if any(f"({q})" in m for m in missing)]
    return {"design": name, "status": "incomplete", "missing": missing, "blocked_by": blocked_by,
            "components": dict.fromkeys(COMPONENTS), "disposable_change": None, "approximations": [],
            "site_note": d.get("site_note")}


# Custom credit for the design builder (spec 8.5, Milestone 8). The site runs the same formula in site/custom.js;
# tests/test_custom.py checks the two agree. Hand calculation: tests/hand_calcs/custom_credit.md.
def people(hh):
    """Each member as [kind, earnings, pensions], all before tax. kind: k = child the age limit of the child
    allowance or under, p = head or spouse, o = anyone else (adult children, relatives)."""
    kid_age = b.params("child_allowance")["eligible_age_max"]["value"]
    kind = lambda m: "k" if m["role"] == "child" and m["age"] <= kid_age else "p" if m["role"] in ("head", "spouse") else "o"
    return [[kind(m), m.get("salary", 0) + m.get("business_income", 0), m.get("public_pension", 0)] for m in hh["members"]]


def custom_people(ppl, p):
    kids = sum(k == "k" for k, _, _ in ppl)
    claimant = None  # the partner with the higher earnings, the first listed (head) if equal
    for i, (k, earn, _) in enumerate(ppl):
        if k == "p" and (claimant is None or earn > ppl[claimant][1]):
            claimant = i
    total = 0
    for i, (k, earn, pension) in enumerate(ppl):
        if earn <= 0:
            continue
        c = min(p["phase_in_rate"] * earn, p["maximum"]) + (kids * p["child_addition"] if i == claimant else 0)
        c -= p["phase_out_rate"] * max(0, earn + pension - p["plateau_end"])
        total += max(0, math.floor(round(c, 6)))  # round(…, 6): 0.05 × 1,000,000 must not floor to 49,999
    return total


def custom(hh, p):
    return custom_people(people(hh), p)


def custom_population(builder, p):
    """Average credit and share of households receiving one, by income decile, and the total cost (yen a year)."""
    credit = [custom_people(x, p) for x in builder["population"]["rows"]]
    pieces = builder["population"]["pieces"]
    weight = [sum(w for i, d, w in pieces if d == k) for k in range(1, 11)]
    return {"mean": [sum(credit[i] * w for i, d, w in pieces if d == k) / weight[k - 1] for k in range(1, 11)],
            "share": [sum(w for i, d, w in pieces if d == k and credit[i] > 0) / weight[k - 1] for k in range(1, 11)],
            "cost": sum(credit[i] * w for i, _, w in pieces)}
