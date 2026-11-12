# How tax and benefit plans would change take-home pay: Tedori Lab report (November 2026 edition)

## Main points

Tedori Lab works out how {n_plans} plans to change tax and benefits would alter households' take-home pay, using the same households, data and method for each. Take-home pay means what is left after tax and insurance premiums, plus child allowance and the single-parent allowance. The calculations cover example households and every household in Japan. Only the {done_labels} can be calculated so far.

- **Under today's rules (the 2026 rules), a household takes home ¥{lead_drop} less a year when a part-time spouse earns ¥{lead_at} a year instead of ¥{lead_from}.** This is before any of the plans. The spouse works under {hours_min} hours a week and is not in their employer's health insurance. A point like this, where earning more leaves a household with less, is called an income wall (年収の壁). The figures are for example household H4: a couple with no children in Shinjuku, Tokyo, in which the other partner is an employee on ¥{h4_earner} a year.
- (Approximation) Under the Daiwa Institute plan, {hh_up} of the {n_households} example households take home more, {hh_down} take home less and {hh_same} see no change. The largest gain is for {hh_best} ({hh_best_change} yen a year) and the largest loss is for {hh_worst} ({hh_worst_change} yen a year).
- (Approximation) Under the Daiwa Institute plan, the government takes in about ¥{net} trillion more a year across the country, in a rough estimate that assumes nobody changes how they work. Income tax rises by about ¥{it_up} trillion a year, and the government pays out about ¥{cash} trillion in cash: the part of the tax credit (an amount taken straight off income tax) that is bigger than the income tax owed. The section on every household in Japan explains how this differs from Daiwa's own estimate.

## How to read the numbers

- Each plan is compared with '2026 rules': the rules actually in force in 2026, before any of these plans. This report also calls them today's rules.
- We assume nobody changes how much they work.
- A figure marked 'Approximation' rests on a point where the calculation had to be simplified. These points are listed at the end, under All approximations.
- Every number is produced automatically from the same calculation results as the website.
- This report does not support any plan, party or politician.

## The {n_plans} plans compared

The government, a trade union federation and a private research institute have put forward plans that change how working people's tax, social insurance and benefits work. Each plan states its own aims, such as easing the burden on people on low or middle incomes. Under the one plan that can be calculated now, take-home pay goes up for some households and down for others.

One form these plans take is a 'refundable tax credit' (給付付き税額控除): it cuts your income tax, and if the cut is bigger than the tax you owe, you get the rest in cash. In the government's plan, municipalities pay cash according to income, and the government calls it a "first step" towards a full refundable tax credit. The plans are:

{plan_list}

The {n_blocked} plans other than the Daiwa Institute plan cannot be calculated yet, for these reasons:

{blocked_list}

## The income wall for a part-time spouse

The household in the first main point hits this wall because the spouse stops being a dependant. A dependant here is someone covered by an employee partner's health insurance and pension without paying premiums of their own. Once that ends, National Pension (¥{lead_np} a year) and National Health Insurance (¥{lead_nhi} a year) premiums must be paid. Taxes fall by ¥{lead_tax_cut} in all. Take-home pay gets back to where it was when the spouse earns ¥{lead_back}. Pay is worked out in {grid_step} steps.

(Approximation) Under the {daiwa_label}, the one plan that can be calculated now, take-home pay at the same point falls by ¥{lead_daiwa_drop} a year (¥{lead_drop} under 2026 rules). It gets back to the same level at ¥{lead_daiwa_back}, again worked out in {grid_step} steps.

The government plans' effect on this household cannot be calculated, for these reasons:

- The government's plans include a top-up (就業促進特例加算). The government's outline, the document that sets out the framework of the scheme, calls it a temporary measure until the income walls are removed.
- The outline defines the wall to include the extra premiums of moving into National Health Insurance and National Pension, not only joining company insurance. It also gives an example of a spouse leaving dependant status, as H4's spouse does.
- On the top-up's amount, the outline says it will be set considering the overall balance, among other things (「総合的なバランス等を勘案して定める」).
- From fiscal {full_year}, married people whose spouse's income is above a set level do not qualify for the payment. Under the bill, that level is an amount set by Cabinet order. The government's basic policy calls this a limited exception for people with a high-income spouse.

