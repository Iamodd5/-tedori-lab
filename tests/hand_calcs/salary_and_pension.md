# Income adjustment for people with both salary and pension income (所得金額調整控除, second kind)

Rule: NTA タックスアンサー No.1411 (sources/tax/nta_1411_shotoku_kingaku_chosei.html), section
「給与所得と年金所得の双方を有する者に対する所得金額調整控除」 (租税特別措置法41条の3の12). Resident tax uses the
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
