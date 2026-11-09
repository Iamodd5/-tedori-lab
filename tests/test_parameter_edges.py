"""One case per rule value that no example household reaches (tests/hand_calcs/parameter_edges.md; case numbers below)."""
import pytest

from engine import baseline as b
from engine import household as h

FULL = {"full_time": True}


def claims(hh, monkeypatch):
    """The head's income-tax deductions, and resident-tax deductions and 調整控除 difference (the head is listed first)."""
    it, rt = [], []
    real_it, real_rt = b.income_tax, b.resident_tax
    monkeypatch.setattr(b, "income_tax", lambda ti, ded, credit=0: it.append(ded) or real_it(ti, ded, credit))
    monkeypatch.setattr(b, "resident_tax", lambda ti, ded, diff, n, sp: rt.append((ded, diff)) or real_rt(ti, ded, diff, n, sp))
    h.compute(hh, ltc_65=False)
    return it[0], rt[0][0], rt[0][1]


def gain(with_, without, monkeypatch):
    a, b_ = claims(with_, monkeypatch), claims(without, monkeypatch)
    return tuple(x - y for x, y in zip(a, b_))


def family(*extra, head=None):
    return {"members": [head or {"id": "a", "role": "head", "age": 45, "salary": 5_000_000, "work": FULL}, *extra]}


def child(age, **kw):
    return {"id": "c", "role": "child", "age": age, **kw}


# --- income tax
def test_1_employment_income_table_starts_at_2191000():
    assert b.employment_income(2_250_000) == 1_493_600


def test_2_income_adjustment_salary_cap():
    assert b.adjustment_deduction(11_000_000, True) == 150_000


def test_3_income_adjustment_needs_a_dependant_under_23():
    head = {"id": "a", "role": "head", "age": 50, "salary": 9_000_000, "work": FULL}
    adj = lambda age: h.compute(family(child(age), head=head))["members"]["a"]["adjustment_deduction"]
    assert (adj(22), adj(23)) == (50_000, 0)


def test_4_public_pension_table_from_65():
    assert b.pension_income(2_000_000, 65) == 900_000


def test_5_elderly_spouse_from_70_income_tax():
    assert (b.spouse_deduction_it(3_560_000, 0, 70), b.spouse_deduction_it(3_560_000, 0, 69)) == (480_000, 380_000)


@pytest.mark.parametrize("case, older, younger, want", [
    ("6 dependant from 16", 16, 15, (380_000, 330_000, 50_000)),
    ("7 specific dependant from 19", 19, 18, (250_000, 120_000, 130_000)),
    ("8 specific dependant under 23", 22, 23, (250_000, 120_000, 130_000)),
])
def test_dependant_ages(case, older, younger, want, monkeypatch):
    assert gain(family(child(older)), family(child(younger)), monkeypatch) == want


def test_9_specific_dependant_amounts(monkeypatch):
    assert gain(family(child(19)), family(), monkeypatch) == (630_000, 450_000, 180_000)


def test_10_elderly_dependant_from_70(monkeypatch):
    dep = lambda age: {"id": "g", "role": "dependant", "age": age}
    assert gain(family(dep(70)), family(dep(69)), monkeypatch) == (100_000, 50_000, 50_000)


def test_11_dependant_income_limit(monkeypatch):
    assert gain(family(child(16, business_income=620_000)), family(), monkeypatch)[0] == 380_000
    assert gain(family(child(16, business_income=630_000)), family(), monkeypatch)[0] == 0


@pytest.mark.parametrize("income, want", [(5_000_000, 350_000), (5_000_001, 0)])
def test_12_single_parent_deduction_and_its_income_limit(income, want, monkeypatch):
    parent = lambda sp: {"id": "a", "role": "head", "age": 35, "business_income": income, "single_parent": sp}
    assert gain(family(child(8), head=parent(True)), family(child(8), head=parent(False)), monkeypatch)[0] == want


