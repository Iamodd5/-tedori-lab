"""Every number written into public text must come from outputs/ or parameters/, or be listed with its source.

Public text = pages and documents the site shows. A number typed by hand drifts when the outputs change,
so each one must be traceable: equal to a value in outputs/ (or a rounding of one: yen, 万, 億, trillion,
%, m), equal to a value in parameters/, households/ or population/, or listed in tests/number_sources.yaml
with where it comes from. Old values kept on purpose go between <!-- history --> and <!-- /history -->.
"""
import csv
import html
import json
import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC = (["docs/VALIDATION.md", "docs/METHODS.md", "docs/METHODS.ja.md", "OPEN_QUESTIONS.md",
           "report/report.ja.md", "report/report.en.md", "press/summary.ja.md"]
          + sorted(str(p.relative_to(ROOT)) for p in ROOT.glob("site/*.html"))
          + sorted(str(p.relative_to(ROOT)) for p in ROOT.glob("households/*.yaml"))
          + sorted(str(p.relative_to(ROOT)) for p in ROOT.glob("parameters/designs/*.yaml")))
UNIT = {"兆": "trillion", "trillion": "trillion", "億": "oku", "万": "man", "m": "m", "million": "m",
        "billion": "bn", "bn": "bn", "%": "%"}
TOKEN = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(兆|trillion|億|万|million|billion|bn|m(?![a-z])|%)?")


def _numbers(obj, out):
    if isinstance(obj, dict):
        for v in obj.values():
            _numbers(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _numbers(v, out)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out.add(float(obj))


def _known():
    vals = set()
    for p in ROOT.glob("outputs/**/*.json"):
        _numbers(json.loads(p.read_text(encoding="utf-8")), vals)
    for p in list(ROOT.glob("outputs/**/*.csv")) + list(ROOT.glob("population/*.csv")):
        for row in csv.reader(p.open(encoding="utf-8")):
            for cell in row:
                try:
                    vals.add(float(cell.replace(",", "")))
                except ValueError:
                    pass
    for p in list(ROOT.glob("parameters/**/*.yaml")) + list(ROOT.glob("households/*.yaml")) + list(ROOT.glob("population/*.yaml")):
        _numbers(yaml.safe_load(p.read_text(encoding="utf-8")), vals)
    # the pattern below reads digits without their sign (text writes −16,100 with a minus sign), so compare sizes
    ints = {round(abs(v)) for v in vals if abs(v - round(v)) < 1e-9}
    scaled = {u: set() for u in set(UNIT.values())}
    for v in map(abs, vals):
        for d in (0, 1, 2):
            scaled["%"] |= {round(v * 100, d), round(v, d)}
            scaled["trillion"].add(round(v / 1e12, d))
            scaled["oku"].add(round(v / 1e8, d))
            scaled["man"].add(round(v / 1e4, d))
            scaled["m"].add(round(v / 1e6, d))
            scaled["bn"].add(round(v / 1e9, d))
    return ints, scaled


def _text(path):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<!--\s*history\s*-->.*?<!--\s*/history\s*-->", " ", s, flags=re.S)
    if path.suffix == ".html":
        s = re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S)
        s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    elif path.suffix == ".yaml":
        parts = []

        def strings(o):
            if isinstance(o, dict):
                for v in o.values():
                    strings(v)
            elif isinstance(o, list):
                for v in o:
                    strings(v)
            elif isinstance(o, str):
                parts.append(o)
        strings(yaml.safe_load(s))
        s = "\n".join(parts)
    s = re.sub(r"https?://\S+", " ", s)
    return re.sub(r"\]\([^)]*\)", "]", s)


def _listed():
    p = ROOT / "tests" / "number_sources.yaml"
    entries = yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None
    for e in entries or []:
        assert e.get("source"), f"tests/number_sources.yaml: {e} needs a source"
    return {(e["file"], e["number"]) for e in entries or []}


INTS, SCALED = _known()
LISTED = _listed()


@pytest.mark.parametrize("name", PUBLIC)
def test_every_number_is_traceable(name):
    text, untraced = _text(ROOT / name), []
    for m in TOKEN.finditer(text):
        raw, unit = m.group(1), m.group(2)
        value = float(raw.replace(",", ""))
        if unit is None:
            if "," not in raw or round(value) in INTS:
                continue                       # bare small numbers (years, articles, ages) are not checked
        elif value in SCALED[UNIT[unit]] or ("," in raw and round(value) in INTS):
            continue
        if (name, m.group(0).strip()) in LISTED:
            continue
        around = text[max(0, m.start() - 50): m.end() + 20].replace("\n", " ")
        untraced.append(f"{m.group(0).strip()!r} in …{around}…")
    assert not untraced, (f"{len(untraced)} number(s) in {name} are not in outputs/ or parameters/ and not listed in "
                          "tests/number_sources.yaml:\n  " + "\n  ".join(untraced))
