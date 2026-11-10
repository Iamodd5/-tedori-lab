"""Numbers listed in tests/number_sources.yaml that the engine or outputs/ produce, worked out again.

A listed number is not checked against outputs/ by tests/test_number_provenance.py, so each one that comes from
the engine is recomputed here; if the engine changes, these fail and the text must be updated.
"""
import json
import pathlib

from engine import household as h
from engine import population as p
from engine import wall_map as w

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = (ROOT / "docs" / "VALIDATION.md").read_text(encoding="utf-8")
CAL = json.loads((ROOT / "outputs" / "population.json").read_text())["calibration"]
million = lambda n: f"{n / 1e6:.2f} million"


def test_h2_deferral_ends_at_2196000():
    hh = h.load("H2")
    pension = lambda s: sum(o["national_pension"] for o in h.compute(w.at_income(hh, s))["members"].values())
    assert (pension(2_195_000), pension(2_196_000)) == (0, 215_040)
    assert "¥2,196,000" in json.dumps(h.load("H2"), ensure_ascii=False)


def test_openfisca_largest_resident_tax_gap():
    rows = json.loads((ROOT / "outputs" / "openfisca_check.json").read_text())["rows"]
    gaps = [r["resident_tax"]["openfisca"] - r["resident_tax"]["ours"] for r in rows if r["household"] != "H1"]
    assert f"OF-J is {min(gaps):,}–{max(gaps):,} yen higher" in DOC


def test_calibration_figures_in_the_text():
    band = {b["band"]: b for b in CAL["wage_earners"]}
    one_to_three = [band["200万円以下"], band["300万円以下"]]
    assert f"({million(sum(b['model'] for b in one_to_three))} against " \
           f"{million(sum(b['official'] + b['official_part_year'] for b in one_to_three))} including part-year" in DOC
    assert f"→ {million(sum(b['model'] for b in CAL['wage_earners']))} (the survey's own count" in DOC
    survey = sum((c["earners"] or 0) * c["households"] for c in p.cells())
    assert f"earners per household × households: {million(survey)})" in DOC
    assert f"gives a net of about {CAL['daiwa_net_scaled_to_official_earners'] / 1e12:.1f} trillion" in DOC


def test_q37_households_in_the_9m_to_10m_spouse_band():
    # OPEN_QUESTIONS Q37: higher earner's total income above 9m up to 10m, partner's total income at most 1,330,000
    n = 0
    for x in p.build():
        out = h.compute(x["household"])["members"]
        partners = sorted((out[m["id"]]["total_income"] for m in x["household"]["members"] if m["role"] in ("head", "spouse")), reverse=True)
        if len(partners) == 2 and 9_000_000 < partners[0] <= 10_000_000 and partners[1] <= 1_330_000:
            n += x["weight"]
    assert round(n, -3) == 185_000
    assert "about 185,000 all-household households (by weight)" in (ROOT / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
