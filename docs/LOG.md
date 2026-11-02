# Project log (plain language)

## Milestone 0 — 2026-10-29: setup, sources, coverage

**What we did**

1. **Notifications.** Claude Code can run a small command whenever it stops and waits for you. We set two of these "hooks" in `.claude/settings.json`: one for the *Stop* event (Claude finished a turn) and one for the *Notification* event (Claude needs permission or input). Both run macOS's `osascript` to pop up "Tedori Lab: your action is needed. Check the terminal." with the "Glass" sound. A test notification was fired by hand (it ran without error). Hooks load when a session starts, so a fresh session is needed for them to be active.
   - If no pop-up appears: macOS shows `osascript` notifications under the app name **Script Editor**. Open System Settings → Notifications → Script Editor and turn on "Allow notifications". Also check that Focus / Do Not Disturb is off.
2. **Project skeleton.** Saved `SPEC.md` and `CLAUDE.md` (the project rules), started `OPEN_QUESTIONS.md` and `docs/HUMAN_TODO.md`, and made the folder a git repository.
3. **Sources.** Downloaded 50 files (government council papers, Daiwa's report, tax and insurance pages, Tokyo 2026 health-insurance tables, statistics landing pages) into `sources/`, each listed in `sources/SOURCES.md`, with fingerprints (SHA-256) in `sources/SHA256SUMS`. A helper script, `scripts/pdf_to_text.py`, turns every PDF into searchable text in `sources/text/`.
4. **Coverage check.** Read the OpenFisca-Japan code (the open-source Japanese tax-and-benefit calculator we plan to build on) and wrote down in `docs/COVERAGE.md` which rules it already has and which are missing or out of date.

**What we learned**

- The story has moved on since the spec was written. July 13 was only the *draft* interim summary. The government then adopted the interim summary (July 29), the Cabinet approved a basic policy (Aug 5), and in September–October it approved and sent to the Diet a law that (a) cuts the consumption tax on food from 8% to 1% for two years from April 2027, and (b) adds a new cash payment for workers called 就業者負担軽減支援金. Deciding which of these is "the government design" is a human decision (HUMAN_TODO H-3).
- The full refundable credit itself is planned for FY2029 (令和11年度). It is per person (not per household), includes single people, rises with work income up to a level, stays flat, then shrinks and disappears at higher total income, with extra for each child aged 18 or under. Exact numbers are for Milestone 1.
- Rengo's website was under maintenance, so its proposal could not be downloaded.
- OpenFisca-Japan already does income tax, resident tax, employee social insurance and child allowance, but some numbers are placeholders or old (e.g. health insurance rate, national pension amount), and it has no National Health Insurance. We will fix these in our own parameter files and offer the fixes back.

**Tools installed**

- A Python virtual environment in `.venv/` with `pypdf`, `cryptography` (needed to open some government PDFs) and `pyyaml`. Python on this machine is 3.15.

### Audit fixes — 2026-10-30

- `requirements.txt` lists the exact Python packages. A fresh copy is set up with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
- File fingerprints moved from hand-copied table columns into `sources/SHA256SUMS`. `cd sources && shasum -a 256 -c SHA256SUMS` checks every file at once.
- The Daiwa report now has its full title in `SOURCES.md` (rule 1).
- `scripts/pdf_to_text.py` names each text file by folder + file name (e.g. `gov_20260713_02_siryou2.txt`), so two PDFs with the same name can't overwrite each other.
- Empty placeholder folders were removed; each folder from SPEC Section 4 is created when its first file is saved.

### Notification fix — 2026-10-30

The first test pop-up did not appear, and "Script Editor" was missing from System Settings → Notifications. macOS only lists an app there after it has asked for permission once. Fix: open Script Editor, run `display notification "Tedori Lab test" with title "Tedori Lab"` there, click **Allow**, and check that Notifications → Script Editor is on. After that, notifications sent from Terminal worked (confirmed by the human, H-1).

## Milestone 1 — 2026-10-30: design parameters

Decision used (H-3): the "government design" is the August 5 Cabinet decision, with details from the July 29 interim summary, the September 15 outline and the October 9 bill. The new worker payment that comes with the food tax cut is part of the food tax cut design.

**What each design file says** (all in `parameters/designs/`)

- **government_final.yaml.** From FY2029 the government will pay each working person (not each household) a yearly cash amount called 就業者負担軽減支援金. The rules so far:
  - You must earn at least a minimum amount from work, and have total income below a maximum.
  - What you pay in tax and social insurance, minus any public pension you receive, must be above a set level. This lets working older people qualify. The government also names who is left out for now: low earners below the minimum, and older people who do not work. Both are to be looked at again later (Aug 5 explanation slide, 資料3 p.3). Our pensioner couple H6 has no work income, so it would get nothing from this payment.
  - If your spouse has a high income, you are excluded.
  - How much you get: a fixed amount at very low earnings. Above that, it rises with each extra yen earned, then stays flat. People earning just past the "income wall", where social insurance starts, get a temporary extra amount. Each child aged 18 or under adds a fixed amount. Above a higher income, the payment shrinks and then disappears.
  - Amounts are rounded up to the next 1,000 yen. It is paid once a year and is not taxed.
  - **None of the yen amounts or rates have been published yet.** The law leaves them to a later Cabinet order, so every number is marked "unresolved" (Q9).
- **food_tax_cut.yaml.** From 1 April 2027 to 31 March 2029, consumption tax on food goes from 8% to 1% (0.78% national plus local tax). "Food" means the same items that get the 8% reduced rate today; newspapers stay at 8%. The same worker payment also starts in FY2027, with three differences: children count only up to age 15, there is no spouse test, and the total cost is capped at roughly what 1% of consumption tax on food raises. Its amounts are also unpublished. Our baseline modelling assumption is that shops pass the whole tax cut on to prices. This is an approximation, and we also show a case where only half reaches shoppers.
- **daiwa.yaml.** Daiwa's idea:
  - Remove the basic deduction from income tax, and give every taxpayer a 56,500-yen tax credit instead. A tax credit is subtracted from the tax bill itself, not from income.
  - If your income tax is smaller than the credit, you get the difference back as cash, but never more than the social insurance you paid on your work income. So people living only on pensions or savings get no cash.
  - Resident tax does not change.

  The report also lists seven other versions. Which to use is your decision (Q10).
- **rengo.yaml.** Empty for now, because Rengo's website was down (Q3).
- **custom_template.yaml.** The five slider settings for the design builder. These have no official values.

**How we check it**

`tests/test_design_citations.py` opens every design file. Each parameter must either have a value plus a source and page number, or be marked "unresolved" with a question ID. Run it with `.venv/bin/python -m pytest -q tests`. Today: 6 passed.

## Milestone 2 — 2026-10-30: the 2026 baseline for H1–H8

Decision used (H-8): National Health Insurance follows Shinjuku ward's rules. Reference incomes as proposed: H1 1.25m; H2 1.0m; H3 4.5m + 3.0m; H4 5.0m + 1.0m; H5 2.5m; H6 pensions 2.0m + 0.8m; H7 business income 3.0m; H8 9.0m + 7.0m.

**How take-home pay is worked out** (`engine/baseline.py`, numbers in `parameters/baseline_2026/`)

1. **Employment income.** From your salary, the law first subtracts a fixed "employment income deduction" (an allowance for work costs). The result is your employment income. For 2026 the minimum deduction rose to 740,000 yen. So:
   - Salary below 741,000 counts as zero income.
   - Up to 2.19 million, income is salary minus 740,000.
   - From there up to 6.6 million, the tax office's official table gives the amount in 4,000-yen steps.
   - Above 6.6 million, a formula is used.

   Earners above 8.5 million with a child under 23 get a further cut of 10% of the salary above 8.5 million (capped at 10 million).
2. **Pension income.** People 65 or older subtract up to 1.1 million from their public pension, and more on a sliding scale at higher pensions.
3. **Social insurance.**
   - **Employees** pay half of each premium, read from Tokyo's 2026 table using "standard monthly pay" bands:
     - health insurance: 9.85%, or 11.47% at ages 40–64, because long-term care is added
     - the new child and childcare support levy: 0.23%
     - pension: 18.3%, with pay counted between 88,000 and 650,000 a month
     - employment insurance: 0.5% for the worker

     A part-timer joins only if all of these hold: they work 20+ hours a week, at a firm with 51+ staff, earn at least 88,000 a month, and are not a student.
   - **A spouse or child who doesn't join** can be a "dependant" with no premiums while their income stays under 1.3 million (1.5 million at ages 19–22). A dependant spouse also pays no pension contribution.
   - **Everyone else** pays National Health Insurance to Shinjuku. For each member there is a flat amount plus a percentage of income above 430,000. Low-income households get the flat amounts cut by 70%, 50% or 20%. People aged 20–59 in this group also pay the national pension, 17,920 yen a month.
4. **Income tax.**
   - From total income, take away the basic deduction (1.04 million for incomes up to 4.89 million, less above that), all social insurance paid, and any personal deductions: spouse, dependants aged 16+, single parent (350,000), working student (270,000).
   - Round the remainder down to 1,000 yen and apply the rate table (5% to 45%).
   - Add 2.1% reconstruction tax, then round down to 100 yen.
5. **Resident tax** (Shinjuku plus Tokyo).
   - Very low incomes pay nothing. For a single person, that means total income of 450,000 or less.
   - Everyone else pays a flat 5,000 yen (ward 3,000, Tokyo 1,000, forest tax 1,000).
   - On top of that, 10% of income after a smaller basic deduction (430,000) and smaller personal deductions, minus a small "adjustment credit" (調整控除) of at least 2,500 yen.
6. **Child allowance.** 15,000 yen a month for each child under 3, and 10,000 for each child from age 3 through high school. The third and later children get 30,000. There is no income limit.
7. **Disposable income** = pay + pensions + child allowance − income tax − resident tax − social insurance.

**Checks.** 28 tests pass (`make all`). They cover:
- the tax office's own worked example
- Shinjuku's health-insurance quick table
- Tokyo's premium table
- all 8 households against step-by-step hand calculations (`tests/hand_calcs/`), which agree to the yen

The table in `docs/VALIDATION.md` also compares our results with OpenFisca-Japan.

**Tools.** The project now runs on Python 3.11, because OpenFisca-Japan needs it. Set up with `uv venv --python 3.11 .venv && VIRTUAL_ENV=.venv uv pip install -r requirements.txt`.

## Milestone 3 — 2026-10-31: the designs as reforms

**Decision recorded.** H-9: A. We keep our own small baseline engine. OpenFisca-Japan stays as a cross-check, and fixes we find are offered back to it.

**How a design is tested against the baseline** (`engine/reforms.py`). We work out a household's take-home pay twice: once under 2026 law, once with the design switched on. The difference is the design's effect. We split it into five parts: income tax, resident tax, social insurance, money paid out by the design, and consumption tax.

**Daiwa's plan.** Today everyone subtracts a "basic deduction" from income before income tax. Daiwa removes it and gives everyone a fixed 56,500 yen off their income tax instead.
- If your tax is smaller than 56,500, the rest is paid to you in cash, but only if you work, and never more than you paid into health insurance and pension.
- Example: H1 (part-timer, 1.25 million) would owe 16,300 yen without the deduction, so 40,200 yen is left over and paid out. H1 gains 40,200 a year.
- Higher earners lose the deduction, which was worth more to them than 56,500 yen, so they pay more. H3's couple pays 18,300 more, H8's couple 148,100 more.
- Problem found: Daiwa sized the 56,500 for 2025 law. In 2026 the basic deduction almost doubled at most incomes, so the same swap costs far more. A single worker on 5 million pays 40,700 more with us, against 13,000 in Daiwa's report. How to handle this is a human decision (H-10).

**The government's payment and the food tax cut.** The law fixes the *shape* of the payment:
- a small flat amount for very low earners,
- then more as you earn more,
- then a flat "basic amount", plus an extra amount per child,
- then it shrinks once total income passes a set level.
That shape is now coded and tested with made-up practice numbers. But every real amount will be set later by a Cabinet order that is not out yet. So the site will show these designs as "incomplete" with no number, instead of a guess. The same goes for the food tax saving until we load food spending by income group (Q8), and for Rengo, whose documents we still cannot download (H-4).

**First contribution for OpenFisca-Japan.** Their national pension amount is 17,510 yen a month, from 2015. For 2026 it is 17,920. The exact change is written in `docs/COVERAGE.md`, ready for the human to submit.

**Checks.** 75 tests pass, including hand calculations for Daiwa (H1, H3, H7), eight practice cases for the payment shape, and a test that every design runs on every household without inventing a number.

## Milestone 4 — 2026-11-01: wall map and comparison table

**Decision recorded.** H-10: A. Daiwa's plan is applied exactly as published, on 2026 rules. Every Daiwa number on the site carries a note (in Japanese and English) saying Daiwa designed it for 2025 rules, so our results differ from theirs.

**The comparison table** (`outputs/household_comparison.csv`). For each household and each design, how much take-home pay changes in a year, and why: income tax, resident tax, social insurance, money paid out, consumption tax. Designs whose numbers are not published yet say "incomplete" instead of showing a number.

**The wall map** (`outputs/wall_map.json`).
- We raise one person's income in 10,000-yen steps from 0 to 10 million.
- At each step we ask: of the next 10,000 yen earned, how much is lost to tax, insurance and lost benefits? That share is the "effective marginal rate".
- If it is more than 100%, earning more leaves you with less money. That is a "wall".

Walls the map shows for 2026 rules:
- **H2 (student), at 1.5 million.** Above it the student can no longer be on the parents' health insurance.
- **H2 and H7, at total income 4.89 million.** The basic deduction drops from 1.04 million to 670,000 here. Daiwa's plan removes this cliff because it removes the basic deduction.
- **H5 (single parent), at salary 2.09 million.** The single-parent exemption from resident tax ends.
- **Every employee, small steps.** Insurance premiums are charged on "bands" of monthly pay, so moving up a band costs more than the raise.

**A surprise worth knowing.** H1 is called "near the 1.3 million wall", but as we modelled H1 (living alone), that wall does not hit them. The 1.06m and 1.3m walls only apply to someone who could otherwise be covered as a dependant on a parent's or spouse's insurance for free. A single person below that line already pays National Health Insurance and the national pension (about 235,000 yen a year), which is more than the employee premiums at that pay. So joining employee insurance actually *raises* H1's take-home pay by about 90,000 yen. Whether to redefine H1 is an open question (Q21).

**What is not done yet.**
- Wall maps for the four households with two incomes (H3, H4, H6, H8) need a decision on whose income moves (H-11).
- A preview page, `site/wallmap.html`, draws both charts and the table straight from `outputs/`.

### Milestone 4 completed — 2026-11-01

**Decision recorded.** H-11: D. In households with two incomes, the wall map moves:
- H4: the part-time spouse's pay (to show the spouse walls);
- H3 and H8: the main earner's pay;
- H6: the main pensioner's pension.

**H4 shows the famous 1.3 million wall.** When the spouse's pay goes from 1,290,000 to 1,300,000, the spouse can no longer be covered for free on the main earner's insurance. The household must now pay:
- national pension, 215,040 a year;
- National Health Insurance, 101,786 a year.
Taxes fall a little, but take-home pay still drops by 281,926 yen for earning 10,000 more. Every step is in `tests/hand_calcs/wall_H4.md`.

**Two rules fixed because the wall map exposed them.** Neither changes the eight reference households.
1. *National Health Insurance discount for low-income homes.* Shinjuku decides who gets it by adding up the incomes of the insured people **and** the head of the household, even if the head has work insurance. We had left the head out.
2. *Resident-tax "soft landing".* Just above the income level where resident tax starts, the law limits the tax to the amount by which your income is over that level. This stops a 10,000-yen raise from costing 85,000 yen in tax. The Ministry's own example: line 1,120,000, income 1,124,200, tax 4,200.

**Why there are spikes every 240,000 yen.** Employee insurance is charged on "standard monthly pay" in steps of 20,000 a month at middle incomes. Crossing a step raises a whole year's premiums at once, so for that 10,000 yen the marginal rate is about 300%. These steps are real. They look sharp only because we use 10,000-yen steps.

**Checks.** 83 tests pass. `make all` rebuilds the outputs, and the preview page draws all eight households.

## Milestone 5 — 2026-11-01: adversarial self-review (spec 12.3)

Two independent reviewers read the whole project. Each took three of the six roles in spec 12.3 and could only read, not change, anything. Below is each finding, whether we confirmed it, and what we did about it.

| Role | Finding | Checked? | What we did |
|---|---|---|---|
| Tax accountant | Spouse aged 70+ never got the larger "elderly spouse" deduction. The number was in the YAML, but no code used it. | Confirmed (NTA p.55) | Fixed; test added |
| Tax accountant | Only the person labelled "head" could claim the spouse or children, or be covered on the other partner's insurance. | Confirmed (H3 at low head pay) | Fixed: the higher earner claims (Q23, labelled approximation) |
| Tax accountant | Resident-tax income limit for a spouse or dependant was 480,000. It is 580,000 from 令和8年度. | Confirmed (MIC p.28) | Fixed; whether it rises to 620,000 for 令和9年度 is still open (Q13) |
| Tax accountant | Part-timers below 88,000 a month pay no employment insurance here. | Plausible, but the rule is not in our sources | Recorded (Q24) |
| Tax accountant | Who counts as an "earner" for the NHI discount | Not in our sources | Recorded (Q25) |
| Tax accountant | Who deducts the spouse's national pension changes H4's wall | True; it is a choice | Recorded (Q26), asked the human |
| Maintainer | Some policy numbers are written in the code, not the YAML (breaks rule 1) | Confirmed | Recorded (Q28); proposed as its own task |
| Maintainer | Hand calculations come from the same author, so tests can be circular; no snapshot test; no outside calculator check | Partly | Snapshot test added; outside check still to do (spec 12.2); 17–20k gap with OpenFisca-Japan recorded (Q27) |
| Maintainer | `sources/text` is out of date | Not confirmed (17 text files for 19 tax files; the other 2 are images) | No change |
| Economist | Approximations not shown on the page (rule 3) | Confirmed | The page now lists every baseline approximation, each household's notes, and Daiwa's Q11/Q18 approximations |
| Economist | Daiwa shown as "complete" although its file has an open item | Confirmed | Shown with its approximations; human asked to approve them (H-12) |
| Economist | Daiwa's 56,500 comes from a formula that gives 52,000 under 2026 rules | Confirmed (Daiwa p.5 注1, p.6) | Recorded (Q29); H-10 reopened for the human (H-12) |
| Ruling-party staffer | The chart showed only Daiwa, with no word that the other designs were missing | Confirmed | A banner now names each design not drawn and why |
| Ruling-party staffer | One label, "incomplete parameters", hid three different reasons | Confirmed | Each design now shows its own reason: "waiting for Cabinet order", "this tool's data not ready", or "documents not obtained" |
| Ruling-party staffer | The government's 2027–28 package was labelled "Food tax cut" only | Confirmed | Labelled as the government's bridge package (food 1% + payment) |
| Ruling-party staffer | Red for the government design | Confirmed | Switched to a colour-blind-safe palette that carries no meaning |
| Ruling-party staffer | Daiwa's own estimates were kept for checking; the government's were not | Confirmed | Government's own figures added; its 1.6m recovery point is checked against our 1.65m (VALIDATION §7) |
| Opposition staffer | Name said "full refundable credit", which the source calls only a "first step" | Confirmed (outline p.1) | Renamed after the documents' own term (支援金制度の本格導入) |
| Opposition staffer | Who the government leaves out was not stated | Confirmed (Aug 5 資料3 p.3) | Stated in the design file and this log; H6 gets nothing |
| Opposition staffer | Food rate returns to 8% in FY2029 | True | Noted; FY2027–28 and FY2029 will be shown separately once numbers exist |
| Journalist | Axis cut at 300% hid the size of the big walls | Confirmed | Cut points are marked ▲ and show their true value on hover or tap |
| Journalist | H1's name promises a wall it does not face | Confirmed (Q21) | A note on the page; renaming H1 is the human's choice |
| Journalist | "Expensive" was an opinion word | Confirmed | Reworded with the numbers |

**Neutrality check:** no text recommends a design, party or politician.

**A lead that is true and checked (for later, not yet published).** Under 2026 rules, a part-time spouse in Shinjuku (H4) keeps about 280,000 yen less by earning 1,300,000 instead of 1,290,000. Their take-home pay does not get back to the 1,290,000 level until they earn 1,650,000. The government's own outline puts that recovery point at about 1.6 million. No design can be compared on this yet, because the government's amounts are not published.

**Results.** 88 tests pass. None of the eight households changed at their reference incomes; the fixes change only the wall maps.

### Milestone 5 checkpoint passed — 2026-11-01

**Decision recorded.** H-12: B.

**How Daiwa's credit is worked out now.** Daiwa did not pick 56,500 yen out of the air. It chose the credit so that nobody earning up to 1.78 million pays income tax. Without a basic deduction, a 1.78m salary leaves 1.78m minus the employment-income minimum as taxable income, and 5% of that is the credit.
- 2025 rules: (1,780,000 − 650,000) × 5% = 56,500. That is Daiwa's own number, and our formula reproduces it exactly.
- 2026 rules: the minimum rose to 740,000, so the same formula gives (1,780,000 − 740,000) × 5% = **52,000**.
- New Daiwa results: H1 +35,700; H3 −27,500; H7 −25,200; H8 −157,300 a year.

The page note explains that 2026 law already reaches the 1.78m threshold through a bigger basic deduction. So on 2026 rules, Daiwa's plan mainly swaps that deduction for a 52,000-yen credit plus a refund linked to social insurance.

**Approximations approved.** The human also approved two choices Daiwa leaves open, and both stay labelled wherever Daiwa numbers appear:
- the credit is taken off before the 2.1% reconstruction surtax (Q11);
- the refund cap counts only health insurance and pension (Q18).

Daiwa's file now has no unresolved items.

## Milestone 6 — 2026-11-01: website v1 (built; not yet published)

**What the site is.** Five pages in `site/`, Japanese by default with an English button. The choice is remembered on the device.
1. **Home**: one finding with its number, the wall map, and a household picker. The finding: when H4's part-time spouse earns 1,300,000 instead of 1,290,000, the household loses 280,126 yen a year, and gets back to the earlier level only at 1,650,000. The page works these numbers out from `outputs/wall_map.json` each time it opens, so they can never disagree with the data.
2. **Compare designs**: for the chosen household, a bar chart and a table with every design side by side. A design with no number yet says why.
3. **Methods**: shows `docs/METHODS.ja.md` (Japanese, new) or `docs/METHODS.md` (English).
4. **Validation**: shows `docs/VALIDATION.md`, with a short Japanese introduction.
5. **Sources and code**: shows `sources/SOURCES.md`, the repository link, and the commands that rebuild every number.

**How it is built.**
- Plain HTML and JavaScript; no build step.
- Charts use Chart.js. The documents are turned into web pages in the browser with `marked`. Both are loaded from public CDNs at exact versions.
- No tracking.
- Checked at phone width (375px), with no sideways scrolling, and in both languages with no errors.

**Known gaps.**
- The Validation and Sources tables are in English only.
- Each household's notes and the list of approximations come from the data files, which are written in English.

### Published — 2026-11-01 (HUMAN_TODO H-16)

**Who is named.** The commits are signed with the GitHub account name Iamodd5 and GitHub's private no-reply email. The earlier commits were rewritten before anything was pushed, so no real name appears anywhere in the public history.

**Which documents are in the public repository.** We read each publisher's terms of use.
- *Republishing allowed, with credit:* national ministries and agencies (Cabinet Secretariat, Children and Families Agency, MHLW, NTA, MIC, Statistics Bureau / e-Stat; they use the government's open-data licence), the Japan Pension Service ("free to reprint"), and Code for Japan's Scrapbox page (CC BY 4.0).
- *Not allowed without permission:* Daiwa Institute of Research, Shinjuku City, and 協会けんぽ. Their files are not in the public repository, and were removed from every earlier commit as well. `make all` downloads them from the publisher and checks their fingerprints (`sources/EXTERNAL.tsv`).
- *Pages that change on every download:* three 協会けんぽ web pages carry an anti-bot code that changes each time, so their original fingerprints are kept for the record but not checked.
- *Rengo:* the file was only a "site under maintenance" page, so it was dropped.

**Licence.** AGPL-3.0, as the spec says. We checked for side effects:
- It works with every library we use (OpenFisca is AGPL too; the others are MIT, BSD or Apache).
- It covers only our own code and documents, not the files in `sources/`.
- Anyone may reuse the code, but if they share a changed version, or run one as a website, they must publish their source too.
- It gives no warranty.

**Clean-clone test.** A fresh copy of the repository, set up from scratch, ran `make all`:
- it downloaded the 12 documents that are not stored in git, and their fingerprints passed;
- all 89 tests passed;
- `outputs/` came out byte-identical.

**Live at** https://iamodd5.github.io/-tedori-lab/

## Policy numbers moved into the YAML files — 2026-11-01 (Q28)

**What changed.** Before this, some policy numbers were typed straight into the Python code, and the YAML files only described them in words. Now the code reads every one of these numbers from `parameters/baseline_2026/`, and each number sits next to the page of the official document it comes from. Examples:

- Employment income: below 741,000 yen of pay there is no taxable employment income; from 741,000 to 2,190,999 it is pay minus 740,000; from 2,191,000 the NTA table is used; from 6,600,000 a formula (年末調整のしかた p.3, No.1410).
- The NHI discount for low-income households: 70%, 50% or 20% off the per-person part (Shinjuku reduction page).
- The resident-tax "no tax" lines: 350,000 × (family members + 1) + 310,000 for the per-person levy, + 420,000 for the income levy, 450,000 for a single person, 1,350,000 for a single parent (Shinjuku page).
- The age groups: spouse 70+, dependants 16+ and 19–22, health-insurance dependants 60+ and 19–22, long-term-care premiums at 40–64, NHI child levy from 18, the child allowance's under-3 rate and third-child rate.
- The spouse-deduction limits: no deduction if the earner's income is over 10 million; for resident tax, the higher amounts only up to 9 million.
- Rounding: taxable income down to 1,000 yen (both taxes), resident tax down to 100 yen.

**A new check.** A new test (`tests/test_parameters_used.py`) runs every household, a coarse wall map for each, and three made-up households that reach the rarer rules (a family with five children aged 1 to 21, one of them earning; a dependant aged 60+; a 50-million earner). It records every number the code reads. If a number in the YAML is never read, the test fails. That is how the elderly-spouse amount went unnoticed until the Milestone 5 review; it cannot happen silently now.

Seven numbers are kept in the YAML for the record but are not used, and the test lists each with its reason: a pension-table cell that repeats the next row, the elderly non-cohabiting dependant (no household has one), the resident-tax basic deduction headline (same as the first row of its table), the 25-million limit on the resident-tax adjustment credit (no household gets near it), the 51-employee and 20-hour tests (household files answer them yes/no), and the half-price NHI per-person amount for preschool children (no household has a preschool child in NHI).

**One number still in the code.** National pension covers ages 20 to 59, but no document in `sources/` says so. Following rule 2, the YAML marks it `status: unresolved` and OPEN_QUESTIONS Q30 asks for a source.

**Results.** No result changed: all tests pass, and `make all` rebuilds `outputs/` byte for byte the same.

## Milestone 7: the population view and cost — 2026-11-01

**Decision recorded.** H-17: A. Food spending and household counts both come from the 2024 全国家計構造調査 (National Survey of Family Income, Consumption and Wealth). Three other official tables are used only to check the result.

**What it does, in plain words.** Households H1–H8 are eight examples. To say something about the whole country, we need all 53.8 million households. We don't have data on each one, but the survey publishes a big table, one row per combination: kind of household (single, couple, couple with children, and so on) × income band (0–1 million, 1–1.5 million, …).

For each row the survey gives:
- how many households there are;
- their average earnings, business income and pensions;
- their average age;
- how many people in them work.

From each row we build one or a few "model households":
1. **Pension or work.** If 57% of a row's income comes from pensions, we say 57% of those households live on a pension (age 70) and 43% live on work. Both kinds get the row's full income, so they stay in the right band.
2. **One or two earners.** For couples who live on work, the survey's "number of earners" tells us what share of spouses also work. Only those spouses get the spouse earnings.
3. **Children.** Children under 18 are 10 years old. Older children are 22 and share the "other members' earnings".

Every model household then goes through exactly the same tax and insurance rules as H1–H8, under every design. Each one counts as many real households as its row stands for.

**Deciles.** We sort all households from lowest to highest annual income and cut them into ten groups of the same size. For each group we report:
- the average change in take-home pay;
- the share of households that gain, lose, or see no change.

**Cost.** We add up everyone's change in take-home pay. If households keep more, the government pays that much more. This is a "static" estimate: it assumes nobody changes how much they work.

**Checks against official numbers** (`docs/VALIDATION.md` §10):
- The household count is 2.8% below the other big survey's.
- The model's income tax total is 13% below the survey's own estimate, and resident tax 4% below.
- The decile boundaries are within 7% of the survey's own.
- The weak spot is people who earn very little: the model has far too many earners under 1 million yen, because averages spread small salaries around (Q33).

**What we changed along the way.** The first version split each row by the share of people aged 65+. That gave almost every pensioner a small salary: 35.8 million "earners" under 1 million yen, against 3.7 million in the tax agency's count. So the split now follows the income itself (pension or work). The test and the hand calculation were rewritten with it, and the change is noted in both. An arithmetic slip in the first hand calculation was also caught by its test and is noted.

**Daiwa result (approximate).**
- On average, the lowest four deciles gain a little (about +4,000 to +9,000 yen a year), and the top deciles lose (−52,000 and −86,000 in the top two).
- In total, income tax rises by 1.53 trillion yen and 0.58 trillion is paid back as refunds, so the government collects about 0.95 trillion more.
- Daiwa's own estimate on 2025 rules was +0.7 trillion tax and 0.7 trillion refunds. The difference comes mainly from the larger 2026 basic deduction that the design removes.
- The other designs still cannot be calculated (their amounts are unpublished or their documents are missing). The page says why.

**New open questions.**
- Q32: a larger deduction for elderly dependants is not in the engine yet.
- Q33: earnings of other household members are spread too thin.

**Results.** 96 tests pass. The earlier outputs (H1–H8, wall maps) did not change. New files: `outputs/population.json`, `outputs/population_households.csv`, and the page `site/population.html`.

## Plain-language rewrite of the website text (2026-11-01)

The human reviewed the site and said the text was too hard to read. Every sentence a visitor sees on Home, Compare plans and All households was rewritten in everyday words, in both languages. No number changed.

- Internal codes (Q13, HUMAN_TODO H-8, `outputs/`, "decile", "baseline") no longer appear on the site. The codes stay in the YAML files as comments, so each note can still be traced.
- The notes about each example household and the approximations behind every number used to show in English only, even in Japanese mode. They are now in both languages (`{ja, en}` in `households/*.yaml`; a new `site: {ja, en}` text on each approximation in `parameters/baseline_2026/`).
- `scripts/build_outputs.py` now stops with an error if a baseline approximation has no `site` text, so a new approximation cannot reach the site unlabelled (CLAUDE.md rule 3).
- Plan names are now plain: for example "Daiwa Institute plan (adjusted to 2026 tax rules)" instead of "Daiwa (recomputed on 2026 rules)".
- Not yet rewritten: the How it works, Checks and Sources pages, which show `docs/METHODS*.md`, `docs/VALIDATION.md` and `sources/SOURCES.md` as written.

96 tests pass.

### Follow-up: vague words made specific (2026-11-01)

The human said the text still had ambiguous references and vague abstractions. Changes:
- The Home page now says what is being compared (plans to lower the tax and insurance working people pay) and describes each of the four plans in one paragraph. The descriptions are in each plan's file (`summary` in `parameters/designs/*.yaml`), so the All households page shows the same text for the chosen plan.
- "2026 rules" is defined on each page: the rules actually in force in 2026, before any plan.
- Unnamed limits and tables now have numbers or names: the student's ¥1.5m dependant limit (ages 19–22), Shinjuku's fiscal 2025 guide, the rounding rule and its maximum effect, and which insurance rates change in March or April.
- "Not calculated" reasons say what is missing (payment amounts and income limits; food spending for H1–H8; Rengo's documents).
- Cost rows say exactly what they count (income tax after any credit; cash paid out).

No number changed; 96 tests pass. H1 is still named "near the 1.3m wall" although that wall does not apply to it (Q21, a human decision).

Published on 2026-11-01 (H-18). A final pass that rewrites all site text and improves the UI is planned once every other milestone is done (H-19).

## H-4, H-13, H-14 (2026-11-01)

**H-4: Rengo's documents found.** Rengo's proposal page was still "under maintenance", but two Rengo documents were available at other addresses: its Tax Reform Plan (税制改革構想, May 2025) and its 2026 key policies (重点政策), which Rengo gave to the government's National Council on Social Security on 2026-05-19. Rengo's plan has two parts:
- **Work-support credit (就労支援給付制度).** Employees earning ¥740,000–¥2.5m in salary have half of the social and employment insurance they pay taken off their income tax. If that amount is bigger than their income tax, the rest is paid in cash. It shrinks above ¥2m and is gone at ¥2.5m. Two details are not stated: whether it shrinks in a straight line (Q34), and whether long-term care and the child-support levy count (Q35). Rengo's own example also does not match its rule: it shows ¥152,000 where the rule gives ¥148,700 (Q36), so it is not used as a test.
- **Consumption-tax refund (消費税還付制度).** People too poor to pay income tax get a fixed amount, depending on how many people they support. No amounts are published (Q3), so Rengo still cannot be calculated. The site now gives that reason.
- Rengo states no terms that allow copying its files, so they are not in git. `make` downloads them. The download now sends a browser user agent, because the government site refuses curl's default one.

**H-13: who deducts a spouse's national pension.** The human chose the main earner. In a couple, the partner with the higher income now deducts the other partner's National Pension, as 所得税法74条 allows when you pay it for them. It is labelled as an approximation on every page, together with the existing rule that the same partner claims the spouse and children (Q23).
- H4's drop at ¥1.3m is now ¥258,226 a year (was ¥280,126), so the rate there is 26.8226 (2,682%). The hand calculation was added first, with a corrected slip in the final division, then the test, then the code.
- H1–H8 at their usual incomes did not change.
- In the population model, about 31,000 households changed: couples where the main earner is not in company insurance and the spouse has no income. Their 2026 numbers are unchanged, because the main earner pays no income tax anyway. Under Daiwa's plan they get a slightly larger refund. Daiwa's net result moves by less than ¥0.001 trillion; decile 2 rises by ¥8 and decile 3 by ¥38.

**H-14: H1 renamed.** H1 is now "Single part-time employee (¥1.25m a year)" (was "near the 1.3m wall", which does not apply to someone who lives alone). The numbers did not change.

96 tests pass.

## Milestone 8: Build your own plan (2026-11-01)

**What it is.** A new page, "Build your own" (自分で案を作る). A visitor moves five sliders to set the rules of a simple tax credit paid in cash to working people. The page shows straight away:
- what it does to an example household's take-home pay at every income (the same charts as Home, with "your plan" next to 2026 rules);
- how much households in each income group get on average, and what share of them get anything;
- what it costs the government in a year.

**The rule, in plain words.** Everyone who earns money (wages or a business) gets a share of their earnings, the "phase-in rate", up to a maximum. In a couple, the one who earns more also gets an extra amount for each child aged 18 or under. Once a person's income before tax (earnings plus pensions) passes a level the visitor sets, the credit shrinks by the "phase-out rate" for every yen above that level, down to zero. The money is simply added to take-home pay: it isn't taxed and nothing else changes.

Example with the starting values (10%, ¥100,000 maximum, ¥50,000 per child, phase-out from ¥3m at 5%): a single parent earning ¥2.5m with one child gets 10% × 2.5m = 250,000, capped at 100,000, plus 50,000 for the child = ¥150,000.

**Why the browser can do it.** The spec says the site has no server. Because the credit doesn't change any tax, the browser only needs the credit formula (`site/custom.js`) and the 2026 numbers we already compute (`outputs/wall_map.json`, plus a new `outputs/builder.json` with each household's earnings and pensions).

**How we know it's right.** A hand calculation (`tests/hand_calcs/custom_credit.md`) with 10 cases checks the Python version. Then the tests run the browser's JavaScript in Node on the same cases and on all 730 model households, and check that it gives the same answers as Python. 108 tests pass.

**Also fixed.** The charts now say whose income moves (for example "Spouse's salary before tax" for H4). Before, the axis said only "income", which was unclear for couples. The same fix applies on Home.

**Neutrality.** The starting values are placeholders, the same as the test values. They come from no plan, and the page says so.

## Readability pass: charts and first-time visitors (2026-11-01)

The human said both Home charts were unreadable, and asked us to go through the site as an average person in Japan who has just heard about it, and fix every place they would get lost. No number in `outputs/` changed except new fields used for display; 110 tests pass.

**The two charts (Home and Build your own).**
- The take-home chart squeezed ¥0–¥10 million into one small box, so the walls were tiny notches. Now buttons choose the income range (0–¥3m, 0–¥6m, 0–¥10m), starting near the household's own income, and the vertical axis fits what is shown. A circle marks the household's income now. Touching a line shows the take-home pay and the difference from 2026 rules.
- The second chart showed the share of each extra ¥10,000 lost. Tax is rounded to ¥100 and insurance rises in steps, so the line was a band of black noise. It now shows the share of each extra **¥100,000** lost, as steps, with a dotted 100% line: above it is a wall. It is worked out in the browser from the same take-home numbers (`site/walls.js`, tested in `tests/test_site.py`).
- Each chart has an "Enlarge" button that fills the screen, on phones too. The axes use short labels (300万 / ¥3m). The charts are taller.
- Above the charts, the biggest walls are listed in words, for example: "If the spouse's salary goes from ¥1,290,000 to ¥1,300,000, the household takes home ¥258,226 less a year. Take-home gets back to where it was at ¥1,640,000." Only the three biggest are listed; the many small dips from insurance steps are counted in one line.

**Where a first-time visitor got lost, and what changed.**
- *"What is this site? What is a refundable tax credit?"* Home now explains both in two sentences and has three buttons: compare plans, see all households, build your own.
- *Four long paragraphs about the plans.* Each plan is now one line with a "calculated" or "can't calculate yet" tag; click it for the full description.
- *"What does this household earn?"* Every page with an example household now shows each person's income (for example "Head (45): salary ¥5,000,000 / Spouse (43): salary ¥1,000,000").
- *Compare page: three of four rows said "can't calculate", and the chart had empty rows.* The result now comes first in plain words (for example "Daiwa: +¥35,700 a year, +3.4%"). The chart and table show only plans that can be calculated, and the others are listed with their reasons.
- *All households page: ten bars with no meaning attached.* A short list of findings now comes first, worked out from the numbers (which groups gain or lose on average, the most in each direction, the total for the government). Each group's label shows its average income. Units are on every number. The table, the plan's assumptions and the list of approximations are folded away under clear headings; the "(Approximation)" label stays visible on each.
- *Build your own: slider names like "phase-in rate".* They now say "how fast it grows (% of earnings)", "most one person can get" and so on, with an example under each. A small chart next to the sliders shows what one person gets at each salary under your settings.
- *How it works, Checks, Sources: long technical documents.* Each page now starts with a few plain bullet points. The full document is still there, folded under "for specialists".
- Rebuilding the site now needs Node.js as well as Python (the tests run the site's JavaScript); README and the Sources page say so.

The final full rewrite of all text and the UI (H-19) is still planned for after the other milestones.

### Follow-up: the second wall chart in yen (2026-11-01)

The human said the "How much of each extra ¥100,000 you lose" chart was still hard to understand, especially the tooltip ("Earning … instead of …"). It is now a question with an answer in yen: **"Earn ¥100,000 more: how much more do you take home?"** Normally the answer is a bit under ¥100,000. Where the line falls below the dotted ¥0 line, earning more leaves you with less: that is a wall. The tooltip now says, for example, "If the spouse's salary goes from ¥1,200,000 to ¥1,300,000 — 2026 rules: take-home pay goes down by ¥176,226 (a wall)". A crash when hovering near the dotted line was also fixed. 110 tests pass.

## Milestone 9: the report (2026-11-01)

**What it is.** A short report in Japanese and English, on the new Report page (レポート) and in `outputs/report.ja.md` / `outputs/report.en.md`. It has: the main finding, what the four plans are and which can be calculated, the eight example households under the one plan that can be calculated (Daiwa), the all-household estimate, the limits, and every approximation behind the numbers.

**The main finding (one sentence with its number).** Under 2026 rules, if a part-time spouse's pay goes from ¥1,290,000 to ¥1,300,000 a year (household H4), the household takes home ¥258,226 less a year, and the spouse has to earn ¥1,640,000 to get back to the same take-home pay. It is the same finding as the Home page. It is about today's rules, not any one plan, and it comes from a hand calculation (`tests/hand_calcs/wall_H4.md`).

**How the numbers get in.** The text is in two templates, `report/report.ja.md` and `report/report.en.md`, with named blanks such as `{lead_drop}`. `scripts/build_report.py` fills every blank from the files in `outputs/`, the same files the website reads. `make all` now builds the report too. Three tests (`tests/test_report.py`):
- the main finding matches the hand calculation;
- the templates contain no numbers of their own, only years, the edition month, household names (H1–H8) and the "10 groups";
- the saved report is current.

**Review before showing it (spec 12.3, report only).**
1. *OpenFisca-Japan maintainer:* every number is generated and tested; nothing is typed by hand.
2. *Tax accountant:* the main finding and the H1–H8 table are the same numbers as the hand-checked site. The H4 wall uses the H-13 decision (the main earner deducts the spouse's National Pension), which is listed among the approximations.
3. *Ruling-party staffer:* the government plans are described in their own documents' terms, and the reason they can't be calculated is the government's own ("set later by Cabinet order"). The main finding is about today's rules, not a criticism of any plan.
4. *Opposition staffer:* no wording favours the government plans; the report says they can't be calculated yet.
5. *Economics journalist:* the main finding is one sentence with a concrete number and is true. It may not be new to readers who already know the "¥1.3m wall"; the exact cost (¥258,226, and ¥1,640,000 to recover) is the new part. Other possible leads are listed for the human (H-20).
6. *Public-finance economist:* all-household numbers are marked "(Approximation)", the calibration gaps are stated (households 2.8% fewer, income tax 12.6% lower, resident tax 3.6% lower), and so are the static assumption and the one-municipality limit. Daiwa's own estimate is shown next to ours, with the reason the two differ.
- One wording change from the review: "the wall remains even under Daiwa's plan" became a plain statement of the Daiwa numbers at the same point, so it doesn't read as a judgement.

113 tests pass. The report is not published yet: it waits for the Milestone 9 checkpoint (H-20).

## Design pass: look, navigation and chart zoom (2026-11-02)

The human asked for a simpler but better-looking site, easier navigation, and a better zoom on the charts. Nothing in `outputs/` changed.

- **Look.** One idea runs through the site: a Japanese payslip (給与明細). Ruled rows, labels on the left, money on the right in evenly spaced digits. Colour means one thing each: indigo for anything you can click or have selected, red only for a wall or a loss, green for a gain. The font is BIZ UDPゴシック, the universal-design font used by many Japanese public bodies, where the device has it, otherwise Hiragino or Noto Sans JP (nothing is downloaded, so there is no tracking).
- **Home.** The main finding is now shown as a payslip: "the part-time spouse earns more: +10,000円" over "the household's take-home pay: −258,226円" in red. The card grid became a ruled list of things to do.
- **Navigation.** The header keeps only the five main pages (Home, Compare plans, All households, Build your own, Report). How it works, Checks and Sources & code moved to the footer on every page. On a phone the menu scrolls sideways, and a fade at the right edge shows there is more.
- **Zoom on the wall charts** (`site/walls.js`, Home and Build your own):
  - drag across a chart with a mouse, or spread two fingers on a phone, to zoom in;
  - an overview strip shows the whole ¥0–10m line, with a frame you can drag to move or pull at its edges to resize (arrow keys and +/− also work);
  - the range buttons and double-click take you back;
  - both charts always show the same incomes, and the vertical axis fits what is shown, so a wall fills the chart when you zoom in on it;
  - "Full screen" opens the whole chart area, controls included; Esc closes it.

113 tests pass. The human approved the design on 2026-11-02 (H-21). Not published yet: it goes out together with the Milestone 9 report once H-20 is answered.

## Milestone 9 checkpoint passed (2026-11-02)

The human read the report and chose its main finding: option A, the ¥1.3m wall for example household H4 (the part-time spouse earns ¥10,000 more and the household takes home ¥258,226 less a year). The report already led with it, so nothing in it changed. The report and the design pass are now published together (H-20).

## Milestone 10 (started 2026-11-02): corrections log and a self-check before outside review

Milestone 10 is about fixing what outside reviewers find, and keeping a public list of every fix. The outside review needs people the human knows, so it starts with the request in `docs/REVIEW_REQUEST.md` (Japanese and English). Before sending it, we checked our own published numbers.

- **Corrections log, live.** A new page, 訂正の記録 / Corrections, linked from the footer of every page. It lists every time we changed a published number or statement because it was wrong or misleading: the date, what changed, why, the numbers before and after, and links to the versions before and after. It is written in `docs/CORRECTIONS.yaml`; `make all` copies it to `outputs/corrections.json` for the page. To find what to list, we compared the output files of every version ever published. Four corrections so far:
  1. The H4 ¥1.3m wall: who deducts the spouse's national pension (decided 2026-11-01). The drop went from ¥280,126 to ¥258,226.
  2. H1's old name said "near the 1.3m wall", which does not apply to a single person.
  3. The reason the Rengo plan can't be calculated (its documents were found; its refund amounts are missing).
  4. A wrong range on the Checks page (below).
  A test recomputes every "before" and "after" number from the published versions, so the log can't misquote them.
- **A wrong number found and fixed.** The Checks page said OpenFisca-Japan's resident tax is "¥17,000–20,000 lower" than ours. The comparison table shows 12,982–19,937 for the four people who pay more than the flat per-person levy. The page now calculates the range from the output files.
- **The OpenFisca-Japan comparison is now rebuilt by `make all`** (`scripts/crosscheck_openfisca.py` → `outputs/openfisca_check.json`). It reproduced the old table exactly. A test checks the table in `docs/VALIDATION.md` against it, and another checks the population calibration tables there against `outputs/population.json`, so the Checks page can't drift from the numbers.
- **The Checks page summary has no numbers typed by hand any more**: the calibration gaps and the ¥1m-earner counts come from `outputs/population.json`.

123 tests pass. Waiting for the outside review (H-22).
