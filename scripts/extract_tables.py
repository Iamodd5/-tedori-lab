"""Build the baseline lookup tables in parameters/baseline_2026/ from the downloaded official PDFs.

1. kyuyo_shotoku_table_r8.csv: 令和8年分の年末調整等のための給与所得控除後の給与等の金額の表
   (NTA, 令和8年分 年末調整のしかた pp.47-54) -> salary_from, salary_to (exclusive), employment_income
2. kyoukaikenpo_tokyo_r8.csv: 協会けんぽ 東京支部 令和8年3月分からの保険料額表 -> grade, standard_monthly,
   from, to (exclusive), employee-half premiums for health (no LTC), health incl. LTC, child-support levy, pension
Run: .venv/bin/python -I scripts/extract_tables.py
"""
import csv
import pathlib
import re

from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "parameters" / "baseline_2026"
num = lambda s: int(s.replace(",", ""))


def kyuyo_table():
    reader = PdfReader(ROOT / "sources/tax/nta_nencho2026_all.pdf")
    rows = []
    for page in reader.pages[46:54]:  # printed pages 47-54
        # the PDF sometimes glues two numbers ("4,734,4006,312,000"); split after each ",ddd" group
        text = re.sub(r"(,\d{3})(?=\d)", r"\1 ", page.extract_text() or "")
        vals = [num(v) for v in re.findall(r"\d{1,3}(?:,\d{3})+", text)]
        # rows are (from, to, amount) with to - from = 1,000-4,000 yen and amount < from; scan for such triples
        i = 0
        while i + 2 < len(vals):
            a, b, c = vals[i:i + 3]
            if 2_191_000 <= a < b <= 6_600_000 and b - a <= 4000 and c < a:
                rows.append((a, b, c))
                i += 3
            else:
                i += 1
    rows = sorted(set(rows))
    # the printed table gives a formula below 2,191,000 (salary - 740,000; nothing below 741,000), handled in code
    # sanity: contiguous bands from the first row up to 6,600,000
    for (a, b, _), (c, _, _) in zip(rows, rows[1:]):
        assert b == c, f"gap or overlap in kyuyo table at {b} -> {c}"
    assert rows[-1][1] == 6_600_000, rows[-1]
    with open(OUT / "kyuyo_shotoku_table_r8.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["salary_from", "salary_to_exclusive", "employment_income"])
        w.writerows(rows)
    return len(rows), rows[0], rows[-1]


def kyoukai_table():
    text = PdfReader(ROOT / "sources/social/kyoukaikenpo_R8_13tokyo.pdf").pages[0].extract_text()
    rows = []
    for line in text.splitlines():
        m = re.match(r"^(\d+)(?:\(\d+\))? ([\d,]+) ([\d,]*) ?～ ?([\d,]*) (.*)$", line)
        if not m:
            continue
        grade, std, lo, hi, rest = m.groups()
        nums = [float(x.replace(",", "")) for x in rest.split()]
        # columns: health full, half, health+LTC full, half, child levy full, half, [pension full, half]
        pension_half = nums[7] if len(nums) >= 8 else None
        rows.append([int(grade), num(std), num(lo) if lo else 0, num(hi) if hi else "", nums[1], nums[3], nums[5], pension_half])
    assert [r[0] for r in rows] == list(range(1, 51)), "expected grades 1-50"
    with open(OUT / "kyoukaikenpo_tokyo_r8.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["grade", "standard_monthly", "from", "to_exclusive", "health_half", "health_ltc_half", "child_levy_half", "pension_half"])
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print("kyuyo rows:", kyuyo_table())
    print("kyoukai grades:", kyoukai_table())
