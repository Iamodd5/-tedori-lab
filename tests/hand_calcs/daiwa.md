# Daiwa headline variant — hand calculations (H1, H3, H7)

Rule (parameters/designs/daiwa.yaml): income-tax basic deduction becomes 0; every taxpayer gets a 56,500-yen tax
credit. Credit left over after income tax is paid in cash, but only up to the person's social insurance on labour
income (employee health + pension; NHI + national pension for the self-employed). Resident tax unchanged.

Rate table (parameters/baseline_2026/income_tax.yaml): 5% up to 1,950,000; 10% − 97,500 up to 3,300,000.
The credit is taken off before the 2.1% reconstruction surtax, as tax credits are in the NTA example
(年末調整のしかた p.59). Daiwa does not say (OPEN_QUESTIONS Q11), so this order is an **approximation**.

Social insurance and incomes below are the baseline figures from H1.md, H3.md, H7.md.

## H1 (salary 1,250,000)
- Taxable: 510,000 − 0 − 183,348 = 326,652 → 326,000 × 5% = 16,300.
- 16,300 − 56,500 < 0 → income tax **0** (baseline 0). Unused credit 56,500 − 16,300 = 40,200.
- Cap: health 61,464 + pension 114,192 = 175,656 ≥ 40,200 → cash refund **40,200**.
- Disposable income change **+40,200**.

## H3 (salaries 4,500,000 and 3,000,000)
- Head: 3,160,000 − 0 − 669,564 = 2,490,436 → 2,490,000 × 10% − 97,500 = 151,500. 151,500 − 56,500 = 95,000
  × 1.021 = 96,995 → **96,900** (baseline 74,000, change +22,900). No unused credit.
- Spouse: 2,020,000 − 0 − 457,728 = 1,562,272 → 1,562,000 × 5% = 78,100. 78,100 − 56,500 = 21,600 × 1.021
  = 22,053.6 → **22,000** (baseline 26,600, change −4,600). No unused credit.
- Children: no income, no tax.
- Disposable income change −22,900 + 4,600 = **−18,300**.

## H7 (business income 3,000,000)
- 3,000,000 − 0 − 554,019 = 2,445,981 → 2,445,000 × 10% − 97,500 = 147,000. 147,000 − 56,500 = 90,500
  × 1.021 = 92,400.5 → **92,400** (baseline 71,700, change +20,700).
- Disposable income change **−20,700**.
