"""Population view (SPEC 9.3): model households from the survey cells, deciles, totals. Hand calcs: tests/hand_calcs/population.md."""
import csv
import pathlib

import pytest

from engine import population as pop

ROOT = pathlib.Path(__file__).resolve().parents[1]


def check(name):
    return next(int(r["value"]) for r in csv.DictReader(open(ROOT / "population/checks.csv")) if r["name"] == name)


def test_cells_cover_every_household_in_the_survey():
    # 総世帯 total in 第3-32-1表 is 53,790,732; cells the survey hides are counted, not lost
    cells = pop.cells()
    assert sum(c["households"] for c in cells) + check("households_in_suppressed_cells") == pytest.approx(53_790_732, abs=50)


def test_single_band_04_split_matches_hand_calc():
    cell = next(c for c in pop.cells() if c["group"] == "single" and c["band"] == "04")
    pension, work = pop.model_households(cell)
    assert pension["weight"] == pytest.approx(1_397_853.04, abs=0.01)
    assert work["weight"] == pytest.approx(1_042_603.96, abs=0.01)
    (p,) = pension["household"]["members"]
    (w,) = work["household"]["members"]
    assert (p["age"], p["public_pension"], p["salary"], p["business_income"]) == (70, 2_109_000, 0, 0)
    assert (w["age"], w["public_pension"], w["salary"], w["business_income"]) == (55, 0, 1_898_334, 210_666)


def test_couple_cell_earners_split_matches_hand_calc():
    cell = next(c for c in pop.cells() if c["group"] == "couple_2children" and c["band"] == "10")
    pension, one, two = pop.model_households(cell)
    assert [round(x["weight"], 2) for x in (pension, one, two)] == [13_019.66, 3_601.76, 230_387.58]
    pick = lambda x, k: [(m["age"], m.get("salary", 0), m.get("business_income", 0), m.get("public_pension", 0))
                         for m in x["household"]["members"] if m["role"] == k][0]
    assert pick(pension, "head") == (70, 0, 0, 3_680_568) and pick(pension, "spouse") == (70, 0, 0, 1_062_432)
    assert pick(one, "head") == (44, 3_845_240, 897_760, 0) and pick(one, "spouse") == (44, 0, 0, 0)
    assert pick(two, "head") == (44, 3_264_609, 762_198, 0) and pick(two, "spouse") == (44, 716_193, 0, 0)
    assert [m["age"] for m in two["household"]["members"] if m["role"] == "child"] == [10, 10]


def test_decile_split_matches_hand_calc():
    pieces = pop.decile_pieces([("a", 1, 6), ("b", 2, 4), ("c", 3, 10)])
    by = {}
    for key, decile, w in pieces:
        by.setdefault(key, []).append((decile, w))
    assert by["a"] == [(1, 2), (2, 2), (3, 2)]
    assert by["b"] == [(4, 2), (5, 2)]
    assert by["c"] == [(d, 2) for d in range(6, 11)]


def test_every_model_household_runs_and_weights_add_up():
    built = pop.build()
    cells = pop.cells()
    assert sum(m["weight"] for m in built) == pytest.approx(sum(c["households"] for c in cells))
    assert all(m["household"]["members"] for m in built)


def test_population_snapshot_is_current():
    # Spec 12.1, as for household_comparison.json: after an intended change, run `make outputs` and explain it in the commit message
    import json
    saved = json.loads((ROOT / "outputs" / "population.json").read_text())
    now = pop.results(list(saved["designs"]))
    for d, entry in saved["designs"].items():
        assert (entry.get("by_decile"), entry.get("cost_yen")) == (now["designs"][d].get("by_decile"), now["designs"][d].get("cost_yen")), d
    assert saved["calibration"] == json.loads(json.dumps(now["calibration"])), "calibration"
