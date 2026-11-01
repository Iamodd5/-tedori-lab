"""Population view (SPEC 9.3, 9.4): model households built from the 2024 survey cells, run through every design,
then grouped into income deciles. Inputs: population/*.csv (scripts/extract_population.py) and population/population.yaml.
Hand calculation: tests/hand_calcs/population.md."""
import csv
import functools
import pathlib

import yaml

from engine import household as h
from engine import reforms as r

P = pathlib.Path(__file__).resolve().parents[1] / "population"


@functools.cache
def config():
    return yaml.safe_load((P / "population.yaml").read_text(encoding="utf-8"))


def _read(name):
    return [{k: (v if k in ("group", "band", "kind", "source_band", "name", "source") else float(v) if v else None)
             for k, v in row.items()} for row in csv.DictReader(open(P / name, encoding="utf-8"))]


@functools.cache
def _cells():
    return _read("cells.csv")


def cells():
    return [dict(c) for c in _cells()]


@functools.cache
def food():
    return {(f["kind"], f["band"]): f["food8_monthly"] for f in _read("food.csv")}


def checks():
    return {c["name"]: c["value"] for c in _read("checks.csv")}


def _share(total, weights):
    s = sum(weights)
    return [total * w / s for w in weights] if s else [total] + [0] * (len(weights) - 1)


def model_households(cell):
    """One cell -> a pension household and/or a work household, with weights adding up to the cell's households."""
    g, a = config()["groups"][cell["group"]], config()["assumptions"]
    old_age, child_age, adult_child_age = (a[k]["value"] for k in ("older_age", "child_age", "adult_child_age"))
    adults = 2 if g["spouse"] else 1
    wh, ws, bus = cell["wage_head"], cell["wage_spouse"], cell["business"]
    ph, ps = cell["pension_head"], cell["pension_spouse"]
    if not g["spouse"]:  # no spouse in the model: their (small) amounts go to the head
        wh, ws, ph, ps = wh + ws, 0, ph + ps, 0

    kids = round(cell["under18"])
    n_child = {"from_size": max(1, round(cell["persons"]) - 1), "under18_only": kids}.get(g["children"], g["children"])
    kids = min(kids, n_child)
    adult_children = 0 if g.get("relatives") else n_child - kids
    relatives = max(0, round(cell["persons"]) - adults - kids) if g.get("relatives") else 0
    relatives_old = relatives > 0 and cell["pension_other"] >= cell["wage_other"]

    # assumption income_split: a pension household and a work household, each with the cell's total income
    work, pens = wh + ws + bus, ph + ps
    total = work + pens
    pi = pens / total if total else 0.0
    variants = []  # (name, share of the cell, age, spouse salary, pension)
    if pi > 0:
        variants.append(("pension", pi, old_age, 0.0, total))
    if pi < 1:
        age = min(64, max(20, round((cell["head_age"] - pi * old_age) / (1 - pi))))
        # assumption spouse_earnings: the survey's earners per household decide how many spouses earn
        others_earning = adult_children + relatives if cell["wage_other"] > 0 else 0
        q = min(1.0, max(0.0, (cell["earners"] - others_earning) / (1 - pi) - 1, ws / work if work else 0.0)) if ws > 0 else 0.0
        if q < 1:
            variants.append(("work_one_earner" if g["spouse"] else "work", (1 - pi) * (1 - q), age, 0.0, 0.0))
        if q > 0:
            variants.append(("work_two_earners", (1 - pi) * q, age, ws / ((1 - pi) * q), 0.0))

    takers = adult_children + relatives
    other_dropped = (cell["wage_other"] if not takers else 0) + (cell["pension_other"] if not relatives_old else 0)
    out = []
    for name, share, age, w_spouse, p in variants:
        w_head, b_head = _share(total - p - w_spouse, [wh, bus])
        p_head, p_spouse = _share(p, [ph, ps])
        members = [{"id": "a", "role": "head", "age": age, "salary": round(w_head), "business_income": round(b_head),
                    "public_pension": round(p_head)}]
        if g["spouse"]:
            members.append({"id": "b", "role": "spouse", "age": age, "salary": round(w_spouse), "public_pension": round(p_spouse)})
        members += [{"id": f"c{i}", "role": "child", "age": child_age} for i in range(kids)]
        members += [{"id": f"d{i}", "role": "child", "age": adult_child_age, "salary": round(cell["wage_other"] / takers)}
                    for i in range(adult_children)]
        members += [{"id": f"r{i}", "role": "dependant", "age": old_age if relatives_old else age,
                     "salary": round(cell["wage_other"] / takers),
                     "public_pension": round(cell["pension_other"] / relatives) if relatives_old else 0} for i in range(relatives)]
        for m in members:
            if m.get("salary"):
                m["work"] = {"hours_20_plus": True, "employer_51_plus": True}  # assumption `work`
        if g["children"] == "from_size":
            members[0]["single_parent"] = True
        kind = "single" if cell["group"] == "single" else "two_plus"
        out.append({"household": {"id": f"{cell['group']}-{cell['band']}-{name}", "members": members,
                                  "spending": {"status": "resolved", "food_annual": 12 * food()[(kind, cell["band"])]}},
                    "weight": cell["households"] * share, "cell": cell, "variant": name,
                    "dropped_other": other_dropped})
    return out


def build():
    return [m for c in cells() for m in model_households(c)]


def decile_pieces(items):
    """items: (key, income, weight). Returns (key, decile 1-10, weight) with households on a boundary split in proportion."""
    total = sum(w for _, _, w in items)
    size, lo, out = total / 10, 0.0, []
    for key, _, w in sorted(items, key=lambda x: x[1]):
        hi = lo + w
        for d in range(1, 11):
            overlap = min(hi, d * size) - max(lo, (d - 1) * size)
            if overlap > 1e-9 * total:
                out.append((key, d, overlap))
        lo = hi
    return out


