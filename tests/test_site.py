"""Chart helpers in site/walls.js (wall list, and how much of an extra ¥100,000 you keep) and the calculator grid in site/grid.js, run in Node.
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
    # Changed 2026-11-03: the step from income 0 is left out of the chart, as it already was from
    # the wall list, so [0, 90_000] is no longer expected. Recorded in docs/VALIDATION.md (project rule 5).
    pts = [[x * 10_000, round(x * 9_000) if x <= 10 else 90_000 - (x - 10) * 4_000] for x in range(21)]
    assert js("w.keepSeries(d)", pts) == [[100_000, -40_000]]


def test_h4_wall_reason():
    # tests/hand_calcs/wall_H4.md: +10,000 − 215,040 national pension − 101,786 NHI + 16,100 + 33,500 − 1,000 taxes
    causes = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H4"]["wall_causes"]
    c = next(x for x in causes if x["from"] == 1_290_000)
    assert js("w.wallReason(d)", c, "ja") == "健康保険と年金の扶養から外れて、国民年金保険料（年215,040円）と国民健康保険料（年101,786円）がかかるためです。所得税と住民税は合わせて年48,600円減ります。"
    # only resident tax falls (H2 at 1.49m): the sentence names resident tax alone
    c = next(x for x in json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H2"]["wall_causes"] if x["from"] == 1_490_000)
    assert c["change"]["income_tax"] == 0 and c["change"]["resident_tax"] < 0
    assert js("w.wallReason(d)", c, "ja").endswith(f"住民税が年{-c['change']['resident_tax']:,}円減ります。")
    assert js("w.wallReason(d)", c, "en").endswith(f"Resident tax falls by ¥{-c['change']['resident_tax']:,} a year.")
    # several items: H5 at 2.09m (single-parent resident-tax exemption ends, VALIDATION §6) and a premium step
    c = {"from": 0, "scheme": ["employee", "employee"], "change": {"income_tax": 0, "resident_tax": 31_200, "employee_insurance": 17_088,
         "national_pension": 0, "nhi": 0, "child_allowance": 0}}
    assert js("w.wallReason(d)", c, "ja") == "住民税が年31,200円増え、会社の保険料が、収入の段階が上がって年17,088円増えるためです。"


def test_wall_reason_names_what_starts_or_stops():
    # H2 at 2.19m: the deferral's income limit (tests/hand_calcs/H2.md). H6 at 2.11m → 2.12m: the head starts paying
    # resident tax (5,000), which moves the head from band 3 (51,480) to band 6 (87,120) and the spouse from band 1 (19,800)
    # to band 4 (63,360) (tests/hand_calcs/H6.md): 35,640 + 43,560 = 79,200. H5 at 3.85m: tests/hand_calcs/H5.md.
    causes = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]
    h2 = next(x for x in causes["H2"]["wall_causes"] if x["from"] == 2_190_000)
    assert h2["trigger"] == ["deferral_ends"]
    assert js("w.wallReason(d)", h2, "ja").startswith("学生納付特例（学生の国民年金保険料を後払いにできる制度）の所得の上限を超えて、国民年金保険料（年215,040円）がかかるためです。")
    h6 = next(x for x in causes["H6"]["wall_causes"] if x["from"] == 2_110_000)
    assert js("w.wallReason(d)", h6, "ja") == "住民税がかかり始め（年5,000円）、そのため65歳以上の人の介護保険料の段階が上がり、合わせて年79,200円増えるためです。"
    h5 = next(x for x in causes["H5"]["wall_causes"] if x["from"] == 3_850_000)
    assert js("w.wallReason(d)", h5, "ja") == "所得が児童扶養手当の上限を超えて、手当（年136,560円）が止まるためです。"


def test_typed_amounts_and_walls_between_grid_points():
    # compare.html calculators: H4's spouse pay ¥1,295,000 lies between grid points 1.29m and 1.3m with the 1.3m wall
    # between them (tests/hand_calcs/wall_H4.md), so both points must be shown, not the nearest one (site/grid.js)
    g = lambda body: f"((g, v) => {body})(require('./site/grid.js'), (k, x) => d.find(p => p[0] === x)[1])"
    assert js(g('["1300000", "1,300,000", "130万", "１３０万円", "", "abc"].map(g.readYen).map(x => Number.isNaN(x) ? "NaN" : x)'), None) == [1_300_000] * 4 + [None, "NaN"]
    pts = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H4"]["designs"]["baseline"]
    pick = lambda raw: js(g(f"{{ const p = g.gridPoints('{raw}', 10000, 1e7); return {{...p, jump: g.jumpBetween(p.lo, p.hi, 10000, v, ['b'])}}; }}"), pts)
    assert pick(1_295_000) == {"lo": 1_290_000, "hi": 1_300_000, "exact": False, "capped": False, "jump": True}
    assert pick(1_254_000) == {"lo": 1_250_000, "hi": 1_260_000, "exact": False, "capped": False, "jump": False}
    assert pick(12_000_000) == {"lo": 10_000_000, "hi": 10_000_000, "exact": False, "capped": True, "jump": False}
    # a jump up counts too: H1 joins company insurance between 1.05m and 1.06m (+95,257, tests/hand_calcs/wall_H1.md)
    h1 = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H1"]["designs"]["baseline"]
    assert js(g("g.jumpBetween(1050000, 1060000, 10000, v, ['b'])"), h1) is True
