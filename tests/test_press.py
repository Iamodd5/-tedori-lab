"""Milestone 11 press kit (scripts/build_press.py, press/summary.ja.md): every number comes from outputs/."""
import pathlib
import re

from scripts import build_press as bp
from tests.test_report import ALLOWED

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_summary_template_has_no_numbers_of_its_own():
    text = re.sub(r"\{\w+\}", "", (ROOT / "press" / "summary.ja.md").read_text(encoding="utf-8"))
    text = re.sub(r"H[1-8](?!\d)|図[1-3]|https?://\S+", "", text)  # household ids, figure numbers and the site address
    assert set(re.findall(r"\d+", text)) <= ALLOWED


def test_press_kit_is_current():
    # after an intended change, run `make outputs`
    for name, content in bp.render().items():
        assert (ROOT / "outputs" / "press" / name).read_text(encoding="utf-8") == content, name
