# Government payment shape — hand calculation with TEST VALUES

The government has not published any amounts (OPEN_QUESTIONS Q9), so this checks only the *shape* from the
Sep 15 outline (sources/gov/20260915_01_siryou1.pdf pp.8–10, 第三 一 2(1)①②④⑤). The numbers are made up for
the test and are **not policy numbers**; they are never used for results.

Test values: floor 100,000; flat 20,000 up to earned income 500,000 (phase-in start); rises in a straight line to
the basic amount 60,000 at earned income 1,500,000 (phase-in end); child addition 30,000 per child; above total
income 3,000,000 the basic amount (+ child additions) falls by 10% of the excess; ceiling 6,000,000.
Result rounded up to 1,000 yen.

| Case | Earned | Total income | Children | Working | Payment |
|---|---|---|---|---|---|
| a | 50,000 | 50,000 | 0 | at or below floor → not eligible | 0 |
| b | 400,000 | 400,000 | 0 | flat | 20,000 |
| c | 1,000,000 | 1,000,000 | 0 | 20,000 + 40,000 × (500,000 / 1,000,000) = 40,000 | 40,000 |
| d | 1,000,000 | 1,000,000 | 2 | 40,000 + 2 × 30,000 | 100,000 |
| e | 2,000,000 | 3,500,000 | 1 | min(60,000 + 30,000, 90,000 − 10% × 500,000 = 40,000) | 40,000 |
| f | 2,000,000 | 3,950,500 | 0 | 60,000 − 95,050 < 0 → 0 | 0 |
| g | 1,234,567 | 1,234,567 | 0 | 20,000 + 40,000 × 734,567/1,000,000 = 49,382.68 → up to 1,000 | 50,000 |
| h | 2,000,000 | 6,000,001 | 0 | above ceiling | 0 |

Food tax cut, consumption-tax side (parameters/designs/food_tax_cut.yaml): a price that includes 8% tax falls to
1% tax. With full pass-through, tax paid on food spending S (measured at today's prices) falls by
S × (0.08 − 0.01) / 1.08. Test value S = 1,080,000 → 70,000 less tax; at 50% pass-through, 35,000.
