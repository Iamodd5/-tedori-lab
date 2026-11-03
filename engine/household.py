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
    """Part-timers need 88,000 a month all year: the wage test to September 2026, then 特定減額特例 (social_insurance.yaml)."""
    if m.get("salary", 0) <= 0:
        return False
    w = m.get("work", {})
    if w.get("full_time"):
        return True
    sc = b.params("social_insurance")["part_time_coverage"]
    return (w.get("hours_20_plus", False) and w.get("employer_51_plus", False) and not m.get("student", False)
            and m["salary"] / 12 >= sc["monthly_wage_min"]["value"])


def _employment_insured(m):
    """雇用保険法6条: 20+ hours a week and not a student; no pay condition and no employer-size condition."""
    w = m.get("work", {})
    return m.get("salary", 0) > 0 and (w.get("full_time") or w.get("hours_20_plus", False)) and not m.get("student", False)


def _nhi_earner(m):
    """給与所得者等 in the NHI reduction test (国保令29条の7第6項第1号, 附則5条)."""
    e = b.params("social_insurance")["nhi_shinjuku_fy2026"]["flat_reduction"]["earner"]
    if m.get("salary", 0) > e["salary_over"]["value"]:
        return True
    if b.employment_income(m.get("salary", 0)) > 0:  # people with salary income are not counted for their pension
        return False
    limit = e["pension_over_65_plus"] if m["age"] >= e["pension_over_65_plus"]["age_from"] else e["pension_over_under_65"]
    return m.get("public_pension", 0) > limit["value"]


def _dependant_limit(m):
    d = b.params("social_insurance")["health_dependant_income_limit"]
    if m["age"] >= d["age_60_plus"]["age_from"]:
        return d["age_60_plus"]["value"]
    s = d["age_19_to_22_not_spouse"]
    if s["age_from"] <= m["age"] < s["age_under"] and m["role"] != "spouse":
        return d["age_19_to_22_not_spouse"]["value"]
    return d["general"]["value"]


def _insurance(members, out):
    """Scheme and 12-month contributions of each member."""
    covered = {m["id"]: _employee_covered(m) for m in members}
    partners = [m for m in members if m["role"] in ("head", "spouse")]
    other_partner_covered = lambda m: any(covered[p["id"]] for p in partners if p is not m)
    np_month = b.params("social_insurance")["national_pension_monthly"]["value"]
    ages = b.params("social_insurance")["national_pension_ages"]
    res, nhi_members, householder = {}, [], None
    for m in members:
        o = out[m["id"]]
        if covered[m["id"]]:
            scheme = "employee"
        elif (m.get("outside_health_dependant") or other_partner_covered(m)) and _gross(m) < _dependant_limit(m):
            scheme = "dependant"
        else:
            scheme = "nhi"
        prem = b.employee_premiums(m["salary"], m["age"]) if scheme == "employee" or _employment_insured(m) else {}
        if scheme != "employee":
            prem = {"employment": prem.get("employment", 0)}  # employment insurance has no pay condition (雇用保険法6条)
        r = res[m["id"]] = {"scheme": scheme, **{k: prem.get(k, 0) for k in ("health", "child_levy", "pension", "employment")}, "nhi": 0}
        spouse_of_employee = m in partners and other_partner_covered(m)  # category-3 pension member if a dependant
        r["national_pension"] = 0
        if scheme != "employee" and ages["from"]["value"] <= m["age"] < ages["to_exclusive"]["value"] and not (scheme == "dependant" and spouse_of_employee):
            r["national_pension"] = 0 if m.get("student_pension_deferral") else 12 * np_month
        tested = {"age": m["age"], "total_income": o["total_income"], "pension_income": o["pension_income"], "has_earnings": _nhi_earner(m)}
        if scheme == "nhi":
            nhi_members.append(tested)
        elif m["role"] == "head":
            householder = tested
    head = next(m for m in members if m["role"] == "head")
    res[head["id"]]["nhi"] = b.nhi_household(nhi_members, householder)  # the householder pays the household's NHI
    return res


