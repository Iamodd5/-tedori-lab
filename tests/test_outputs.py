"""Milestone 4: wall map (spec 9.2) and household comparison (spec 9.1)."""
from engine import household as h
from engine import wall_map as w


def test_h1_baseline_walls_match_hand_calculation():
    # tests/hand_calcs/wall_H1.md
    emr = {r["income"]: r["emr"] for r in w.grid(h.load("H1"), "baseline", top=1_200_000)}
    assert emr[1_110_000] == 1.7088                    # premium band step 88,000 -> 98,000
    # joining employee insurance raises take-home. wall_H1.md revision 2 (2026-11-03 recheck): below 88,000 a month H1
    # stays out all year (特定減額特例), and pays employment insurance at every wage (+90,013 first, +69,994 in revision 1)
    assert emr[1_050_000] == round(1 - 95_257 / 10_000, 4)
    assert h.compute(w.at_income(h.load("H1"), 1_050_000))["disposable"] == 809_595


def test_h2_walls_match_hand_calculation():
    # tests/hand_calcs/H2.md, wall map points (令和9年度 working-student limit 890,000)
    hh = h.load("H2")
    got = {s: h.compute(w.at_income(hh, s))["disposable"] for s in (1_490_000, 1_500_000, 1_630_000, 1_640_000)}
    assert got == {1_490_000: 1_482_000, 1_500_000: 1_406_428, 1_630_000: 1_516_074, 1_640_000: 1_497_616}


def test_grid_point_at_reference_income_matches_household():
    hh = h.load("H7")
    rows = w.grid(hh, "baseline", top=3_000_000)
    assert rows[-1]["income"] == 3_000_000 and rows[-1]["disposable"] == h.compute(hh)["disposable"]


def test_daiwa_grid_adds_change_to_baseline():
    hh = h.load("H1")
    base = w.grid(hh, "baseline", top=1_250_000)[-1]["disposable"]
    assert w.grid(hh, "daiwa", top=1_250_000)[-1]["disposable"] == base + 35_700   # tests/hand_calcs/daiwa.md


def test_two_income_households_use_the_chosen_member():
    # the project owner's choice of whose income moves
    assert [w.varying_member(h.load(x)) for x in ("H3", "H4", "H6", "H8")] == [
        ("a", "salary"), ("b", "salary"), ("a", "public_pension"), ("a", "salary")]


def test_h4_spouse_hits_the_13m_wall():
    # tests/hand_calcs/wall_H4.md
    emr = {r["income"]: r["emr"] for r in w.grid(h.load("H4"), "baseline", top=1_300_000)}
    assert emr[1_290_000] == 26.8226  # main earner deducts the spouse's national pension; see hand calc revision


def test_h4_wall_cause_matches_hand_calculation():
    # tests/hand_calcs/wall_H4.md: the spouse leaves dependant status; national pension 17,920 × 12 and NHI 101,786 start,
    # the head's income tax falls 16,100 and resident tax 33,500, the spouse's resident tax rises 1,000
    (c,) = w.wall_causes(h.load("H4"), [{"from": 1_290_000, "at": 1_300_000}])
    assert c["scheme"] == ["dependant", "nhi"]
    assert c["change"] == {"income_tax": -16_100, "resident_tax": -32_500, "employee_insurance": 0,
                           "national_pension": 215_040, "nhi": 101_786, "child_allowance": 0}


def test_outputs_snapshot_is_current():
    # Spec 12.1: fails on any unexplained change. After an intended change, run `make outputs` and explain it in the commit message.
    import json, pathlib
    from engine import reforms as r
    saved = json.loads((pathlib.Path(__file__).parents[1] / "outputs" / "household_comparison.json").read_text())
    for row in saved:
        hh = h.load(row["household"])
        now = r.run(row["design"], hh)
        assert (h.compute(hh)["disposable"], now["disposable_change"], now["components"]) == \
               (row["baseline_disposable"], row["disposable_change"], row["components"]), (row["household"], row["design"])


def test_own_household_shapes_match_example_households():
    # the "your own household" shapes are built like the example households they resemble
    disp = lambda shape, age, kids, s: h.compute(w.own(shape, age, kids, s))["disposable"]
    assert disp("single", 30, 0, 1_250_000) == h.compute(h.load("H1"))["disposable"]          # H1: 30, part-time 20+ hours
    assert disp("couple_part", 45, 0, 5_000_000) == h.compute(h.load("H4"))["disposable"]     # H4: head 5.0m, spouse 1.0m under 20 hours
    assert len(list(w.own_combinations())) == 24
