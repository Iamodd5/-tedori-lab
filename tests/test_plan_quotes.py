"""Every sentence that describes a plan must be backed by an exact quote from the plan's own document.

Each design file's `summary` and `short` texts are split into sentences. Each sentence must appear in a
`quotes` entry's `claim` (ja or en), and each entry's `text` must appear, exactly, on the cited page of the
saved source (sources/text/, built by `make text`). Sentences that state no fact about the plan (for example
how this site calculates it) go in `own_words` with the reason. A reader can then compare each claim with its
quote, and a paraphrase that drifts from the source is easy to see.

    quotes:
      - claim: {ja: "…one sentence copied from summary.ja…", en: "…the same sentence from summary.en…"}
        text: "…the exact words in the source…"
        source: outline          # a key under `source:`
        page: 9                  # PDF page as in sources/text (=== page N ===)
    own_words:
      - {ja: "…", en: "…", reason: "how this site calculates the plan"}
"""
import pathlib
import re

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGNS = [p for p in sorted((ROOT / "parameters" / "designs").glob("*.yaml")) if p.stem != "custom_template"]
SPLIT = {"ja": re.compile(r"(?<=。)"), "en": re.compile(r"(?<=[.!?])\s+(?=[A-Z(¥])")}


def norm(s):
    return re.sub(r"\s+", "", s)


def sentences(text, lang):
    return [s.strip() for s in SPLIT[lang].split(text) if s.strip()]


def page_text(design, source_key, page):
    src = design["source"][source_key]
    # scripts/pdf_to_text.py names each file by its folders and stem: sources/gov/x.pdf -> sources/text/gov_x.txt
    txt = ROOT / "sources" / "text" / ("_".join(pathlib.Path(src["file"]).relative_to("sources").with_suffix("").parts) + ".txt")
    if not txt.exists():
        pytest.skip(f"{txt.relative_to(ROOT)} not built (run `make text`)")
    pages = re.split(r"=== page (\d+) ===", txt.read_text(encoding="utf-8"))
    by_page = {int(pages[i]): pages[i + 1] for i in range(1, len(pages) - 1, 2)}
    return by_page.get(page, txt.read_text(encoding="utf-8") if len(by_page) == 0 else "")


@pytest.mark.parametrize("path", DESIGNS, ids=lambda p: p.stem)
def test_every_plan_sentence_is_backed_by_a_quote(path):
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    covered = {"ja": set(), "en": set()}
    for q in d.get("quotes", []):
        for lang in ("ja", "en"):
            covered[lang].add(norm(q["claim"][lang]))
    for w in d.get("own_words", []):
        assert w.get("reason"), f"{path.name}: own_words entry needs a reason"
        for lang in ("ja", "en"):
            covered[lang].add(norm(w[lang]))
    missing = []
    for field in ("short", "summary"):
        for lang in ("ja", "en"):
            for s in sentences((d.get(field) or {}).get(lang, ""), lang):
                if not any(norm(s) == c or norm(s) in c for c in covered[lang]):
                    missing.append(f"{field}.{lang}: {s}")
    assert not missing, f"{path.name}: {len(missing)} sentence(s) without a quote or an own_words reason:\n  " + "\n  ".join(missing)


@pytest.mark.parametrize("path", DESIGNS, ids=lambda p: p.stem)
def test_every_quote_is_in_its_source(path):
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    for q in d.get("quotes", []):
        assert q["source"] in d["source"], f"{path.name}: unknown source {q['source']}"
        for lang in ("ja", "en"):
            text = (d.get("summary") or {}).get(lang, "") + (d.get("short") or {}).get(lang, "")
            assert norm(q["claim"][lang]) in norm(text), f"{path.name}: claim not in short/summary.{lang}: {q['claim'][lang]}"
        assert norm(q["text"]) in norm(page_text(d, q["source"], q["page"])), \
            f"{path.name}: quote not found on {q['source']} p.{q['page']}: {q['text']}"
