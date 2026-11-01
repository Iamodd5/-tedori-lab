"""Build the population-view input tables in population/ from the official statistics in sources/stats/ (H-17: A).

1. cells.csv: households by group (population/population.yaml) and 年間収入 band, with the income sources, ages
   and the survey's own tax estimates, from 令和6年全国家計構造調査 所得 第3-32-1表. Amounts in yen per year.
2. food.csv: food at the 8% rate (食料 − 酒類 − 一般外食) and consumption, yen per month, by household kind and
   band, from 令和6年全国家計構造調査 家計収支 第1-21表. Bands of 10m yen and more use the survey's pooled bands
   (R1 10-12.5m, R2 12.5-15m, R3 15m+) because single-person cells there are small or suppressed.
3. checks.csv: official totals used only to check the result (docs/VALIDATION.md).
Run: .venv/bin/python -I scripts/extract_population.py
"""
import csv
import pathlib
import re
import xml.etree.ElementTree as ET
import zipfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
S = ROOT / "sources" / "stats"
OUT = ROOT / "population"
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def xlsx(path):
    """{sheet name: {row number: {column letter: text}}} using only the standard library."""
    z = zipfile.ZipFile(path)
    shared = [("".join(t.text or "" for t in si.iter(M + "t")))
              for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(M + "si")]
    names = [s.get("name") for s in ET.fromstring(z.read("xl/workbook.xml")).iter(M + "sheet")]
    out = {}
    for i, name in enumerate(names, 1):
        rows = {}
        for c in ET.fromstring(z.read(f"xl/worksheets/sheet{i}.xml")).iter(M + "c"):
            v = c.find(M + "v")
            if v is None:
                continue
            col, row = re.match(r"([A-Z]+)(\d+)", c.get("r")).groups()
            rows.setdefault(int(row), {})[col] = shared[int(v.text)] if c.get("t") == "s" else v.text
        out[name] = rows
    return out


def band_range(label):
    """'02_100～150万円' -> (1_000_000, 1_500_000); '40_2000万円以上' -> (20_000_000, None)."""
    nums = [int(n) * 10_000 for n in re.findall(r"\d+(?=[～万])", label.split("_", 1)[1])]
    if "未満" in label:
        return 0, nums[0]
    if "以上" in label:
        return nums[0], None
    return nums[0], nums[1]


BANDS = [f"{i:02d}" for i in range(1, 41)]
# item -> (column E label or column G code prefixes summed); amounts are 千円
INCOME_ITEMS = {
    "households": ["世帯数分布"], "sample": ["集計世帯数（概数）"], "persons": ["世帯人員"],
    "under18": ["18歳未満人員"], "over65": ["65歳以上人員"], "earners": ["有業人員"], "head_age": ["世帯主の年齢"],
    "annual_income": ["2"], "wage_head": ["21101"], "wage_spouse": ["21102"], "wage_other": ["21103"],
    "business": ["2121", "2122", "2124"], "rent": ["2123"],
    "pension_head": ["21401", "21601"], "pension_spouse": ["21402", "21602"], "pension_other": ["21403", "21603"],
    "est_income_tax": ["811"], "est_resident_tax": ["812"],
}
COUNTS = ("households", "sample")
PER_HOUSEHOLD_NOT_YEN = ("persons", "under18", "over65", "earners", "head_age")


