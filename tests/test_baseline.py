"""2026 baseline rules. Expected values come from official worked examples or tables, or from tests/hand_calcs/."""
import pathlib

import pytest
import yaml

from engine import baseline as b
from engine import household as h

HAND = pathlib.Path(__file__).parent / "hand_calcs"


# --- NTA 令和8年分 年末調整のしかた, 設例 (pp.57-59): salary 8,970,000 with spouse, specific relative and child under 23
def test_nta_example_employment_income_and_adjustment():
    assert b.employment_income(8_970_000) == 7_020_000          # p.58 item 2
    assert b.adjustment_deduction(8_970_000, True) == 47_000    # p.58 item 3


def test_nta_example_deductions():
    assert b.basic_deduction_it(6_973_000) == 620_000            # p.59 item 10
    assert b.spouse_deduction_it(6_973_000, 500_000) == 380_000  # p.59 item 7
    assert b.specific_relative_special_it(990_000) == 410_000    # p.59 item 8 (income 95-100万)


def test_nta_example_rate_schedule_and_surtax():
    # p.59 items 12-15: taxable 2,146,898 -> 2,146,000 -> 117,100; after housing credit 40,600 -> x1.021 -> 41,400
    assert b.income_tax(2_146_898, 0) == b.floor_to(117_100 * 1.021, 100)
    assert b.floor_to(40_600 * 1.021, 100) == 41_400


# --- NTA employment-income table rows (p.48) and formula ranges (p.3)
@pytest.mark.parametrize("salary, expected", [(740_999, 0), (741_000, 1_000), (2_190_999, 1_450_999),
                                              (2_584_000, 1_728_800), (2_999_999, 2_017_200), (6_600_000, 4_840_000)])
def test_employment_income(salary, expected):
    assert b.employment_income(salary) == expected


# --- Shinjuku 令和8年度 国民健康保険料 概算早見表 (sources/shinjuku/000452428.pdf): one member, under 40 and 40-64
@pytest.mark.parametrize("income, under40, age40_64", [(1_100_000, 137_959, 172_040), (2_000_000, 233_179, 289_130),
                                                       (3_000_000, 338_979, 419_230)])
def test_nhi_matches_shinjuku_quick_table(income, under40, age40_64):
    # the quick table shows amounts before the income-based flat reduction; these incomes are above the 20% limit
    assert b.nhi_household([{"age": 35, "total_income": income, "pension_income": 0, "has_earnings": True}]) == under40
    assert b.nhi_household([{"age": 50, "total_income": income, "pension_income": 0, "has_earnings": True}]) == age40_64


# --- 協会けんぽ Tokyo FY2026 table (sources/social/kyoukaikenpo_R8_13tokyo.pdf)
def test_employee_premiums_table_lookup():
    p = b.employee_premiums(300_000 * 12, 45)            # standard monthly 300,000 (grade 22), LTC age
    assert p["health"] == 12 * 17_205 and p["pension"] == 12 * 27_450 and p["child_levy"] == 12 * 345
    low = b.employee_premiums(70_000 * 12, 30)           # below the pension floor: pension uses 88,000
    assert low["pension"] == 12 * 8_052


def test_child_allowance():
    assert b.child_allowance([8, 2]) == 12 * 25_000
    assert b.child_allowance([17, 12, 1]) == 12 * (10_000 + 10_000 + 30_000)


# --- Households H1-H8 against documented hand calculations (Milestone 2 acceptance: within 1,000 yen)
EXPECTED = yaml.safe_load((HAND / "expected.yaml").read_text())


@pytest.mark.parametrize("hid", sorted(EXPECTED))
def test_household_matches_hand_calculation(hid):
    assert abs(h.compute(h.load(hid))["disposable"] - EXPECTED[hid]) <= 1000


# --- Shinjuku reduction test counts the householder even when not in NHI (sources/shinjuku/hoken01_002030.html:
# "世帯主と被保険者全員の前年中の総所得金額等"). Hand calc: tests/hand_calcs/wall_H4.md
def test_nhi_reduction_counts_householder_outside_nhi():
    spouse = {"age": 43, "total_income": 560_000, "pension_income": 0, "has_earnings": True}
    assert b.nhi_household([spouse]) < 101_786                       # alone, 560,000 qualifies for a cut
    head = {"age": 45, "total_income": 3_560_000, "pension_income": 0, "has_earnings": True}
    assert b.nhi_household([spouse], householder=head) == 101_786    # with the head's income: no cut


# --- Burden-relief band above the income-levy exemption line: the levy is capped at the excess over the line.
# MIC 個人住民税の基礎控除・非課税限度額等 (sources/tax/soumu_kojin_juminzei_kiso_kojo_r8.pdf) p.18: couple, line
# 1,120,000, total income 1,124,200 -> income levy 4,200.
def test_nhi_reduction_counts_earners_as_the_cabinet_order_does():
    # tests/hand_calcs/H6.md revision 2026-11-03: the spouse's 800,000 pension (age 72) is not over 1,250,000, so 1 earner
    import copy
    hh = copy.deepcopy(h.load("H6"))
    next(m for m in hh["members"] if m["role"] == "head")["public_pension"] = 1_700_000
    assert h.compute(hh)["disposable"] == 2_414_941


