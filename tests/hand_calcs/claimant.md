# Who claims the spouse and dependants (Milestone 5 fix)

Rule used: in a couple, the partner with the higher total income claims the other as spouse and claims the
children; a partner can be a health-insurance dependant (and category-3 pension member) of whichever partner is in
employee insurance. Either partner may legally claim; choosing the higher earner is a modelling choice
(**approximation**, OPEN_QUESTIONS Q23). Before the fix only the member labelled "head" could claim or be claimed on.

## H3 with the head's salary at 1,000,000 (spouse b stays at 3,000,000)
- Head: employment income 1,000,000 − 740,000 = 260,000 ≤ 620,000 → b can claim the head as spouse.
- b: total income 2,020,000; employee premiums 457,728 (H3.md). Spouse deduction (b's income ≤ 9m column) 380,000.
- b's income tax: 2,020,000 − 1,040,000 − 457,728 − 380,000 = 142,272 → 142,000 × 5% = 7,100 × 1.021 = 7,249.1
  → **7,200** (before the fix: 26,600, with no spouse deduction).

## H3 with the head's salary at 0
- b is in employee insurance; the head has no income (< 1,300,000) → health-insurance dependant of b and
  category-3 pension member: **no NHI and no national pension** (before the fix: NHI + 215,040 national pension).

## Elderly spouse (income tax)
- NTA 年末調整のしかた p.55: 老人控除対象配偶者 (spouse aged 70 or over), earner total income ≤ 9,000,000 → **480,000**.
