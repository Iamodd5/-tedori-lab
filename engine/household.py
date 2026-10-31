"""Combine the baseline rules for one household (households/*.yaml) into disposable income."""
import pathlib

import yaml

from engine import baseline as b

HOUSEHOLDS = pathlib.Path(__file__).resolve().parents[1] / "households"


def load(hid):
    return yaml.safe_load((HOUSEHOLDS / f"{hid}.yaml").read_text(encoding="utf-8"))


def _gross(m):
    return m.get("salary", 0) + m.get("business_income", 0) + m.get("public_pension", 0)


def _employee_covered(m):
    if m.get("salary", 0) <= 0:
        return False
    w = m.get("work", {})
    if w.get("full_time"):
        return True
    sc = b.params("social_insurance")["part_time_coverage"]
    return (w.get("hours_20_plus", False) and w.get("employer_51_plus", False) and not m.get("student", False)
            and m["salary"] / 12 >= sc["monthly_wage_min"]["value"])


def _dependant_limit(m):
    d = b.params("social_insurance")["health_dependant_income_limit"]
    if m["age"] >= 60:
        return d["age_60_plus"]["value"]
    if 19 <= m["age"] <= 22 and m["role"] != "spouse":
        return d["age_19_to_22_not_spouse"]["value"]
    return d["general"]["value"]


