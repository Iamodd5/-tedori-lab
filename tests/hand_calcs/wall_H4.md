# H4 wall map — the 1.3m wall (spouse salary 1,290,000 → 1,300,000)

Head: salary 5,000,000, age 45, employee; total income 3,560,000; employee premiums 762,984 (H4.md).
Spouse: age 43, works under 20 hours a week, so not in employee insurance (households/H4.yaml).

**At 1,290,000** the spouse earns under 1,300,000 → health-insurance dependant, category-3 pension member: no premiums.
Spouse total income 550,000. Spouse resident tax: 550,000 − 430,000 = 120,000 → 12,000 − 調整控除 2,500 = 9,500
+ per-capita 5,000 = **14,500**.

**At 1,300,000** the spouse is no longer a dependant (limit is "under 1.3m", social_insurance.yaml) → National
Health Insurance + national pension. Spouse total income 560,000.
- National pension: 17,920 × 12 = **215,040** (paid by the spouse).
- NHI (Shinjuku FY2026, age 40–64; base = 560,000 − 430,000 = 130,000). The reduction test counts the householder's
  income too ("世帯主と被保険者全員の前年中の総所得金額等", sources/shinjuku/hoken01_002030.html):
  3,560,000 + 560,000 = 4,120,000 is far above every limit → **no reduction**.
  medical 47,600 + 9,763 = 57,363; support 17,600 + 3,640 = 21,240; care 17,800 + 3,159 = 20,959;
  child levy 1,873 + 351 = 2,224 → **101,786** (billed to the householder, who also deducts it).
- Spouse resident tax: 560,000 − 430,000 − 215,040 < 0 → income levy 0; per-capita **5,000** (−9,500).

**Head's taxes.** Spouse income 550,000 / 560,000: income-tax spouse deduction 380,000 both times; resident-tax
spouse special deduction 330,000 both times (spouse income above 480,000).
- Income tax: 3,560,000 − 762,984 − 1,040,000 − 380,000 = 1,377,016 → 1,377,000 × 5% = 68,850 × 1.021 → **70,200**.
  With NHI: − 864,770 instead → 1,275,230 → 1,275,000 × 5% = 63,750 × 1.021 → **65,000** (−5,200).
- Resident tax: 3,560,000 − 762,984 − 430,000 − 330,000 = 2,037,016 → 2,037,000 × 10% = 203,700 − 2,500 + 5,000
  = **206,200**. With NHI: 1,935,230 → 1,935,000 → 193,500 − 2,500 + 5,000 = **196,000** (−10,200).

**Change in take-home pay** = +10,000 − 215,040 − 101,786 + 9,500 + 5,200 + 10,200 = **−281,926**.
Effective marginal rate = 1 + 291,926 / 10,000 = **29.1926** (2,919%).

## Correction 2026-11-01 (Milestone 5 review)

The resident-tax income limit for a spouse or dependant is **580,000** from 令和8年度, not 480,000
(MIC 個人住民税の基礎控除等について p.28, ④「改正前：48万円 → 改正後：58万円」). So at spouse income 550,000 and
560,000 the head takes the resident-tax **spouse deduction** (330,000, same amount) and the 調整控除 difference
for a spouse (50,000) is added:
- At 1,290,000: 2,037,000 × 10% = 203,700 − 5% × max(100,000 − 37,000, 50,000) = 3,150 → 200,550 → 200,500
  + 5,000 = **205,500** (was 206,200).
- At 1,300,000: 1,935,000 × 10% = 193,500 − 5% × min(100,000, 1,935,000) = 5,000 → 188,500 + 5,000 = **193,500**
  (was 196,000). Change −12,000 (was −10,200).

Corrected change in take-home pay = +10,000 − 215,040 − 101,786 + 9,500 + 5,200 + 12,000 = **−280,126**.
Effective marginal rate = 1 + 290,126 / 10,000 = **29.0126**.