NTA_BANDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]  # million yen, upper limits of 民間給与実態統計調査 第3表 bands


def results(designs):
    """Everything outputs/population.json needs: deciles, winners and losers, cost, and the calibration checks."""
    rows = []
    for m in build():
        hh = m["household"]
        base = h.compute(hh)
        rows.append({**m, "base": base, "runs": {d: r.run(d, hh) for d in designs}})
    pieces = decile_pieces([(i, x["cell"]["annual_income"], x["weight"]) for i, x in enumerate(rows)])
    deciles = []
    for d in range(1, 11):
        mine = [(rows[i], w) for i, dd, w in pieces if dd == d]
        n = sum(w for _, w in mine)
        deciles.append({"decile": d, "households": round(n),
                        "annual_income_mean": round(sum(x["cell"]["annual_income"] * w for x, w in mine) / n),
                        "annual_income_max": max(x["cell"]["annual_income"] for x, _ in mine),
                        "baseline_disposable_mean": round(sum(x["base"]["disposable"] * w for x, w in mine) / n)})
    out = {"deciles": deciles, "designs": {}}
    for d in designs:
        status = rows[0]["runs"][d]["status"]
        entry = {"label": r.design(d)["label"], "status": status,
                 "blocked_by": rows[0]["runs"][d]["blocked_by"], "approximations": rows[0]["runs"][d]["approximations"],
                 "published_estimates": r.design(d).get("published_estimates"), "site_note": r.design(d).get("site_note"),
                 "summary": r.design(d)["summary"]}
        if status == "complete":
            assert all(x["runs"][d]["status"] == "complete" for x in rows)
            by = []
            for k in range(1, 11):
                mine = [(rows[i]["runs"][d]["disposable_change"], w) for i, dd, w in pieces if dd == k]
                n = sum(w for _, w in mine)
                by.append({"decile": k, "mean_change": round(sum(c * w for c, w in mine) / n),
                           "winners_share": round(sum(w for c, w in mine if c > 0) / n, 4),
                           "losers_share": round(sum(w for c, w in mine if c < 0) / n, 4),
                           "unchanged_share": round(sum(w for c, w in mine if c == 0) / n, 4)})
            total = lambda f: round(sum(f(x) * x["weight"] for x in rows))
            entry["by_decile"] = by
            # cost to the government = total gain in take-home pay (static: no change in how people work)
            entry["cost_yen"] = total(lambda x: x["runs"][d]["disposable_change"])
            entry["cost_components_yen"] = {c: total(lambda x: x["runs"][d]["components"][c]) for c in r.COMPONENTS}
        out["designs"][d] = entry

    # calibration checks (SPEC 9.3): compare with official totals; gaps go to docs/VALIDATION.md
    chk = checks()
    cell_total = lambda f: round(sum(f(c) * c["households"] for c in cells()))
    persons = [(m.get("salary", 0), x["weight"]) for x in rows for m in x["household"]["members"]]
    official = [(k.removeprefix("wage_earners_upto_"), v) for k, v in chk.items() if k.startswith("wage_earners_upto_")]
    earners = []
    for (label, n), lo, top in zip(official, [0] + NTA_BANDS, NTA_BANDS + [None]):  # checks.csv keeps the table's order
        ours = sum(w for s, w in persons if s > lo * 1_000_000 and (top is None or s <= top * 1_000_000))
        earners.append({"band": label, "model": round(ours), "official": round(n)})
    member_total = lambda k: round(sum(o[k] * x["weight"] for x in rows for o in x["base"]["members"].values()))
    out["calibration"] = {
        "households": {"model": round(sum(x["weight"] for x in rows)), "suppressed_cells": round(chk["households_in_suppressed_cells"]),
                       "official_kiso_2025": round(chk["households_total"])},
        "wage_earners": earners,
        "people_65_plus": {"model": round(sum(x["weight"] for x in rows for m in x["household"]["members"] if m["age"] >= 65)),
                           "survey": cell_total(lambda c: c["over65"])},
        "income_tax": {"model_baseline_2026": member_total("income_tax"), "survey_estimate_2024": cell_total(lambda c: c["est_income_tax"])},
        "resident_tax": {"model_baseline_2026": member_total("resident_tax"), "survey_estimate_2024": cell_total(lambda c: c["est_resident_tax"])},
        "income_covered": {"modelled": cell_total(lambda c: c["wage_head"] + c["wage_spouse"] + c["wage_other"] + c["business"]
                                                  + c["pension_head"] + c["pension_spouse"] + c["pension_other"]),
                           "survey_annual_income": cell_total(lambda c: c["annual_income"]),
                           "dropped_other_members": round(sum(x["dropped_other"] * x["weight"] for x in rows))},
        "decile_upper_bounds": [{"decile": k["decile"], "model": k["annual_income_max"],
                                 "official": round(chk[f"decile_{k['decile']}_upper_annual_income"])} for k in deciles[:9]],
        "food8_monthly": {"survey_2024_oct_nov": round(chk["food8_monthly_all_households_2024_oct_nov"]),
                          "kakei_2025_full_year": round(chk["food8_monthly_all_households_2025_full_year"])},
    }
    out["households_csv_rows"] = [{"id": x["household"]["id"], "group": x["cell"]["group"], "band": x["cell"]["band"],
                                   "variant": x["variant"], "weight": round(x["weight"], 2),
                                   "annual_income": x["cell"]["annual_income"], "baseline_disposable": x["base"]["disposable"],
                                   **{f"change_{d}": x["runs"][d]["disposable_change"] for d in designs}} for x in rows]
    return out
