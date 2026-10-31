"""Reforms (spec Section 8). Expected values come from tests/hand_calcs/daiwa.md and credit_shape.md."""
import pytest

from engine import household as h
from engine import reforms as r

HOUSEHOLDS = [f"H{i}" for i in range(1, 9)]
DESIGNS = ["government_final", "rengo", "daiwa", "food_tax_cut"]


# --- Daiwa headline variant (tests/hand_calcs/daiwa.md)
@pytest.mark.parametrize("hid, change", [("H1", 40_200), ("H3", -18_300), ("H7", -20_700)])
def test_daiwa_matches_hand_calculation(hid, change):
    res = r.run("daiwa", h.load(hid))
    assert res["disposable_change"] == change


def test_daiwa_h1_components():
    c = r.run("daiwa", h.load("H1"))["components"]
    assert c == {"income_tax": 0, "resident_tax": 0, "social_insurance": 0, "credit": 40_200, "consumption_tax": 0}


# --- Government payment shape with made-up test values (tests/hand_calcs/credit_shape.md)
TEST_P = {"earned_income_floor": 100_000, "income_ceiling": 6_000_000, "flat_amount_low_income": 20_000,
          "phase_in_start": 500_000, "phase_in_end": 1_500_000, "basic_amount": 60_000,
          "child_addition_per_child": 30_000, "phase_out_start": 3_000_000, "phase_out_rate": 0.1}


@pytest.mark.parametrize("earned, total, kids, expected", [
    (50_000, 50_000, 0, 0), (400_000, 400_000, 0, 20_000), (1_000_000, 1_000_000, 0, 40_000),
    (1_000_000, 1_000_000, 2, 100_000), (2_000_000, 3_500_000, 1, 40_000), (2_000_000, 3_950_500, 0, 0),
    (1_234_567, 1_234_567, 0, 50_000), (2_000_000, 6_000_001, 0, 0)])
def test_payment_shape(earned, total, kids, expected):
    assert r.payment(earned, total, kids, TEST_P) == expected


@pytest.mark.parametrize("pass_through, expected", [(1.0, 70_000), (0.5, 35_000)])
def test_food_tax_saving(pass_through, expected):
    assert r.food_tax_saving(1_080_000, pass_through) == expected


# --- Every design runs on every household (Milestone 3 acceptance)
@pytest.mark.parametrize("design", DESIGNS)
@pytest.mark.parametrize("hid", HOUSEHOLDS)
def test_every_design_runs(design, hid):
    res = r.run(design, h.load(hid))
    assert res["status"] in {"complete", "incomplete"}
    if res["status"] == "incomplete":
        assert res["missing"] and res["disposable_change"] is None   # never a made-up number
    else:
        assert isinstance(res["disposable_change"], int)


def test_unpublished_designs_are_incomplete():
    for design in ("government_final", "rengo", "food_tax_cut"):
        assert r.run(design, h.load("H1"))["status"] == "incomplete"
