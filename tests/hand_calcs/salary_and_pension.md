# Income adjustment for people with both salary and pension income (所得金額調整控除, second kind)

Rule: NTA タックスアンサー No.1411 (sources/tax/nta_1411_shotoku_kingaku_chosei.html), section
「給与所得と年金所得の双方を有する者に対する所得金額調整控除」 (租税特別措置法41条の3の11第2項). Resident tax uses the
same deduction: 大田区「計算のしくみ」 注釈2 (2) (sources/tax/ota_keisan_no_shikumi.html).

- Applies to a person with both 給与所得控除後の給与等の金額 (salary income) and 公的年金等に係る雑所得 (pension income),
  when the two add up to more than 100,000.
- Deduction = min(salary income, 100,000) + min(pension income, 100,000) − 100,000, taken off salary income.
- If the first kind (salary over 8.5m with a dependant under 23) also applies, the second kind uses the salary income
  after the first.

Salary income for 2026 (令和8年分): revenue 741,000–2,190,999 → revenue − 740,000.
Pension income, aged 65 or over, pension revenue up to 3,300,000, other income up to 10m → revenue − 1,100,000.

| Age | Salary | Pension | Salary income | Pension income | Deduction | Total income |
|---|---|---|---|---|---|---|
| 70 | 1,000,000 | 2,000,000 | 260,000 | 900,000 | 100,000 + 100,000 − 100,000 = 100,000 | 260,000 − 100,000 + 900,000 = **1,060,000** |
| 70 | 800,000 | 1,160,000 | 60,000 | 60,000 | 60,000 + 60,000 − 100,000 = 20,000 | 60,000 − 20,000 + 60,000 = **100,000** |
| 70 | 790,000 | 1,130,000 | 50,000 | 30,000 | sum 80,000 is not over 100,000 → 0 | **80,000** |
| 70 | 1,000,000 | 0 | 260,000 | 0 | no pension income → 0 | **260,000** |

Before this rule the engine gave 1,160,000, 120,000, 80,000 and 260,000 (OPEN_QUESTIONS Q41).
No example household H1–H8 has both kinds of income; the all-household estimate does (relatives aged 70 who
receive a share of other members' earnings).

## The 65+ care premium uses salary income before this deduction

介護保険法施行令22条の2第4項第1号 (sources/law/kaigo_sekourei_410CO0000000412_asof20260401.xml): for bands 1–5, salary
income is taken 「（租税特別措置法第四十一条の三の十一第二項の規定による控除が行われている場合には、その控除前の金額）から
十万円を控除して得た額」 (not below 0). So the deduction above must not also lower the premium's measure.

Age 70, living alone, salary 900,000, pension 1,150,000:
- salary income 900,000 − 740,000 = 160,000; pension income 1,150,000 − 1,100,000 = 50,000;
- deduction 100,000 + 50,000 − 100,000 = 50,000; total income 160,000 − 50,000 + 50,000 = 160,000; no resident tax (450,000 limit);
- premium measure: 課税年金収入 1,150,000 + (160,000 − 100,000) = **1,210,000**, above 1,200,000 → band 3, **51,480**
  (taking the deduction off as well would give 1,160,000 → band 2, 27,720).