def test_specific_relative_special_rt():
    # 特定親族特別控除 for resident tax, 令和9年度 (sources/tax/ota_shotokukojo.html table; 地方税法314条の2第1項第12号)
    assert b.specific_relative_special_rt(620_001) == 450_000   # 62万超95万以下
    assert b.specific_relative_special_rt(990_000) == 410_000   # 95万超100万以下
    assert b.specific_relative_special_rt(1_230_000) == 30_000  # 120万超123万以下
    assert b.specific_relative_special_rt(1_230_001) == 0


def test_resident_tax_rounds_ward_and_tokyo_separately():
    # Ota City worked example (sources/tax/ota_keisan_no_shikumi.html): total income 4,930,000, deductions 1,595,550 →
    # taxable 3,334,000; 特別区民税 198,540 + 3,000 → 201,500; 都民税 132,360 + 1,000 → 133,300 (地方税法20条の4の2第3項).
    # Plus the forest environment tax 1,000. Rounding the 10% once would give 330,900 + 5,000.
    assert b.resident_tax(4_930_000, 1_595_550, 50_000, 0, False) == 201_500 + 133_300 + 1_000


@pytest.mark.xfail(strict=True, reason="OPEN_QUESTIONS Q22 (reread 2026-11-03 recheck): MIC's p.18 figure plots the levy "
                   "before rounding, 4,200 = 2,520 + 1,680, which the engine also reaches; this test compares it with the "
                   "rounded amount, 2,500 + 1,600 (地方税法20条の4の2第3項). Kept so a return to one combined rounding fails")
def test_resident_tax_relief_band_matches_mic_figure():
    # couple (N = 1): per-capita line 350,000 x 2 + 310,000 = 1,010,000 is passed, so the 5,000 per-capita levy applies
    assert b.resident_tax(1_124_200, 430_000 + 330_000, 100_000, 1, False) == 4_200 + 5_000


def test_resident_tax_relief_band_by_law():
    # 地方税法附則3条の3第2項・第5項: each tax's 所得割 is cut by the excess × its share, so the two together equal
    # income − line = 4,200, shared 60:40 (only the 調整控除 applies: 3% and 2%) = 2,520 and 1,680; each rounded down
    # to 100 yen (20条の4の2第3項) = 2,500 + 1,600. Per-capita 3,000 + 1,000 + forest 1,000.
    assert b.resident_tax(1_124_200, 430_000 + 330_000, 100_000, 1, False) == 2_500 + 1_600 + 5_000


def test_resident_tax_relief_band_h3_head():
    # H3 head with two children (N = 2): line 350,000 x 3 + 420,000 = 1,470,000; income 1,480,000 -> levy 10,000
    assert b.resident_tax(1_480_000, 430_000 + 330_000, 50_000, 2, False) == 10_000 + 5_000


# --- Elderly spouse: NTA 年末調整のしかた p.55 (老人控除対象配偶者, earner ≤ 9m) -- tests/hand_calcs/claimant.md
def test_elderly_spouse_deduction():
    assert b.spouse_deduction_it(3_000_000, 500_000, spouse_age=72) == 480_000
    assert b.spouse_deduction_it(3_000_000, 500_000, spouse_age=69) == 380_000


# --- The higher-earning partner claims the other (tests/hand_calcs/claimant.md)
def test_higher_earner_claims_spouse():
    hh = h.load("H3")
    hh["members"][0]["salary"] = 1_000_000
    assert h.compute(hh)["members"]["b"]["income_tax"] == 7_200


def test_partner_can_be_dependant_of_employee_spouse():
    hh = h.load("H3")
    hh["members"][0]["salary"] = 0
    a = h.compute(hh)["members"]["a"]
    assert a["scheme"] == "dependant" and a["national_pension"] == 0 and a["nhi"] == 0


# --- Resident-tax spouse deduction by the earner's income, 令和9年度 (tests/hand_calcs/spouse_rt.md; OPEN_QUESTIONS Q37)
@pytest.mark.parametrize("earner, spouse, age, expected", [
    (8_000_000, 0, 40, (330_000, 50_000)), (9_050_000, 0, 40, (220_000, 40_000)), (9_550_000, 0, 72, (130_000, 30_000)),
    (8_000_000, 1_200_000, 40, (160_000, 0)), (9_050_000, 1_200_000, 40, (110_000, 0)), (9_550_000, 1_200_000, 40, (60_000, 0)),
    (10_050_000, 0, 40, (0, 0))])
def test_spouse_deduction_rt(earner, spouse, age, expected):
    assert b.spouse_deduction_rt(earner, spouse, age) == expected


@pytest.mark.parametrize("salary, lower", [(10_500_000, 33_000), (11_000_000, 22_000), (11_500_000, 11_000)])
def test_spouse_lowers_resident_tax_by_earner_band(salary, lower):
    from engine import wall_map as w
    rt = lambda shape: h.compute(w.own(shape, 45, 0, salary))["members"]["a"]["resident_tax"]
    assert rt("single") - rt("couple") == lower


def test_h4_head_resident_tax_at_the_620000_spouse_limit():
    # tests/hand_calcs/wall_H4.md, "The ¥620,000 spouse limit" (OPEN_QUESTIONS Q40)
    from engine import wall_map as w
    head = lambda s: h.compute(w.at_income(h.load("H4"), s))["members"]["a"]["resident_tax"]
    assert (head(1_340_000), head(1_370_000)) == (171_300, 173_500)
