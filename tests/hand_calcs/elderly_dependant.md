# Dependants aged 70 and over (老人扶養親族, 同居老親等)

Rules:
- Income tax, 令和8年分: NTA 年末調整のしかた (sources/tax/nta_nencho2026_all.pdf) p.56 「令和8年分の扶養控除額等の表」:
  general 380,000; 老人扶養親族 not living together 480,000; 同居老親等 580,000. p.12: a 同居老親等 is a 老人扶養親族 who is a
  lineal ascendant (parent, grandparent) of the taxpayer or the spouse and normally lives with either of them.
  老人扶養親族 = a dependant aged 70 or over (所得税法2条1項34号の4).
- Resident tax, 令和9年度 (sources/law/chihozeiho_20270101.xml): 314条の2第1項第11号 general 330,000, 老人扶養親族 (70 or over)
  380,000; 第4項 a 同居直系尊属 450,000. 調整控除 differences, 314条の6第1号イ表: (8)(i) general 50,000,
  (8)(iii) 老人扶養親族 100,000, (9) 同居直系尊属 130,000.

## One earner with one dependant who has no income
Head aged 45, salary 11,000,000 (employee). The dependant has no income, so the head claims them.
- Salary income: 11,000,000 − 1,950,000 = 9,050,000. No dependant under 23, so no income adjustment.
- Social insurance (employee premiums, tested elsewhere): 640,020 + 12,828 + 713,700 + 54,996 = 1,421,544.
- Basic deduction (income tax), income 6,550,001–23,500,000: 620,000.

Income tax = taxable income rounded down to 1,000 × 20% − 427,500; plus 2.1% (yen rounded down); total rounded down to 100.

| Dependant | Deduction | Deductions in all | Taxable | Tax | + 2.1% | Income tax |
|---|---|---|---|---|---|---|
| aged 40 | 380,000 | 2,421,544 | 6,628,000 | 898,100 | 18,860 | **916,900** |
| aged 75, not a parent | 480,000 | 2,521,544 | 6,528,000 | 878,100 | 18,440 | **896,500** |
| aged 75, a parent living with them | 580,000 | 2,621,544 | 6,428,000 | 858,100 | 18,020 | **876,100** |

Resident tax: taxable income is far above 2,000,000 plus the differences, so the 調整控除 is the 50,000 floor in every
case, and the deduction alone moves the tax: 6% (ward) and 4% (Tokyo), each a whole 100 yen.
- aged 75, not a parent: 380,000 − 330,000 = 50,000 more deduction → 3,000 + 2,000 = **5,000 lower** than aged 40.
- aged 75, a parent: 450,000 − 330,000 = 120,000 → 7,200 + 4,800 = **12,000 lower** than aged 40.

Before this rule the engine gave the general amounts at every age (OPEN_QUESTIONS Q32): 916,900 and no difference.

## A lower income, where the 調整控除 differences count

Head aged 45, salary 3,500,000 (employee): salary income 3,500,000 × 70% − 80,000 = 2,370,000; social insurance
206,460 + 4,140 + 329,400 + 17,496 = 557,496; resident-tax basic deduction 430,000. Taxable income T (rounded down to
1,000) is under 2,000,000, so the 調整控除 is 3% (ward) and 2% (Tokyo) of the smaller of the total
difference and T. Each tax is rounded down to 100; the flat per-person part is 5,000.

| Dependant | Deduction | T | Differences (basic 50,000 +) | Ward 6% − 3% | Tokyo 4% − 2% | Resident tax |
|---|---|---|---|---|---|---|
| aged 40 | 330,000 | 1,052,000 | 100,000 | 63,120 − 3,000 → 60,100 | 42,080 − 2,000 → 40,000 | **105,100** |
| aged 75, not a parent | 380,000 | 1,002,000 | 150,000 | 60,120 − 4,500 → 55,600 | 40,080 − 3,000 → 37,000 | **97,600** |
| aged 75, a parent living with them | 450,000 | 932,000 | 180,000 | 55,920 − 5,400 → 50,500 | 37,280 − 3,600 → 33,600 | **89,100** |
