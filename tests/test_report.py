"""Milestone 9 report (scripts/build_report.py, report/*.md). Lead finding from tests/hand_calcs/wall_H4.md."""
import json
import pathlib
import re

from scripts import build_report as br

ROOT = pathlib.Path(__file__).resolve().parents[1]
# numbers the templates may contain themselves: years, the edition month (2026年11月), household ids,
# and the ten income groups (structure, not data)
ALLOWED = {"2024", "2025", "2026", "11", "10"}


def test_lead_finding_matches_hand_calc():
    pts = json.loads((ROOT / "outputs" / "wall_map.json").read_text())["households"]["H4"]["designs"]["baseline"]
    lead = max(br.walls(pts), key=lambda w: w["drop"])
    assert lead == {"from": 1_290_000, "at": 1_300_000, "drop": 258_226, "back": 1_640_000}


def test_templates_have_no_numbers_of_their_own():
    for lang in br.LANGS:
        text = re.sub(r"\{\w+\}", "", (ROOT / "report" / f"report.{lang}.md").read_text(encoding="utf-8"))
        text = re.sub(r"H[1-8](?!\d)", "", text)
        assert set(re.findall(r"\d+", text)) <= ALLOWED, lang


def test_report_is_current():
    # after an intended change, run `make outputs` and explain it in docs/LOG.md
    for lang, text in br.render().items():
        assert (ROOT / "outputs" / f"report.{lang}.md").read_text(encoding="utf-8") == text, lang
