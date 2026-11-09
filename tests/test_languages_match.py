"""The Japanese and English versions of a text must carry the same numbers.

A fix made in one language and not the other shows up here. Amounts are compared as values, so 130万円
and ¥1.3m count as the same number, and 7割 as 70%.
"""
import pathlib
import re
from collections import Counter

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
MULT = {"兆": 1e12, "億": 1e8, "万": 1e4, "trillion": 1e12, "billion": 1e9, "bn": 1e9, "million": 1e6, "m": 1e6}
JA = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(兆|億|万)?(?:(\d)千)?\s*(割|%)?")
EN = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(trillion|billion|bn|million|m(?![a-z]))?\s*(%)?")
# Differences that are correct, each with the reason: {(file, value): reason}
EXPECTED_DIFFERENCES = {}


def _clean(text):
    return re.sub(r"https?://\S+|\]\([^)]*\)|`[^`]*`", " ", text)


def ja_values(text):
    out = Counter()
    for m in JA.finditer(_clean(text)):
        raw, unit, thousands, pct = m.groups()
        v = float(raw.replace(",", "")) * MULT.get(unit, 1) + (int(thousands) * 1000 if thousands else 0)
        if pct == "割":
            v, pct = v * 10, "%"
        if "," not in raw and unit is None and pct is None:
            continue
        out[round(v, 6)] += 1
    return out


def en_values(text):
    out = Counter()
    for m in EN.finditer(_clean(text)):
        raw, unit, pct = m.groups()
        if "," not in raw and unit is None and pct is None:
            continue
        out[round(float(raw.replace(",", "")) * MULT.get(unit, 1), 6)] += 1
    return out


def _strings(o, lang):
    if isinstance(o, dict):
        if {"ja", "en"} <= set(o) and isinstance(o["ja"], str):
            yield o[lang]
        else:
            for v in o.values():
                yield from _strings(v, lang)
    elif isinstance(o, list):
        for v in o:
            yield from _strings(v, lang)


PAIRS = [("report/report.ja.md", "report/report.en.md"), ("docs/METHODS.ja.md", "docs/METHODS.md")]
YAMLS = sorted(str(p.relative_to(ROOT)) for p in list(ROOT.glob("households/*.yaml")) + list(ROOT.glob("parameters/designs/*.yaml")))


def _check(name, ja, en):
    only_ja = {v: n for v, n in (ja - en).items() if (name, v) not in EXPECTED_DIFFERENCES}
    only_en = {v: n for v, n in (en - ja).items() if (name, v) not in EXPECTED_DIFFERENCES}
    assert not only_ja and not only_en, f"{name}: only in Japanese {only_ja}; only in English {only_en}"


@pytest.mark.parametrize("ja_file, en_file", PAIRS)
def test_document_pairs_carry_the_same_numbers(ja_file, en_file):
    _check(ja_file, ja_values((ROOT / ja_file).read_text(encoding="utf-8")), en_values((ROOT / en_file).read_text(encoding="utf-8")))


@pytest.mark.parametrize("name", YAMLS)
def test_bilingual_fields_carry_the_same_numbers(name):
    y = yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))
    _check(name, ja_values("\n".join(_strings(y, "ja"))), en_values("\n".join(_strings(y, "en"))))
