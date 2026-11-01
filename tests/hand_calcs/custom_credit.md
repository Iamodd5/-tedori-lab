# Hand calculation: the custom credit (design builder, Milestone 8)

The custom credit has no policy numbers: the visitor sets them with sliders (`parameters/designs/custom_template.yaml`).
The values below are **test values only**.

Test values: phase-in rate 10%, maximum 100,000, phase-out starts at income 3,000,000, phase-out rate 5%,
child addition 50,000 per child.

## Rule

For each person with earnings (salary + business income) above 0:

1. credit = min(10% × earnings, 100,000)
2. the partner with the higher earnings (the head if equal) adds 50,000 for each child aged 18 or under
   (the same age limit as the child allowance, `child_allowance.yaml` eligible_age_max)
3. subtract 5% × (income − 3,000,000) if income is above 3,000,000, where income = earnings + pensions,
   all before tax
4. not below 0; rounded down to the yen

The credit is paid in cash on top of take-home pay under 2026 rules. It is not taxed and changes no other tax,
insurance or benefit.

## Single people

| Case | Salary | Business | Pension | Credit |
|---|---|---|---|---|
| a | 0 | 0 | 2,000,000 | no earnings → **0** |
| b | 500,000 | 0 | 0 | min(50,000, 100,000) = **50,000** |
| c | 2,000,000 | 0 | 0 | min(200,000, 100,000) = **100,000** |
| d | 4,000,000 | 0 | 0 | 100,000 − 5% × 1,000,000 = **50,000** |
| e | 6,000,000 | 0 | 0 | 100,000 − 150,000 < 0 → **0** |
| f | 1,000,000 | 0 | 2,500,000 | 100,000 − 5% × 500,000 = **75,000** |
| g | 0 | 300,000 | 0 | 10% × 300,000 = **30,000** |
| h | 123,456 | 0 | 0 | 12,345.6 → rounded down **12,345** |

## A couple with children: H3 at its reference income

Head salary 4,500,000; spouse salary 3,000,000; children aged 8 and 2.

- Head (higher earnings): min(450,000, 100,000) + 2 × 50,000 − 5% × (4,500,000 − 3,000,000) = 200,000 − 75,000 = **125,000**
- Spouse: min(300,000, 100,000) − 0 (income not above 3,000,000) = **100,000**
- Household: **225,000**

## A single parent: H5 at its reference income

Parent salary 2,500,000; one child aged 10: min(250,000, 100,000) + 50,000 = **150,000**.
