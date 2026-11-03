"""2026 baseline: income tax, resident tax (Shinjuku), social insurance and child allowance for one household.

All amounts are annual yen for calendar-year 2026 income. Every number comes from parameters/baseline_2026/.
Each function is one rule so it can be tested alone and offered to OpenFisca-Japan as a formula.
"""
import bisect
import csv
import functools
import math
import pathlib

import yaml

P = pathlib.Path(__file__).resolve().parents[1] / "parameters" / "baseline_2026"


@functools.cache
def params(name):
    return yaml.safe_load((P / f"{name}.yaml").read_text(encoding="utf-8"))


@functools.cache
def _csv(name):
    with open(P / name, newline="") as f:
        return [{k: (float(v) if v not in ("", None) else None) for k, v in r.items()} for r in csv.DictReader(f)]


def floor_to(x, unit):
    return math.floor(x / unit) * unit


def half_round(x):
    """協会けんぽ 注①: employee half, 0.50 yen or less rounds down, more rounds up."""
    frac = x - math.floor(x)
    return math.floor(x) + (1 if frac > 0.5 else 0)


def band(bands, x, above=0):
    """bands = [[upper_inclusive, value], ...] sorted; returns value of first band with x <= upper."""
    for upper, value in bands:
        if x <= upper:
            return value
    return above


# ---------- income ----------

def employment_income(salary):
    """給与所得控除後の給与等の金額 (令和8年分)."""
    e = params("income_tax")["employment_income"]
    if salary < e["zero_below"]["value"]:
        return 0
    if salary < e["table_from"]["value"]:
        return salary - e["minimum_deduction"]["value"]
    formula = e["deduction_from_6_6m"]
    if salary < formula[0]["from"]:
        rows = _csv(e["table"]["value"])
        i = bisect.bisect_right([r["salary_from"] for r in rows], salary) - 1
        return int(rows[i]["employment_income"])
    row = [r for r in formula if salary >= r["from"]][-1]
    deduction = row["fixed"] if "fixed" in row else salary * row["rate"] + row["add"]
    return math.floor(salary - deduction)


def adjustment_deduction(salary, has_dependant_under_23):
    """所得金額調整控除 (No.1411)."""
    p = params("income_tax")["adjustment_deduction"]
    if salary <= p["salary_floor"]["value"] or not has_dependant_under_23:
        return 0
    return math.ceil((min(salary, p["salary_cap"]["value"]) - p["salary_floor"]["value"]) * p["rate"]["value"])


def pension_income(pension, age):
    """公的年金等に係る雑所得, age 65+ with other income ≤ 10m (No.1600 図1)."""
    if pension <= 0:
        return 0
    p = params("income_tax")["public_pension_income"]
    assert age >= p["age65_plus_age_from"]["value"], "only the 65+ table is in parameters (households H1-H8 need no other)"
    rows = p["age65_plus"]
    row = [r for r in rows if pension >= r["from"]][-1]
    return max(0, math.floor(pension * row["rate"] - row["minus"]))


# ---------- social insurance ----------

def _grade(table, monthly):
    for r in table:
        if r["to_exclusive"] is None or monthly < r["to_exclusive"]:
            return r
    return table[-1]


def employee_premiums(salary, age):
    """Employee share of health (+LTC 40-64), child-support levy, pension (to 70), employment insurance."""
    e = params("social_insurance")["employee"]
    table = _csv(e["premium_table"]["value"])
    monthly = salary / 12
    g = _grade(table, monthly)
    health = g["health_ltc_half"] if e["ltc_age_from"]["value"] <= age < e["ltc_age_to_exclusive"]["value"] else g["health_half"]
    pension_rows = [r for r in table if r["pension_half"] is not None]
    pg = pension_rows[0] if monthly < pension_rows[0]["from"] else _grade(pension_rows, monthly)
    pension = pg["pension_half"] if age < e["pension_age_to_exclusive"]["value"] else 0
    rate = e["employment_insurance_worker_rate"]["value"]
    return {
        "health": 12 * half_round(health),
        "child_levy": 12 * half_round(g["child_levy_half"]),
        "pension": 12 * half_round(pension),
        "employment": 12 * half_round(monthly * rate),
    }


