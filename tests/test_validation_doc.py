"""docs/VALIDATION.md is shown on the website, so the numbers it copies from outputs/ must match them (project rule 7)."""
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


def test_wall_map_section_matches_engine():
    # section 6, "Engine" column, worked out again from the engine
    from engine import household as h
    from engine import wall_map as w
    res = lambda hid, s: h.compute(w.at_income(h.load(hid), s))
    disp = lambda hid, s: res(hid, s)["disposable"]
    tax = lambda hid, s, k: sum(o[k] for o in res(hid, s)["members"].values())
    sgn = lambda n: ("+" if n > 0 else "−") + f"{abs(n):,}"
    h4 = next(c for c in w.wall_causes(h.load("H4"), [{"from": 1_290_000, "at": 1_300_000}]))["change"]
    step = disp("H4", 1_300_000) - disp("H4", 1_290_000)
    want = [f"marginal rate {(1 - (disp('H1', 1_120_000) - disp('H1', 1_110_000)) / 10_000) * 100:.2f}%",
            f"take-home {sgn(disp('H1', 1_060_000) - disp('H1', 1_050_000))}",
            f"resident tax {sgn(tax('H5', 2_100_000, 'resident_tax') - tax('H5', 2_090_000, 'resident_tax'))}",
            f"take-home {sgn(step)}; marginal rate {round((1 - step / 10_000) * 100):,}%",
            f"national pension {sgn(h4['national_pension'])}, NHI {sgn(h4['nhi'])}, income tax {sgn(h4['income_tax'])}, "
            f"resident tax {sgn(h4['resident_tax'])}",
            f"take-home {disp('H6', 1_700_000):,}"]
    engine_column = [l.split(" | ")[1] for l in section(6).splitlines() if l.startswith("| H")]
    assert engine_column == want


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
