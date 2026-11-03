# Resident-tax spouse deduction by the earner's income (令和9年度), and the ¥620,000 spouse limit

Law: 地方税法 as in force from 2027-01-01 (sources/law/chihozeiho_20270101.xml).
- 314条の2第1項第10号: spouse deduction 330,000 (elderly 380,000) when the earner's total income is ≤ 9,000,000;
  220,000 (260,000) above 9,000,000 up to 9,500,000; 110,000 (130,000) above 9,500,000 up to 10,000,000.
- 第10号の2: the spouse special deduction is the ≤ 9,000,000 amount for the spouse's band, then 2/3 of it
  (9.0m–9.5m) or 1/3 of it (9.5m–10m), "一万円未満の端数がある場合には、これを切り上げた金額".
- 314条の6第1号イ表(6): the 調整控除 difference for a spouse is 50,000 (elderly 100,000), or 40,000 (60,000) and
  20,000 (30,000) in the two higher bands. Row (7), for the spouse special deduction, applies only to a spouse with
  total income under 550,000. From 令和9年度 such a spouse is already a 控除対象配偶者 (limit 620,000, 292条1項), so the
  spouse special deduction never has a difference.

## Deduction and difference (earner total income, spouse total income)
| Earner | Spouse | Deduction | Difference | Why |
|---|---|---|---|---|
| 8,000,000 | 0 | 330,000 | 50,000 | 第10号イ |
| 9,050,000 | 0 | 220,000 | 40,000 | 第10号ロ |
| 9,550,000 | 0, aged 72 | 130,000 | 30,000 | 第10号ハ (elderly) |
| 8,000,000 | 1,200,000 | 160,000 | 0 | band 1,150,001–1,200,000 → 160,000 |
| 9,050,000 | 1,200,000 | 110,000 | 0 | 160,000 × 2/3 = 106,666.7 → round up to 10,000 |
| 9,550,000 | 1,200,000 | 60,000 | 0 | 160,000 × 1/3 = 53,333.3 → 60,000 |
| 10,050,000 | 0 | 0 | 0 | earner above 10,000,000 |

## A couple where only one partner earns, against the same person single
Salary 11,000,000 → employment income 11,000,000 − 1,950,000 = 9,050,000 (no child, so no income-adjustment deduction).
Taxable income is far above 2,000,000, so the 調整控除 is 5% of the 50,000 floor for both (max(差 − (taxable − 2m), 50,000)),
and the spouse changes only the deduction: resident tax is lower by 10% of it, each tax rounded on its own
(220,000 × 6% = 13,200 and × 4% = 8,800, both whole hundreds).
- Salary 10,500,000 (income 8,550,000): 33,000 lower.
- Salary 11,000,000 (income 9,050,000): **22,000** lower (the engine gave 33,000 before this file: OPEN_QUESTIONS Q37).
- Salary 11,500,000 (income 9,550,000): **11,000** lower.