def cells():
    rows = next(iter(xlsx(S / "zkk2024_shotoku_3-32-1.xlsx").values()))
    col = {v.split("_")[0]: k for k, v in rows[6].items() if len(k) > 1 or k >= "I"}
    table = {}  # (band, column code, item) -> value
    for r in rows.values():
        band = r.get("D", "")[:2]
        if band not in BANDS:
            continue
        key = r.get("E") if r.get("E") != "1世帯当たり年間収入額" else r.get("G", "").split("_")[0]
        for code, c in col.items():
            table[(band, code, key)] = r.get(c)
    groups = yaml.safe_load((OUT / "population.yaml").read_text(encoding="utf-8"))["groups"]
    out, suppressed = [], 0

    def value(band, code, item):
        parts = [table.get((band, code, k)) for k in INCOME_ITEMS[item]]
        if any(p == "X" or p is None for p in parts):
            return None
        return sum(0.0 if p == "-" else float(p) for p in parts)

    for gid, g in groups.items():
        for band in BANDS:
            terms = [(-1 if c.startswith("-") else 1, c.lstrip("-")) for c in g["columns"]]
            n = sum(s * (value(band, c, "households") or 0) for s, c in terms)
            if n <= 0:
                continue
            rec = {"group": gid, "band": band, "households": round(n)}
            rec["band_from"], rec["band_to"] = band_range(next(v for k, v in rows.items() if k > 7 and v.get("D", "").startswith(band + "_"))["D"])
            for item in INCOME_ITEMS:
                if item == "households":
                    continue
                vals = [(s, value(band, c, "households") or 0, value(band, c, item)) for s, c in terms]
                if any(v is None and w for _, w, v in vals):
                    rec = None  # the survey hides this cell (too few households sampled)
                    break
                if item in COUNTS:
                    rec[item] = round(sum(s * (v or 0) for s, _, v in vals))
                    continue
                mean = sum(s * w * (v or 0) for s, w, v in vals) / n
                # the "other" group is a difference of columns, so a small item can come out slightly below zero
                rec[item] = mean if item in PER_HOUSEHOLD_NOT_YEN else max(0, round(mean * 1000))
            if rec is None:
                suppressed += round(n)
                continue
            out.append(rec)
    fields = ["group", "band", "band_from", "band_to", "households"] + [k for k in INCOME_ITEMS if k != "households"]
    with open(OUT / "cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for rec in out:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in rec.items()})
    return len(out), sum(r["households"] for r in out), suppressed


def food():
    rows = next(iter(xlsx(S / "zkk2024_kakei_1-21.xlsx").values()))
    header = rows[7]
    band_col = {v.split("_")[0]: k for k, v in header.items() if (len(k) > 1 or k >= "M") and re.match(r"(\d\d|R\d)_.*万円", v)}
    pooled = lambda b: "R1" if 20 <= int(b) <= 24 else "R2" if 25 <= int(b) <= 29 else "R3" if int(b) >= 30 else b
    out = []
    for kind, label in (("two_plus", "1_二人以上の世帯"), ("single", "2_単身世帯")):
        sel = {r.get("I") if r.get("I") != "1世帯当たり1か月間の収入と支出" else r.get("K").split("_")[0]: r
               for r in rows.values() if r.get("D") == label and r.get("F") == "0_全世帯" and r.get("H") == "0_平均"}
        for band in BANDS:
            c = band_col[pooled(band)]
            get = lambda k: float(sel[k][c])
            out.append({"kind": kind, "band": band, "source_band": pooled(band), "sample": int(get("集計世帯数（概数）")),
                        "food8_monthly": round(get("210101") - get("21010111") - get("210101121")),
                        "consumption_monthly": round(get("2101"))})
    with open(OUT / "food.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(out[0]))
        w.writeheader()
        w.writerows(out)
    # national average, kept for the seasonality check against 家計調査 2025
    avg = {r.get("I") if r.get("I") != "1世帯当たり1か月間の収入と支出" else r.get("K").split("_")[0]: r
           for r in rows.values() if r.get("D") == "0_総世帯" and r.get("F") == "0_全世帯" and r.get("H") == "0_平均"}
    m = next(k for k, v in header.items() if v == "00_平均")
    deciles = [k for k, v in header.items() if re.match(r"0\d_十分位\d$", v)]  # deciles 1-9 have an upper bound
    return (round(float(avg["210101"][m]) - float(avg["21010111"][m]) - float(avg["210101121"][m])),
            [int(float(avg["各分位の境界値（分位の上限・万円）"][c])) * 10_000 for c in deciles])


def checks(zkk_food8, zkk_decile_bounds, suppressed):
    out = []
    add = lambda name, value, source: out.append({"name": name, "value": value, "source": source})
    # 国民生活基礎調査 2025 世帯票 第2表: the 2025 row of the 推計数 (千世帯) block
    text = (S / "kiso2025_setai_2.csv").read_bytes().decode("cp932")
    block = text.split("推計数")[1]
    row = next(line for line in block.splitlines() if line.startswith("2025"))
    add("households_total", int(row.split(",")[1]) * 1000, "kiso_2025")
    add("households_in_suppressed_cells", suppressed, "zkk_income")
    # 民間給与実態統計調査 令和7年分 第3表 その1: full-year private-sector earners by pay band, men + women
    sheet = xlsx(S / "minkan_r7_3.xlsx")["03_01"]
    bands = {}
    for r in sheet.values():
        if r.get("B") == "１年を通じて勤務した給与所得者" and r.get("C", "")[:1] in ("男", "女") and r.get("A") != "計":
            bands[r["A"]] = bands.get(r["A"], 0) + int(float(r["F"]))
    for label, n in bands.items():
        add(f"wage_earners_upto_{label}", n, "minkan_r7")
    kakei = xlsx(S / "kakei2025_sosetai_3.xlsx")["総"].values()
    get = lambda name: float(next(r for r in kakei if (r.get("L") or "").strip() == name)["N"])  # first match: 用途分類
    add("food8_monthly_all_households_2025_full_year", round(get("食料") - get("酒類") - get("一般外食")), "kakei_2025")
    add("food8_monthly_all_households_2024_oct_nov", zkk_food8, "zkk_spending")
    for i, v in enumerate(zkk_decile_bounds, 1):
        add(f"decile_{i}_upper_annual_income", v, "zkk_spending")
    with open(OUT / "checks.csv", "w", newline="") as f:
        w = csv.DictWriter(f, ["name", "value", "source"])
        w.writeheader()
        w.writerows(out)
    return len(out)


if __name__ == "__main__":
    n, households, suppressed = cells()
    print("population cells:", n, "households:", households, "in suppressed cells:", suppressed)
    f8, bounds = food()
    print("food rows written; all-household food at 8%:", f8, "yen/month")
    print("check values:", checks(f8, bounds, suppressed))
