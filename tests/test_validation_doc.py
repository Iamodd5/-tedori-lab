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


def test_checks_page_directions_match_the_signs():
    # site/validation.html, "All-household estimate vs official figures": each direction word, from its sign
    # numbers are filled in at page load, so the empty spans are dropped and spaces closed up
    page = " ".join(re.sub(r"<[^>]+>", "", (ROOT / "site" / "validation.html").read_text(encoding="utf-8")).split())
    cal = json.loads((ROOT / "outputs" / "population.json").read_text())["calibration"]
    band = {b["band"]: b for b in cal["wage_earners"]}
    official = lambda b: b["official"] + b["official_part_year"]
    top = [b for k, b in band.items() if k in ("1,500万円以下", "2,000万円以下", "2,500万円以下", "2,500万円超")]
    mid = [band["200万円以下"], band["300万円以下"]]
    assert cal["households"]["model"] < cal["households"]["official_kiso_2025"] and "household count is below the official one" in page and "世帯数は公式より少なめ" in page
    assert cal["income_tax"]["model_baseline_2026"] < cal["income_tax"]["survey_estimate_2024"] and "Total income tax is lower" in page and "推計した税額より低め" in page
    assert cal["resident_tax"]["model_baseline_2026"] < cal["resident_tax"]["survey_estimate_2024"] and "resident tax lower than" in page
    assert sum(b["model"] for b in mid) > sum(map(official, mid)) and "far more than the official" in page and "公式の約を大きく上回" in page
    assert sum(b["model"] for b in top) < sum(map(official, top)) and "too few people earning ¥10m or more" in page and "1,000万円以上の人は少なすぎ" in page
    assert cal["people_65_plus"]["model"] < cal["people_65_plus"]["survey"] and "too few people aged 65 or over" in page and "65歳以上の人は少なめ" in page


def test_likely_bigger_net_gain_rests_on_both_gap_signs():
    # rule 13: "the net gain is likely bigger" (report, press, All households, Checks) follows only while both gaps hold:
    # too many earners at ¥1m–3m (more cash paid out) and too few at ¥10m+ (less extra income tax)
    cal = json.loads((ROOT / "outputs" / "population.json").read_text())["calibration"]
    band = {b["band"]: b for b in cal["wage_earners"]}
    official = lambda b: b["official"] + b["official_part_year"]
    mid = [band["200万円以下"], band["300万円以下"]]
    top = [b for k, b in band.items() if k in ("1,500万円以下", "2,000万円以下", "2,500万円以下", "2,500万円超")]
    assert sum(b["model"] for b in mid) > sum(map(official, mid))
    assert sum(b["model"] for b in top) < sum(map(official, top))
    for f, words in (("report/report.ja.md", "大きい可能性が高い"), ("report/report.en.md", "more likely"), ("press/summary.ja.md", "大きい可能性が高い"),
                     ("site/population.html", "大きい可能性が高い"), ("site/validation.html", "大きい可能性が高い")):
        assert words in (ROOT / f).read_text(encoding="utf-8"), f"{f}: the sentence this test backs has changed; check it again"