These further points apply to this calculation:

- (Approximation) In a couple, we assume the partner with the higher income pays the spouse's National Pension premiums and deducts them from their own income. By law either partner may.
- From fiscal 2026, whether someone can be a dependant is judged from the yearly pay expected under their work contract. Going over the line now and then, for example through overtime that isn't in the contract, may not end dependant status. Here we work out what happens when the contracted pay goes up.
- A spouse who works at least {hours_min} hours a week, at a company with at least {employer_min} employees, joins that company's insurance and so does not face this wall. The all-household estimate assumes every wage earner works like that.

## Results for each example household

This table shows the change in take-home pay under the {daiwa_label} for each example household. The main points give the summary.

| Household | Who they are | Take-home pay under 2026 rules (yen a year) | (Approximation) Change under the plan (yen a year) |
|---|---|---|---|
{household_rows}

In the table, + means take-home pay goes up and − means it goes down.

{daiwa_note}

## Results for every household in Japan (rough estimate)

We worked out the change in take-home pay under the {daiwa_label} for every household in Japan, by income group. The groups are ten equal-sized sets of households, lined up from lowest to highest yearly income. (Approximation) All of the following are rough estimates.

- (Approximation) In groups {up_groups}, take-home pay goes up on average. The biggest average change is in group {up_top_group}, at ¥{up_top} a year per household. But within these groups, take-home pay goes up for {up_win}% of households, and {up_same}% see no change.{up_lose}
- (Approximation) In groups {down_groups}, take-home pay goes down on average. The biggest average change is in group {down_top_group}, at ¥{down_top} a year per household. But within these groups, take-home pay goes down for {down_lose_range}% of households and up for {down_win_range}%, and {down_same_range}% see no change.

The national total is in the main points. Daiwa's own estimate is about ¥{pub_it} trillion more income tax and about ¥{pub_cash} trillion paid in cash, which comes to about zero overall. This is called fiscally neutral. The two estimates cannot be compared directly, because Daiwa used 2025 tax rules and a ¥{credit_2025} credit, and this site uses 2026 rules and ¥{credit_2026}.

## Assumptions and limits

- We assume nobody changes how much they work. Some people would change their hours when the rules change; that is not included.
- The example households live in Shinjuku, Tokyo. Outside Shinjuku, the parts of National Health Insurance and resident tax that each municipality sets are different. Outside Tokyo, so is the health insurance rate for employees (協会けんぽ), which is set by prefecture.
- The all-household numbers are rough estimates from made-up households matched to the averages in a 2024 government survey. They differ from official figures in these ways:
  - The household count is {gap_households}% lower than the official figure.
  - Total income tax is {gap_income_tax}% lower and total resident tax {gap_resident_tax}% lower than the tax that survey itself estimates from reported incomes. This is not a comparison with tax actually collected.
  - Income tax is lower because of recent tax cuts (a larger basic deduction), too few high earners in the estimate and taxing households' average incomes, among other things. We have not measured each of these separately.
  - The survey's tax estimate is after the one-off 2024 flat tax cut, so against a normal year the shortfall would be larger (see the Checks page).
- Compared with official counts, the estimate has too many low-paid workers and too few high earners. Both gaps make the cash paid out look larger and the extra income tax smaller, so the net gain to the government is more likely above this estimate's figure than below.
- Changing how the made-up households are built can move the national totals a lot, especially the cash paid out.
- The plans that cannot be calculated yet will be calculated once the amounts they need are decided and published. The reasons for each are listed under the plans above.

## All approximations

These are the points where the calculation behind a figure marked 'Approximation' was simplified.

### Behind every number

{approx_baseline}

### {daiwa_label}

{approx_daiwa}

### All-household numbers

{approx_population}

## Method and sources

The method, the checks and every source are on the website's How it works, Checks and Sources and code pages. All the code is public, so anyone can recalculate every number, including this report, and check it. The steps are on the Sources and code page.
