"""docs/VALIDATION.md is shown on the website, so the numbers it copies from outputs/ must match them (CLAUDE.md rule 7)."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = (ROOT / "docs" / "VALIDATION.md").read_text(encoding="utf-8")


def section(n):
    return DOC.split(f"\n## {n}. ")[1].split("\n## ")[0]


def table_ints(text):
    rows = "\n".join(l for l in text.splitlines() if l.startswith("|"))
    return {int(x.replace(",", "")) for x in re.findall(r"\d{1,3}(?:,\d{3})+", rows)}


def test_openfisca_table_matches_output():
    rows = json.loads((ROOT / "outputs" / "openfisca_check.json").read_text())["rows"]
    want = [f"| {r['household']} | {r['person']} | " + " | ".join(
        f"{v:,}" for v in [r["salary"], *(r[k][who] for k in ("social_insurance", "income_tax", "resident_tax")
                                          for who in ("ours", "openfisca"))]) + " |" for r in rows]
    assert [l for l in section(3).splitlines() if re.match(r"\| H\d", l)] == want


def test_calibration_tables_match_output():
    cal = json.loads((ROOT / "outputs" / "population.json").read_text())["calibration"]
    found = set()

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, (int, float)):
            found.add(round(x))
    walk(cal)
    found |= {sum(b["model"] for b in cal["wage_earners"]), sum(b["official"] for b in cal["wage_earners"])}
    assert table_ints(section(10)) <= found