def compute(hh, basic_deduction_it=b.basic_deduction_it, it_credit=0):
    """basic_deduction_it and it_credit (income-tax credit per person) let a reform change those two rules."""
    members = hh["members"]
    it, rt = b.params("income_tax"), b.params("resident_tax")
    out = {m["id"]: {"age": m["age"], "role": m["role"], "gross": _gross(m)} for m in members}

    # 1. incomes
    child_under_23 = any(m["role"] == "child" and m["age"] < it["adjustment_deduction"]["dependant_age_under"]["value"] for m in members)
    for m in members:
        o = out[m["id"]]
        emp = b.employment_income(m.get("salary", 0))
        o["adjustment_deduction"] = min(emp, b.adjustment_deduction(m.get("salary", 0), child_under_23))
        o["pension_income"] = b.pension_income(m.get("public_pension", 0), m["age"])
        o["total_income"] = emp - o["adjustment_deduction"] + m.get("business_income", 0) + o["pension_income"]

    # 2. insurance scheme and contributions
    for mid, x in _insurance(members, out).items():
        out[mid].update(x)
        o = out[mid]
        o["social_insurance"] = o["health"] + o["child_levy"] + o["pension"] + o["employment"] + o["national_pension"] + o["nhi"]
    partners = [m for m in members if m["role"] in ("head", "spouse")]
    head = next(m for m in members if m["role"] == "head")

    # 3. taxes: the higher-earning partner claims the other partner and the dependants (approximation, Q23)
    claimant = max(partners, key=lambda p: out[p["id"]]["total_income"])
    spouse = next((p for p in partners if p is not claimant), None)
    deps = [m for m in members if m["role"] in ("child", "dependant")]
    single_parent = spouse is None and any(out[d["id"]]["total_income"] <= it["dependent_deduction"]["income_limit"]["value"] for d in deps if d["role"] == "child") and head.get("single_parent", False)
    rp = rt["personal_deductions"]
    diff_p = rt["personal_deduction_difference"]
    dd = it["dependent_deduction"]
    specific_it = lambda age: dd["specific_age_from"]["value"] <= age < dd["specific_age_under"]["value"]
    specific_rt = lambda age: rp["dependent_specific_age_from"]["value"] <= age < rp["dependent_specific_age_under"]["value"]
    full_spouse_rt = rp["spouse_earner_full_limit"]["value"]
    for m in members:
        o = out[m["id"]]
        ti = o["total_income"]
        is_claimant = m is claimant
        # income tax. The claimant also deducts the other partner's national pension (HUMAN_TODO H-13, 所得税法74条)
        own_si = o["social_insurance"] - (o["national_pension"] if spouse is m else 0)
        if is_claimant and spouse is not None:
            own_si += out[spouse["id"]]["national_pension"]
        ded = basic_deduction_it(ti) + own_si
        r_ded = b.basic_deduction_rt(ti) + own_si
        diff = diff_p["basic"]["value"]
        n_family = 0
        if is_claimant and spouse is not None:
            si = out[spouse["id"]]["total_income"]
            elderly = spouse["age"] >= rp["elderly_spouse_age_from"]["value"]
            ded += b.spouse_deduction_it(ti, si, spouse["age"])
            if ti <= rp["spouse_earner_income_limit"]["value"]:
                if si <= rp["dependant_income_limit"]["value"]:
                    r_ded += rp["elderly_spouse" if elderly else "spouse"]["value"]
                    diff += diff_p["elderly_spouse" if elderly else "spouse"]["value"] if ti <= full_spouse_rt else 0
                    n_family += 1
                else:  # the band table gives 0 above its last row (1,330,000)
                    r_ded += b.band(rp["spouse_special"]["bands"], si) if ti <= full_spouse_rt else 0
        if is_claimant:
            for d in deps:
                di, age = out[d["id"]]["total_income"], d["age"]
                if di <= dd["income_limit"]["value"]:
                    if specific_it(age):
                        ded += dd["specific_19_to_22"]["value"]
                    elif age >= dd["general_age_from"]["value"]:
                        ded += dd["general_16_plus"]["value"]
                elif specific_it(age):
                    ded += b.specific_relative_special_it(di)
                if di <= rp["dependant_income_limit"]["value"]:
                    n_family += 1
                    if specific_rt(age):
                        r_ded += rp["dependent_specific_19_to_22"]["value"]
                        diff += diff_p["dependent_specific"]["value"]
                    elif age >= rp["dependent_general_age_from"]["value"]:
                        r_ded += rp["dependent_general_16_plus"]["value"]
                        diff += diff_p["dependent_general"]["value"]
                elif specific_rt(age):  # no 調整控除 difference for this deduction (地方税法314条の6)
                    r_ded += b.specific_relative_special_rt(di)
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
        o["resident_tax"] = b.resident_tax(ti, r_ded, diff, n_family, single_parent and is_claimant) if _gross(m) > 0 else 0

    child_ages = [m["age"] for m in members if m["role"] == "child" and m["age"] <= b.params("child_allowance")["eligible_age_max"]["value"]]
    allowance = b.child_allowance(child_ages)
    gross = sum(o["gross"] for o in out.values())
    tax = sum(o["income_tax"] + o["resident_tax"] for o in out.values())
    si = sum(o["social_insurance"] for o in out.values())
    return {"members": out, "child_allowance": allowance, "gross": gross, "taxes": tax, "social_insurance": si,
            "disposable": gross + allowance - tax - si}