def compute(hh, basic_deduction_it=b.basic_deduction_it, it_credit=0):
    """basic_deduction_it and it_credit (income-tax credit per person) let a reform change those two rules."""
    members = hh["members"]
    it, rt = b.params("income_tax"), b.params("resident_tax")
    out = {m["id"]: {"age": m["age"], "role": m["role"], "gross": _gross(m)} for m in members}

    # 1. who is in which insurance scheme
    covered = {m["id"]: _employee_covered(m) for m in members}
    employee_in_household = any(covered[m["id"]] for m in members if m["role"] in ("head", "spouse"))
    for m in members:
        o = out[m["id"]]
        if covered[m["id"]]:
            o["scheme"] = "employee"
        elif (m.get("outside_health_dependant") or (employee_in_household and m["role"] != "head")) and _gross(m) < _dependant_limit(m):
            o["scheme"] = "dependant"
        else:
            o["scheme"] = "nhi"

    # 2. incomes
    child_under_23 = any(m["role"] == "child" and m["age"] < 23 for m in members)
    for m in members:
        o = out[m["id"]]
        emp = b.employment_income(m.get("salary", 0))
        o["adjustment_deduction"] = min(emp, b.adjustment_deduction(m.get("salary", 0), child_under_23))
        o["pension_income"] = b.pension_income(m.get("public_pension", 0), m["age"])
        o["total_income"] = emp - o["adjustment_deduction"] + m.get("business_income", 0) + o["pension_income"]

    # 3. contributions
    np_month = b.params("social_insurance")["national_pension_monthly"]["value"]
    nhi_members = []
    for m in members:
        o = out[m["id"]]
        prem = b.employee_premiums(m["salary"], m["age"]) if o["scheme"] == "employee" else {}
        o.update({k: prem.get(k, 0) for k in ("health", "child_levy", "pension", "employment")})
        spouse_of_employee = m["role"] == "spouse" and any(covered[x["id"]] for x in members if x["role"] == "head")
        o["national_pension"] = 0
        if o["scheme"] != "employee" and 20 <= m["age"] < 60 and not (o["scheme"] == "dependant" and spouse_of_employee):
            o["national_pension"] = 0 if m.get("student_pension_deferral") else 12 * np_month
        if o["scheme"] == "nhi":
            nhi_members.append({"age": m["age"], "total_income": o["total_income"], "pension_income": o["pension_income"],
                                "has_earnings": _gross(m) > 0})
        o["nhi"] = 0
    head = next(m for m in members if m["role"] == "head")
    out[head["id"]]["nhi"] = b.nhi_household(nhi_members)  # the householder pays the household's NHI
    for o in out.values():
        o["social_insurance"] = o["health"] + o["child_levy"] + o["pension"] + o["employment"] + o["national_pension"] + o["nhi"]

    # 4. taxes (dependants are claimed by the head; spouse deduction by the head)
    spouse = next((m for m in members if m["role"] == "spouse"), None)
    deps = [m for m in members if m["role"] in ("child", "dependant")]
    single_parent = spouse is None and any(out[d["id"]]["total_income"] <= it["dependent_deduction"]["income_limit"]["value"] for d in deps if d["role"] == "child") and head.get("single_parent", False)
    rp = rt["personal_deductions"]
    diff_p = rt["personal_deduction_difference"]
    for m in members:
        o = out[m["id"]]
        ti = o["total_income"]
        is_head = m is head
        # income tax
        ded = basic_deduction_it(ti) + o["social_insurance"]
        r_ded = b.basic_deduction_rt(ti) + o["social_insurance"]
        diff = diff_p["basic"]["value"]
        n_family = 0
        if is_head and spouse is not None:
            si = out[spouse["id"]]["total_income"]
            ded += b.spouse_deduction_it(ti, si)
            if ti <= 10_000_000:
                if si <= rp["dependant_income_limit"]["value"]:
                    r_ded += rp["spouse"]["value"]
                    diff += diff_p["spouse"]["value"] if ti <= 9_000_000 else 0
                    n_family += 1
                elif si <= 1_330_000:
                    r_ded += b.band(rp["spouse_special"]["bands"], si) if ti <= 9_000_000 else 0
        if is_head:
            for d in deps:
                di, age = out[d["id"]]["total_income"], d["age"]
                if di <= it["dependent_deduction"]["income_limit"]["value"]:
                    if 19 <= age <= 22:
                        ded += it["dependent_deduction"]["specific_19_to_22"]["value"]
                    elif age >= 16:
                        ded += it["dependent_deduction"]["general_16_plus"]["value"]
                elif 19 <= age <= 22:
                    ded += b.specific_relative_special_it(di)
                if di <= rp["dependant_income_limit"]["value"]:
                    n_family += 1
                    if 19 <= age <= 22:
                        r_ded += rp["dependent_specific_19_to_22"]["value"]
                        diff += diff_p["dependent_specific"]["value"]
                    elif age >= 16:
                        r_ded += rp["dependent_general_16_plus"]["value"]
                        diff += diff_p["dependent_general"]["value"]
            if single_parent and ti <= it["single_parent_deduction"]["income_limit"]["value"]:
                ded += it["single_parent_deduction"]["amount"]["value"]
                r_ded += rp["single_parent"]["value"]
                diff += diff_p["single_parent_mother"]["value"]  # H5 is a mother (households/H5.yaml)
        if m.get("student") and m.get("salary", 0) > 0:
            if ti <= it["working_student_deduction"]["income_limit"]["value"]:
                ded += it["working_student_deduction"]["amount"]["value"]
            if ti <= rp["working_student_income_limit"]["value"]:
                r_ded += rp["working_student"]["value"]
                diff += diff_p["working_student"]["value"]
        files = m["role"] != "child" or ti > 0
        o["income_tax"] = b.income_tax(ti, ded, it_credit) if files else 0
        o["unused_credit"] = max(0, it_credit - b.income_tax_before_surtax(ti, ded)) if files else 0
        o["resident_tax"] = b.resident_tax(ti, r_ded, diff, n_family, single_parent and is_head) if _gross(m) > 0 else 0

    child_ages = [m["age"] for m in members if m["role"] == "child" and m["age"] <= 18]
    allowance = b.child_allowance(child_ages)
    gross = sum(o["gross"] for o in out.values())
    tax = sum(o["income_tax"] + o["resident_tax"] for o in out.values())
    si = sum(o["social_insurance"] for o in out.values())
    return {"members": out, "child_allowance": allowance, "gross": gross, "taxes": tax, "social_insurance": si,
            "disposable": gross + allowance - tax - si}
