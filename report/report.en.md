# How would the tax plans change take-home pay? — Tedori Lab report (November 2026 edition)

## The main finding

**Under 2026 rules, if a part-time spouse's pay goes from ¥{lead_from} to ¥{lead_at} a year, the household takes home ¥{lead_drop} less a year.** To get back to the same take-home pay, the spouse has to earn ¥{lead_back} (example household H4: one partner is an employee on a salary of ¥{h4_earner} a year, the other works part-time).

Calculated with the one plan that can be calculated now, the {daiwa_label}, take-home pay at the same point falls by ¥{lead_daiwa_drop} a year and gets back to the same level at ¥{lead_daiwa_back}.

## About this report

The government and others have put forward plans to lower the tax and social insurance that working people pay. One idea is a "refundable tax credit" (給付付き税額控除): it cuts your income tax, and if the cut is bigger than the tax you owe, you get the rest in cash. Tedori Lab works out, with the same households, data and method, how {n_plans} of these plans would change take-home pay (what is left after tax and insurance) for example households and for every household in Japan. Each plan is compared with "2026 rules": the rules actually in force in 2026, before any of these plans. We assume nobody changes how much they work.

Every number in this report is produced automatically from the same output files as the website. This report does not support any plan, party or politician.

## The {n_plans} plans compared

{plan_list}

**Right now only the {done_labels} can be calculated.** The other {n_blocked} plans can't be calculated yet, for these reasons:

{blocked_list}

## Example households: {daiwa_label}

| Household | Who they are | Take-home pay under 2026 rules (yen a year) | Change under the plan (yen a year) |
|---|---|---|---|
{household_rows}

Of the {n_households} example households, {hh_up} take home more, {hh_down} take home less and {hh_same} see no change. The largest gain is for {hh_best} ({hh_best_change} yen a year) and the largest loss is for {hh_worst} ({hh_worst_change} yen a year).

{daiwa_note}

## Every household in Japan: {daiwa_label} (estimate)

We lined up every household from lowest to highest yearly income and cut the line into ten groups of the same size. (Approximation) All of the following are rough estimates.

- (Approximation) In groups {up_groups}, take-home pay goes up on average (most in group {up_top_group}: ¥{up_top} a year).
- (Approximation) In groups {down_groups}, take-home pay goes down on average (most in group {down_top_group}: ¥{down_top} a year).
- (Approximation) Overall, income tax rises by ¥{it_up} trillion a year and ¥{cash} trillion is paid out in cash (the part of the credit bigger than income tax), so the government takes in ¥{net} trillion more a year.
- Daiwa's own estimate is about ¥{pub_it} trillion more income tax and about ¥{pub_cash} trillion paid in cash: about zero overall (fiscally neutral). Daiwa used 2025 tax rules and a ¥{credit_2025} credit; this site uses 2026 rules and ¥{credit_2026}, so the two can't be compared directly.

## Limits

- We assume nobody changes how much they work. Some people would change their hours when the rules change; that is not included.
- The example households live in Shinjuku, Tokyo. National Health Insurance and some other amounts differ between cities.
- The all-household numbers are rough estimates from made-up households matched to the averages in a 2024 government survey. Compared with official figures, the household count is {gap_households}% lower, total income tax {gap_income_tax}% lower and total resident tax {gap_resident_tax}% lower.
- The plans that can't be calculated yet will be calculated once the amounts they need are published.

## All approximations

Behind every number:

{approx_baseline}

{daiwa_label}:

{approx_daiwa}

All-household numbers:

{approx_population}

## Method and sources

The method, the checks and every source are on the website's How it works, Checks and Sources & code pages. All the code is public, and anyone can rebuild every number, including this report, with `make all`.
