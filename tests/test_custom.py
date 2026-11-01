"""Custom credit for the design builder (Milestone 8). Hand calc: tests/hand_calcs/custom_credit.md.
The site runs the same formula in JavaScript (site/custom.js); these tests run it in Node and compare."""
import json
import pathlib
import subprocess

import pytest

from engine import household as h
from engine import reforms as r

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = {"phase_in_rate": 0.10, "maximum": 100_000, "plateau_end": 3_000_000, "phase_out_rate": 0.05, "child_addition": 50_000}
SINGLES = [  # (salary, business income, pension, credit)
    (0, 0, 2_000_000, 0), (500_000, 0, 0, 50_000), (2_000_000, 0, 0, 100_000), (4_000_000, 0, 0, 50_000),
    (6_000_000, 0, 0, 0), (1_000_000, 0, 2_500_000, 75_000), (0, 300_000, 0, 30_000), (123_456, 0, 0, 12_345)]


def single(salary, business, pension):
    return {"members": [{"id": "a", "role": "head", "age": 40, "salary": salary, "business_income": business,
                         "public_pension": pension}]}


@pytest.mark.parametrize("salary,business,pension,credit", SINGLES)
def test_single_person_matches_hand_calc(salary, business, pension, credit):
    assert r.custom(single(salary, business, pension), P) == credit


def test_households_match_hand_calc():
    assert r.custom(h.load("H3"), P) == 225_000
    assert r.custom(h.load("H5"), P) == 150_000


def node(script, data):
    out = subprocess.run(["node", "-e", script], input=json.dumps(data), capture_output=True, text=True, cwd=ROOT, check=True)
    return json.loads(out.stdout)


def test_javascript_credit_matches_python():
    cases = [r.people(single(*c[:3])) for c in SINGLES] + [r.people(h.load(x)) for x in ("H3", "H5")]
    js = node("const c = require('./site/custom.js'); const d = JSON.parse(require('fs').readFileSync(0));"
              "console.log(JSON.stringify(d.cases.map(x => c.customCredit(x, d.p))))", {"cases": cases, "p": P})
    assert js == [c[3] for c in SINGLES] + [225_000, 150_000]


def test_javascript_population_matches_python():
    # the page's decile and cost numbers, computed in Node from outputs/builder.json, equal Python's
    builder = json.loads((ROOT / "outputs" / "builder.json").read_text())
    js = node("const c = require('./site/custom.js'); const d = JSON.parse(require('fs').readFileSync(0));"
              "console.log(JSON.stringify(c.populationResults(d.b, d.p)))", {"b": builder, "p": P})
    py = r.custom_population(builder, P)
    assert js.keys() == py.keys()
    for k in py:  # float sums: equal up to rounding
        assert js[k] == pytest.approx(py[k], rel=1e-9), k


def test_javascript_wall_adds_the_credit():
    # H5 at its reference salary 2,500,000: the hand calc's 150,000 on top of the 2026 take-home pay
    builder = json.loads((ROOT / "outputs" / "builder.json").read_text())
    base = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H5"]["designs"]["baseline"]
    js = node("const c = require('./site/custom.js'); const d = JSON.parse(require('fs').readFileSync(0));"
              "console.log(JSON.stringify(c.customWall(d.h, d.base, d.p)))", {"h": builder["households"]["H5"], "base": base, "p": P})
    at = {x: d for x, d, _ in js}
    assert at[2_500_000] == dict((x, d) for x, d, _ in base)[2_500_000] + 150_000
