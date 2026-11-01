"""Chart helpers in site/walls.js (wall list, and how much of an extra ¥100,000 you keep), run in Node.
Expected values: tests/hand_calcs/wall_H4.md (the 1.3m wall) and the arithmetic in the comments."""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]


def js(expr, data):
    out = subprocess.run(["node", "-e", "global.lang = 'en'; global.li = () => {}; const w = require('./site/walls.js');"
                          "const d = JSON.parse(require('fs').readFileSync(0)); console.log(JSON.stringify(" + expr + "))"],
                         input=json.dumps(data), capture_output=True, text=True, cwd=ROOT, check=True)
    return json.loads(out.stdout)


def test_h4_wall_is_listed_with_its_drop_and_recovery():
    pts = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H4"]["designs"]["baseline"]
    walls = js("w.bigWalls(d).walls", pts)
    assert walls[0] == {"from": 1_290_000, "at": 1_300_000, "drop": 258_226, "back": 1_640_000}


def test_keep_per_100000():
    # take-home 0 → 90,000 → 50,000 at income 0 / 100,000 / 200,000: keep 90,000 of the first ¥100,000, then −40,000 (a wall)
    pts = [[x * 10_000, round(x * 9_000) if x <= 10 else 90_000 - (x - 10) * 4_000] for x in range(21)]
    assert js("w.keepSeries(d)", pts) == [[0, 90_000], [100_000, -40_000]]
