"""The open questions page names the list's columns and status words in Japanese from its own key.

site/questions.html reads the Japanese words from the spans marked data-head and data-status in the key
「一覧の読み方」, and counts the rows whose status begins with "open". These checks keep the key and
OPEN_QUESTIONS.md in step, so every column head and every status cell gets its Japanese word.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE = (ROOT / "site/questions.html").read_text(encoding="utf-8")
LIST = (ROOT / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
STATUS = re.compile(r"^(answered in part|answered|open|decided|rule found)\b")


def _rows():
    return [[c.strip() for c in line.strip().strip("|").split("|")] for line in LIST.splitlines() if re.match(r"\|\s*Q\d+\s*\|", line)]


def test_every_column_head_has_a_japanese_word_in_the_key():
    head = next(line for line in LIST.splitlines() if line.startswith("| ID"))
    assert {c.strip() for c in head.strip().strip("|").split("|")} == set(re.findall(r'data-head="([^"]+)"', PAGE))


def test_every_status_word_has_a_japanese_word_in_the_key():
    assert set(re.findall(r'data-status="([^"]+)"', PAGE)) == {"open", "answered", "answered in part", "decided", "rule found"}


def test_every_status_cell_begins_with_a_known_word():
    rows = _rows()
    assert rows
    assert [r[0] for r in rows if not STATUS.match(r[-1])] == []


def test_report_title_carries_the_edition_the_pages_read():
    # Checks, Sources and Open questions read the edition from the first line of the built report (data-edition)
    ja = (ROOT / "outputs" / "report.ja.md").read_text(encoding="utf-8").split("\n")[0]
    en = (ROOT / "outputs" / "report.en.md").read_text(encoding="utf-8").split("\n")[0]
    assert re.search(r"\d+年\d+月版", ja) and re.search(r"\w+ \d{4} edition", en)
