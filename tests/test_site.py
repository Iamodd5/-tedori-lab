"""Chart helpers in site/walls.js (wall list, and how much of an extra ¥100,000 you keep), run in Node.
Expected values: tests/hand_calcs/wall_H4.md (the 1.3m wall) and the arithmetic in the comments."""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]


def js(expr, data, lang="en"):
    out = subprocess.run(["node", "-e", f"global.lang = '{lang}'; global.li = () => {{}}; global.t = o => o[lang] ?? o.ja;"
                          "global.yen = n => Math.round(n).toLocaleString('ja-JP'); const w = require('./site/walls.js');"
                          "const d = JSON.parse(require('fs').readFileSync(0)); console.log(JSON.stringify(" + expr + "))"],
                         input=json.dumps(data), capture_output=True, text=True, cwd=ROOT, check=True)
    return json.loads(out.stdout)


def test_h4_wall_is_listed_with_its_drop_and_recovery():
    pts = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H4"]["designs"]["baseline"]
    walls = js("w.bigWalls(d).walls", pts)
    assert walls[0] == {"from": 1_290_000, "at": 1_300_000, "drop": 258_226, "back": 1_640_000}


def test_keep_per_100000():
    # take-home 0 → 90,000 → 50,000 at income 0 / 100,000 / 200,000: keep 90,000 of the first ¥100,000, then −40,000 (a wall).
    # Changed 2026-11-03 (persona review E14): the step from income 0 is left out of the chart, as it already was from
    # the wall list, so [0, 90_000] is no longer expected. Recorded in docs/VALIDATION.md (project rule 5).
    pts = [[x * 10_000, round(x * 9_000) if x <= 10 else 90_000 - (x - 10) * 4_000] for x in range(21)]
    assert js("w.keepSeries(d)", pts) == [[100_000, -40_000]]


def test_h4_wall_reason():
    # tests/hand_calcs/wall_H4.md: +10,000 − 215,040 national pension − 101,786 NHI + 16,100 + 33,500 − 1,000 taxes
    causes = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H4"]["wall_causes"]
    c = next(x for x in causes if x["from"] == 1_290_000)
    assert js("w.wallReason(d)", c, "ja") == "扶養から外れて、国民年金保険料（年215,040円）と国民健康保険料（年101,786円）がかかるためです。税は合わせて年48,600円減ります。"
    # several items: H5 at 2.09m (single-parent resident-tax exemption ends, VALIDATION §6) and a premium step
    c = {"from": 0, "scheme": ["employee", "employee"], "change": {"income_tax": 0, "resident_tax": 31_200, "employee_insurance": 17_088,
         "national_pension": 0, "nhi": 0, "child_allowance": 0}}
    assert js("w.wallReason(d)", c, "ja") == "住民税が年31,200円増え、会社の保険料が、収入の段階が上がって年17,088円増えるためです。"
