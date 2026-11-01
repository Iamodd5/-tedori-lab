"""Milestone 4: wall map (spec 9.2) and household comparison (spec 9.1)."""
from engine import household as h
from engine import wall_map as w


def test_h1_baseline_walls_match_hand_calculation():
    # tests/hand_calcs/wall_H1.md
    emr = {r["income"]: r["emr"] for r in w.grid(h.load("H1"), "baseline", top=1_200_000)}
    assert emr[1_110_000] == 1.7088                    # premium band step 88,000 -> 98,000
    assert emr[1_050_000] == round(1 - 90_013 / 10_000, 4)  # joining employee insurance raises take-home


def test_grid_point_at_reference_income_matches_household():
    hh = h.load("H7")
    rows = w.grid(hh, "baseline", top=3_000_000)
    assert rows[-1]["income"] == 3_000_000 and rows[-1]["disposable"] == h.compute(hh)["disposable"]


def test_daiwa_grid_adds_change_to_baseline():
    hh = h.load("H1")
    base = w.grid(hh, "baseline", top=1_250_000)[-1]["disposable"]
    assert w.grid(hh, "daiwa", top=1_250_000)[-1]["disposable"] == base + 40_200   # tests/hand_calcs/daiwa.md


def test_multi_earner_households_wait_for_a_decision():
    assert w.varying_member(h.load("H3")) is None   # HUMAN_TODO H-11