@pytest.mark.parametrize("salary, want", [(1_540_000, (270_000, 260_000, 10_000)), (1_631_000, (0, 0, 0))])
def test_13_working_student_deduction_and_its_income_limit(salary, want, monkeypatch):
    student = lambda s: {"id": "a", "role": "head", "age": 20, "salary": salary, "student": s}
    assert gain(family(head=student(True)), family(head=student(False)), monkeypatch) == want


# --- resident tax
def test_14_elderly_spouse_from_70_resident_tax():
    assert (b.spouse_deduction_rt(3_560_000, 0, 70), b.spouse_deduction_rt(3_560_000, 0, 69)) == ((380_000, 100_000), (330_000, 50_000))


def test_15_single_persons_line():
    assert b.resident_tax(460_000, 430_000, 50_000, 0, False) == 6_500


def test_16_single_parent_pays_none_up_to_1350000():
    assert b.resident_tax(1_350_000, 730_000, 100_000, 1, True) == 0
    assert b.resident_tax(1_400_000, 730_000, 100_000, 1, True) == 67_000


def test_17_no_adjustment_credit_above_25m():
    assert b.resident_tax(25_500_000, 0, 50_000, 0, False) == 2_555_000


# --- social insurance
def test_18_employee_ltc_to_64_and_pension_to_69():
    p = lambda age: b.employee_premiums(3_000_000, age)
    assert p(65)["health"] == p(39)["health"] < p(64)["health"]
    assert p(70)["pension"] == 0 and p(69)["pension"] == p(30)["pension"] > 0


@pytest.mark.parametrize("salary, scheme", [(1_750_000, "dependant"), (1_850_000, "nhi")])
def test_19_dependant_limit_from_60(salary, scheme):
    hh = family({"id": "b", "role": "spouse", "age": 60, "salary": salary}, head={"id": "a", "role": "head", "age": 62, "salary": 5_000_000, "work": FULL})
    assert h.compute(hh)["members"]["b"]["scheme"] == scheme


def test_20_national_pension_to_59():
    np = lambda age: h.compute(family(head={"id": "a", "role": "head", "age": age, "business_income": 3_000_000}))["members"]["a"]["national_pension"]
    assert (np(60), np(59)) == (0, 215_040)


def test_21_earners_in_the_nhi_reduction_test():
    assert h._nhi_earner({"age": 30, "salary": 560_000})
    assert h._nhi_earner({"age": 64, "public_pension": 610_000})
    assert h._nhi_earner({"age": 65, "public_pension": 1_260_000})


def test_22_reduction_line_per_extra_earner():
    m = lambda ti: {"age": 30, "total_income": ti, "pension_income": 0, "has_earnings": True}
    assert b.nhi_household([m(532_000), m(0)]) == 77_864


def test_23_reduction_test_takes_150000_off_65_plus_pension():
    assert b.nhi_household([{"age": 65, "total_income": 580_001, "pension_income": 580_001, "has_earnings": False}]) == 49_406


def test_24_65_plus_care_premium_from_65():
    ltc = lambda age: h.compute(family(head={"id": "a", "role": "head", "age": age, "public_pension": 2_000_000}))["members"]["a"]["ltc_65"]
    assert ltc(65) == ltc(66) > 0


# --- allowances
def test_25_child_allowance_to_18():
    assert (h.compute(family(child(18)))["child_allowance"], h.compute(family(child(19)))["child_allowance"]) == (120_000, 0)


def test_26_single_parent_allowance_for_children_to_18():
    parent = {"id": "a", "role": "head", "age": 40, "salary": 1_000_000, "single_parent": True}
    got = lambda age: h.compute(family(child(age), head=parent))["child_rearing_allowance"]
    assert got(19) == 0 < got(18)


def test_27_limit_for_a_dependant_aged_70_plus():
    assert b.child_rearing_allowance(2_560_000, 1, 0, 0, elderly=1) == 0
    assert b.child_rearing_allowance(2_550_000, 1, 0, 0, elderly=1) == 139_200


def test_28_further_child_rate():
    assert b.child_rearing_allowance(1_690_000, 2, 0, 0) == 346_920
