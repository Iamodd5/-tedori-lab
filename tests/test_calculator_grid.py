"""The Compare page's two calculators read a precomputed ¥10,000 grid. An amount between two grid points
must never be shown as the nearer point: a wall can lie between them (for H4 one lies between ¥1,290,000 and
¥1,300,000, so ¥1,295,000 shown at ¥1,300,000 would be far too low). site/grid.js decides which grid points to
show; run in Node.
"""
import json
import pathlib
import re
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
STEP, TOP = 10_000, 10_000_000


def points(raw):
    expr = f"require('./site/grid.js').gridPoints({json.dumps(raw)}, {STEP}, {TOP})"
    out = subprocess.run(["node", "-e", f"console.log(JSON.stringify({expr}))"], capture_output=True, text=True, cwd=ROOT, check=True)
    return json.loads(out.stdout)


def test_amount_on_the_grid_is_exact():
    assert points("1300000") == {"lo": 1_300_000, "hi": 1_300_000, "exact": True, "capped": False}


@pytest.mark.parametrize("raw", ["1,300,000", "130万", "１３０万円", "¥1,300,000"])
def test_the_ways_the_page_accepts_an_amount(raw):
    assert points(raw) == {"lo": 1_300_000, "hi": 1_300_000, "exact": True, "capped": False}


def test_amount_between_grid_points_gives_both():
    assert points("1295000") == {"lo": 1_290_000, "hi": 1_300_000, "exact": False, "capped": False}
    assert points("1290001") == {"lo": 1_290_000, "hi": 1_300_000, "exact": False, "capped": False}
    assert points("129.5万") == {"lo": 1_290_000, "hi": 1_300_000, "exact": False, "capped": False}


@pytest.mark.parametrize("raw", ["", "  ", "-1", "abc", "1e6", "NaN", "Infinity", "1.2.3", "万"])
def test_no_result_for_input_that_is_not_an_amount(raw):
    assert points(raw) is None


def test_amount_above_the_top_is_capped_and_says_so():
    assert points("12000000") == {"lo": TOP, "hi": TOP, "exact": False, "capped": True}


def test_every_wall_is_bracketed_not_rounded_across():
    walls = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]
    checked = 0
    for hid, hh in walls.items():
        pts = hh["designs"]["baseline"]
        for (a, ta, *_), (b, tb, *_) in zip(pts, pts[1:]):
            if tb < ta:                                    # take-home falls between a and b
                p = points(str(a + (b - a) // 2 + 1))      # just past the middle, where rounding would jump to b
                assert (p["lo"], p["hi"], p["exact"]) == (a, b, False), f"{hid}: {a}→{b}"
                checked += 1
    assert checked > 0


def test_compare_page_uses_grid_js_and_no_nearest_rounding():
    page = (ROOT / "site" / "compare.html").read_text(encoding="utf-8")
    assert 'src="grid.js"' in page
    assert "Math.round(raw / step)" not in page
    # site/walls.js gridPoint picks the nearer point when it finds no wall between the two; grid.js replaces it
    for p in sorted(ROOT.glob("site/*.js")) + sorted(ROOT.glob("site/*.html")):
        if p.name != "grid.js":
            assert not re.search(r"\bgridPoint\(", p.read_text(encoding="utf-8")), f"{p.name} still uses gridPoint"
    assert "rounded to ¥10,000" not in page and "1万円単位に丸めています" not in page
