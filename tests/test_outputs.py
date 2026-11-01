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


def test_two_income_households_use_the_chosen_member():
    # HUMAN_TODO H-11: D
    assert [w.varying_member(h.load(x)) for x in ("H3", "H4", "H6", "H8")] == [
        ("a", "salary"), ("b", "salary"), ("a", "public_pension"), ("a", "salary")]


def test_h4_spouse_hits_the_13m_wall():
    # tests/hand_calcs/wall_H4.md
    emr = {r["income"]: r["emr"] for r in w.grid(h.load("H4"), "baseline", top=1_300_000)}
    assert emr[1_290_000] == 29.0126  # corrected 2026-11-01, see hand calc


def test_outputs_snapshot_is_current():
    # Spec 12.1: fails on any unexplained change. After an intended change, run `make outputs` and explain it in docs/LOG.md.
    import json, pathlib
    from engine import reforms as r
    saved = json.loads((pathlib.Path(__file__).parents[1] / "outputs" / "household_comparison.json").read_text())
    for row in saved:
        hh = h.load(row["household"])
        now = r.run(row["design"], hh)
        assert (h.compute(hh)["disposable"], now["disposable_change"], now["components"]) == \
               (row["baseline_disposable"], row["disposable_change"], row["components"]), (row["household"], row["design"])