def nhi_household(members, householder=None):
    """Shinjuku FY2026 NHI for the NHI-insured members of one household.

    members: list of dicts with age, total_income (総所得金額等), pension_income, has_earnings.
    householder: same shape, when the householder is not in NHI; their income still counts in the reduction test.
    """
    if not members:
        return 0
    p = params("social_insurance")["nhi_shinjuku_fy2026"]
    base = [max(0, m["total_income"] - p["base_deduction"]["value"]) for m in members]
    n = len(members)
    n18 = sum(m["age"] >= p["child_levy"]["age_from"] for m in members)
    ltc = [b for m, b in zip(members, base) if p["ltc_40_64"]["age_from"] <= m["age"] < p["ltc_40_64"]["age_to_exclusive"]]
    # flat-amount reduction by household income (65+ pension income gets an extra 150,000 off for this test)
    r = p["flat_reduction"]
    extra = r["pensioner_65_extra_deduction"]
    tested = members + ([householder] if householder else [])
    test_income = sum(m["total_income"] - (min(extra["value"], m["pension_income"]) if m["age"] >= extra["age_from"] else 0) for m in tested)
    earners = max(1, sum(m["has_earnings"] for m in tested))
    limit0 = r["base"]["value"] + (earners - 1) * r["per_extra_earner"]["value"]
    cut = 0.0
    for tier in ("seventy_percent", "fifty_percent", "twenty_percent"):
        if test_income <= limit0 + r[tier]["per_member_add"] * n:
            cut = r[tier]["share"]
            break
    keep = 1 - cut
    part = lambda flat, rate, bases, count, cap: min(cap, flat * count * keep + rate * sum(bases))
    total = (part(p["medical"]["per_member"], p["medical"]["rate"], base, n, p["medical"]["cap"])
             + part(p["support"]["per_member"], p["support"]["rate"], base, n, p["support"]["cap"])
             + part(p["ltc_40_64"]["per_member"], p["ltc_40_64"]["rate"], ltc, len(ltc), p["ltc_40_64"]["cap"])
             + part(p["child_levy"]["per_member_18_plus"], p["child_levy"]["rate"], base, n18, p["child_levy"]["cap"]))
    return math.floor(total)


# ---------- income tax ----------

def income_tax_before_surtax(total_income, deductions):
    it = params("income_tax")
    taxable = floor_to(max(0, total_income - deductions), it["rate_schedule"]["taxable_income_rounding"]["value"])
    for upper, rate, minus in it["rate_schedule"]["bands"]:
        if taxable <= upper:
            break
    else:
        rate, minus = it["rate_schedule"]["top"]
    return max(0, math.floor(taxable * rate - minus))


def income_tax(total_income, deductions, credit=0):
    """Tax credits come off before the 2.1% surtax, as with the NTA example's housing credit (年末調整のしかた p.59)."""
    it = params("income_tax")
    tax = max(0, income_tax_before_surtax(total_income, deductions) - credit)
    return floor_to(tax * it["reconstruction_surtax_factor"]["value"], it["final_rounding"]["value"])


def basic_deduction_it(total_income):
    b = params("income_tax")["basic_deduction"]
    return band(b["bands"], total_income, b["above"])


def spouse_deduction_it(earner_income, spouse_income, spouse_age=0):
    s = params("income_tax")["spouse_deduction"]
    if earner_income > s["earner_bands"][-1][0]:
        return 0
    col = band(s["earner_bands"], earner_income)
    ordinary = s["spouse_ordinary"]["bands"]
    if spouse_age >= s["elderly_age_from"]["value"] and spouse_income <= ordinary[-1][0]:
        return s["elderly_spouse_ordinary"]["value"][col]
    return band(ordinary + s["spouse_special"]["bands"], spouse_income, [0, 0, 0])[col]


def specific_relative_special_it(income):
    it = params("income_tax")
    if income <= it["dependent_deduction"]["income_limit"]["value"]:
        return 0
    return band(it["specific_relative_special_deduction"]["bands"], income)


# ---------- resident tax ----------

def resident_tax(total_income, deductions, diff, n_family, single_parent):
    """所得割 + 均等割 (incl. forest environment tax). n_family = 同一生計配偶者 + 扶養親族 (incl. under 16)."""
    rt = params("resident_tax")
    nt = rt["non_taxable"]
    line = lambda add: nt["single"]["value"] if n_family == 0 else nt["per_person"]["value"] * (n_family + 1) + nt[add]["value"]
    if single_parent and total_income <= nt["single_parent_none_if_total_income_le"]["value"]:
        return 0
    if total_income <= line("per_capita_add"):
        return 0
    pcl = rt["per_capita_levy"]
    per_capita = pcl["ward"]["value"] + pcl["tokyo"]["value"] + pcl["forest_environment_tax"]["value"]
    levy_line = line("income_levy_add")
    if total_income <= levy_line:
        return per_capita
    taxable = floor_to(max(0, total_income - deductions), rt["rounding"]["taxable_income"]["value"])
    a = rt["adjustment_credit"]
    if taxable <= a["threshold"]["value"]:
        base = min(diff, taxable)
    else:
        base = max(diff - (taxable - a["threshold"]["value"]), a["minimum_base"]["value"])
    # 特別区民税 and 都民税 each: rate × taxable − its share of the 調整控除
    levies = [max(0, taxable * rt["income_levy_rate"][k]["value"] - a["rate"][k]["value"] * base) for k in ("ward", "tokyo")]
    total = sum(levies)
    if total > total_income - levy_line > 0:  # burden-relief band (relief_band): the excess comes off each tax in proportion
        levies = [x * (total_income - levy_line) / total for x in levies]
    return sum(floor_to(x, rt["rounding"]["income_levy"]["value"]) for x in levies) + per_capita


