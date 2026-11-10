# How would the tax plans change take-home pay? — Tedori Lab report (November 2026 edition)

## The main finding

**Under today's rules (2026 rules, before any plan), if a part-time spouse who works under {hours_min} hours a week and is not in their employer's health insurance earns ¥{lead_at} a year instead of ¥{lead_from}, the household takes home ¥{lead_drop} less a year.** The spouse stops being a dependant, so National Pension (¥{lead_np} a year) and National Health Insurance (¥{lead_nhi} a year) must be paid; taxes fall by ¥{lead_tax_cut} in all. Take-home pay gets back to where it was when the spouse earns ¥{lead_back} (worked out in {grid_step} steps). Example household H4: Shinjuku, Tokyo; one partner is an employee on ¥{h4_earner} a year; no children.

- (Approximation) In a couple, we assume the partner with the higher income pays the spouse's National Pension premiums and deducts them from their own income (by law either partner may).
- From fiscal 2026, whether someone can be a dependant is judged from the yearly pay expected under their work contract. Going over the line now and then, for example through overtime that isn't in the contract, may not end dependant status. Here we work out what happens when the contracted pay goes up.
- A spouse who works {hours_min}+ hours a week at a company with at least {employer_min} employees joins that company's insurance, so does not face this wall. The all-household estimate assumes every wage earner works like that.

(Approximation) Under the {daiwa_label}, the one plan that can be calculated now, take-home pay at the same point falls by ¥{lead_daiwa_drop} a year (¥{lead_drop} under 2026 rules), and gets back to the same level at ¥{lead_daiwa_back} (worked out in {grid_step} steps). The government's plans include a top-up (就業促進特例加算) that the outline calls a temporary measure until the income walls are removed. The outline defines the wall to include the extra premiums of moving into National Health Insurance and National Pension, not only joining company insurance, and gives an example of a spouse leaving dependant status, as H4's spouse does. On the top-up's amount, the outline says it will be set considering the overall balance, among other things (「総合的なバランス等を勘案して定める」). From fiscal {full_year}, married people whose spouse's income is above a set level (under the bill, an amount set by Cabinet order) don't qualify for the payment (the government's basic policy calls this a limited exception for people with a high-income spouse). So the government plans' effect on this household can't be calculated.

## About this report

The government, a trade union federation and a private research institute have put forward plans that change how working people's tax, social insurance and benefits work. Each plan states its own aims, such as easing the burden on people on low or middle incomes (see each plan below). Under the one plan that can be calculated now, take-home pay goes up for some households and down for others. One form these plans take is a "refundable tax credit" (給付付き税額控除): it cuts your income tax, and if the cut is bigger than the tax you owe, you get the rest in cash. In the government's plan, municipalities pay cash according to income, and the government calls it a "first step" towards a full refundable tax credit. Tedori Lab works out, with the same households, data and method, how {n_plans} of these plans would change take-home pay (what is left after tax and insurance, plus child allowance and the single-parent allowance) for example households and for every household in Japan. Each plan is compared with "2026 rules": the rules actually in force in 2026, before any of these plans. We assume nobody changes how much they work.

Every number in this report is produced automatically from the same output files as the website. This report does not support any plan, party or politician.

## The {n_plans} plans compared

{plan_list}

**Right now only the {done_labels} can be calculated.** The other {n_blocked} plans can't be calculated yet, for these reasons:

{blocked_list}

## Example households: {daiwa_label}

| Household | Who they are | Take-home pay under 2026 rules (yen a year) | (Approximation) Change under the plan (yen a year) |
|---|---|---|---|
{household_rows}

(Approximation) Of the {n_households} example households, {hh_up} take home more, {hh_down} take home less and {hh_same} see no change. The largest gain is for {hh_best} ({hh_best_change} yen a year) and the largest loss is for {hh_worst} ({hh_worst_change} yen a year).

{daiwa_note}

## Every household in Japan: {daiwa_label} (estimate)

We lined up every household from lowest to highest yearly income and cut the line into ten groups of the same size. (Approximation) All of the following are rough estimates.

- (Approximation) In groups {up_groups}, take-home pay goes up on average (by the most in group {up_top_group}: ¥{up_top} a year). But within these groups, take-home goes up for {up_win}% of households, and {up_same}% see no change.{up_lose}
- (Approximation) In groups {down_groups}, take-home pay goes down on average (by the most in group {down_top_group}: ¥{down_top} a year). But within these groups, take-home goes down for {down_lose_range}% of households, up for {down_win_range}%, and {down_same_range}% see no change.
- (Approximation) Overall, income tax rises by about ¥{it_up} trillion a year and about ¥{cash} trillion is paid out in cash (the part of the credit bigger than income tax), so the government takes in about ¥{net} trillion more a year (a rough estimate that assumes nobody changes how they work).
- Daiwa's own estimate is about ¥{pub_it} trillion more income tax and about ¥{pub_cash} trillion paid in cash: about zero overall (fiscally neutral). Daiwa used 2025 tax rules and a ¥{credit_2025} credit; this site uses 2026 rules and ¥{credit_2026}, so the two can't be compared directly.

## Limits

- We assume nobody changes how much they work. Some people would change their hours when the rules change; that is not included.
- The example households live in Shinjuku, Tokyo. Outside Shinjuku, parts of National Health Insurance and resident tax (set by each municipality) are different, and outside Tokyo so is the health insurance rate for employees (協会けんぽ, set by prefecture).
- The all-household numbers are rough estimates from made-up households matched to the averages in a 2024 government survey. Compared with official figures, the household count is {gap_households}% lower. Total income tax is {gap_income_tax}% lower and total resident tax {gap_resident_tax}% lower than the tax that survey itself estimates from reported incomes (not tax actually collected; income tax is lower because of recent tax cuts (a larger basic deduction), too few high earners in the estimate and taxing households' average incomes, among other things, which we haven't measured separately). The estimate has too many low-paid workers and too few high earners compared with official counts, so the cash paid out and the extra income tax may be off. Changing how the made-up households are built can move the national totals a lot, especially the cash paid out. The gaps with official figures (too many low-paid workers, too few high earners) both make the cash paid out look larger and the extra income tax smaller, so the net gain to the government is more likely above this estimate's figure than below. The survey's tax estimate is after the one-off 2024 flat tax cut, so against a normal year the shortfall would be larger (see the Checks page).
- The plans that can't be calculated yet will be calculated once the amounts they need are decided and published (the reasons for each are listed above).

## All approximations

Behind every number:

{approx_baseline}

{daiwa_label}:

{approx_daiwa}

All-household numbers:

{approx_population}

## Method and sources

The method, the checks and every source are on the website's How it works, Checks and Sources & code pages. All the code is public, and anyone can rebuild every number, including this report, with `make all`.