def specific_relative_special_rt(income):
    """特定親族特別控除 (resident tax, 令和9年度): a relative aged 19-22 whose income is above the dependant limit."""
    return band(params("resident_tax")["personal_deductions"]["specific_relative_special"]["bands"], income)


def basic_deduction_rt(total_income):
    b = params("resident_tax")["basic_deduction"]["taper"]
    return band(b["bands"], total_income, b["above"])


# ---------- child allowance ----------

def child_allowance(child_ages):
    """Monthly amounts x 12. Order counts eldest first; children are those up to high-school age (≤18 here)."""
    m = params("child_allowance")["monthly"]
    total = 0
    for rank, age in enumerate(sorted(child_ages, reverse=True), 1):
        if rank >= m["third_child_and_later"]["rank_from"]:
            total += m["third_child_and_later"]["value"]
        elif age < m["under_3"]["age_under"]:
            total += m["under_3"]["value"]
        else:
            total += m["age_3_to_high_school"]["value"]
    return 12 * total


def spouse_deduction_rt(earner, spouse, age):
    """Resident-tax deduction for a spouse and its 調整控除 difference, from the earner's and the spouse's total income
    (地方税法314条の2第1項第10号・第10号の2, 314条の6第1号イ表(6); tests/hand_calcs/spouse_rt.md)."""
    rt = params("resident_tax")
    rp, dp = rt["personal_deductions"], rt["personal_deduction_difference"]
    if earner > rp["spouse_earner_income_limit"]["value"]:
        return 0, 0
    elderly = age >= rp["elderly_spouse_age_from"]["value"]
    if earner <= rp["spouse_earner_full_limit"]["value"]:
        key = "elderly_spouse" if elderly else "spouse"
        amount, diff, thirds = rp[key]["value"], dp[key]["value"], 3
    else:
        upper, sp, old, d, d_old, thirds = next(r for r in rp["spouse_earner_above_9m"]["bands"] if earner <= r[0])
        amount, diff = (old, d_old) if elderly else (sp, d)
    if spouse <= rp["dependant_income_limit"]["value"]:
        return amount, diff
    unit = rp["spouse_earner_above_9m"]["special_round_up"]
    return math.ceil(band(rp["spouse_special"]["bands"], spouse) * thirds / 3 / unit) * unit, 0  # 0 above 1,330,000


def child_rearing_allowance(income, children, ordinary, specific, pension=0):
    """Annual 児童扶養手当 for a claimant with `children` (監護等児童) whose test income is `income` (施行令4条1項). Dependants and
    supported children raise the limits: `ordinary` at 380,000 each, `specific` (aged 16 to 22) at 530,000 each (施行令2条の4).
    A public pension of the claimant (`pension`, a year) is taken off month by month (施行令6条の5)."""
    if children <= 0:
        return 0
    p = params("child_rearing_allowance")
    lim, m, wh = p["limits"], p["monthly"], p["withheld"]
    extra = ordinary * lim["per_dependant"]["value"] + specific * lim["per_specific"]["value"]
    full, stop = lim["full_base"]["value"] + extra, lim["partial_base"]["value"] + extra
    if income >= stop:
        return 0
    unit = wh["round_to"]["value"]
    to_unit = lambda x: math.floor(x / unit + 0.5) * unit  # under 5 down, 5 or more up (2条の4第3項, 6条の5第2項第8号)
    # nothing withheld below the full limit; above it the rounded share plus 10 (2条の4第3項・第4項)
    withheld = lambda rate: 0 if income < full else to_unit((income - full) * rate) + wh["plus"]["value"]
    monthly = (m["first_child"]["value"] - withheld(wh["first_child_rate"]["value"])
               + (children - 1) * (m["each_further_child"]["value"] - withheld(wh["further_child_rate"]["value"])))
    return 12 * max(0, monthly - to_unit(pension // 12))


def ltc_65_premium(taxed, household_taxed, total_income, pension_revenue, pension_income, salary_income):
    """Shinjuku fiscal 2026 long-term-care premium for one person aged 65+ (ltc_65.yaml; tests/hand_calcs/H6.md revision).
    taxed: the person pays resident tax; household_taxed: someone in the household does."""
    p = params("ltc_65")
    if taxed:
        return next((a for upper, a in p["taxed"]["bands"] if total_income < upper), p["taxed"]["above"])
    # 課税年金収入 + その他の合計所得金額, with 給与所得 less 100,000 (bands 1-5)
    other = max(0, total_income - pension_income - min(p["salary_adjustment"]["value"], salary_income))
    measure = pension_revenue + other
    low, mid = p["low_line"]["value"], p["mid_line"]["value"]
    if household_taxed:
        return p["household_taxed"]["value"][0 if measure <= low else 1]
    return p["household_untaxed"]["value"][0 if measure <= low else 1 if measure <= mid else 2]

