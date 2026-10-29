# Tedori Lab (手取りラボ): Build Spec for Claude Code

> **Kickoff prompt:** "Read `TEDORI_LAB_SPEC.md` in full. Then do Milestone 0 only, and stop at its checkpoint."
>
> **Resume prompt (any later session):** "Read `SPEC.md`, `CLAUDE.md` and `docs/HUMAN_TODO.md`. Then continue from the next unfinished milestone."

---

## 0. How to use this file

- This file is the single source of truth for the project. Save it as `SPEC.md` at the repository root and keep `CLAUDE.md` (Section 2) next to it.
- Work milestone by milestone (Section 11). At every **CHECKPOINT**, stop, summarize what was done, and wait for the human.
- Whenever the human must do or decide anything, follow the **Human handoff protocol (Section 13)** exactly: notify, then give precise step-by-step instructions. The human is a high school student who may not be watching the terminal.
- When anything is unclear or a number is missing, do not guess. Add it to `OPEN_QUESTIONS.md` and continue with the parts that are clear.

---

## 1. Mission

Build an open, bilingual (Japanese and English) web tool that compares every proposed design of Japan's **refundable tax credit (給付付き税額控除)** and the **food consumption tax cut (飲食料品の消費税減税)**, using one consistent method, for typical household types and for the population by income decile.

Tagline: **Every proposal, your household, one method. (どの案でも、あなたの世帯で、同じ方法で。)**

Context the tool must reflect:
- The government set up the Social Security National Council (社会保障国民会議) in February 2026 to design the credit.
- On July 13, 2026, its working group received a final government draft aimed at full introduction in FY2029. Reported features: support rises gradually up to a certain income, with an addition per dependent child.
- A food consumption tax cut has been proposed as a two-year bridge (reported ruling-party plan: 8% to 1% from April 2027, contested).
- Competing designs exist from Rengo (連合) and Daiwa Institute of Research (大和総研).

Exact parameters must come from primary documents (Section 6), never from this summary.

---

## 2. `CLAUDE.md` (create this file at the repo root on day 1)

```markdown
# Rules for this repository

1. Every policy parameter lives in a YAML file under `parameters/` and cites its source:
   document title, URL, page number, and the date the document was published.
2. Never invent, round, or "reasonably assume" a policy number. If a value is missing
   or ambiguous, add it to OPEN_QUESTIONS.md and mark the parameter `status: unresolved`.
3. Any approximation (for example consumption-tax incidence or population weighting)
   must be labelled `approximation: true` with a one-line explanation, and the label
   must be shown wherever the number appears on the website.
4. Tests come before rules. Each rule needs at least one test built from an official
   worked example or a hand calculation documented in `tests/hand_calcs/`.
5. Never edit a test to make it pass. Fix the rule, or record the conflict in OPEN_QUESTIONS.md.
6. Each policy design is its own reform file. The 2026 baseline is never edited to model a reform.
7. Every number on the website must be reproducible with `make all` from a clean clone.
8. Neutrality: the same households, data and method for every design. Outputs state
   findings only. No text recommends a design, party, or politician.
9. Prefer contributing to OpenFisca-Japan over duplicating it. If a needed rule is missing
   there, implement it in a way that can be offered upstream as a pull request.
10. After each milestone, write a plain-language summary in `docs/LOG.md` that a high school
    student could use to explain every rule implemented, without reading code.
11. Whenever human input or action is needed, stop and follow the Human handoff protocol
    in SPEC.md Section 13: add the task to docs/HUMAN_TODO.md, then end your turn with a
    HUMAN ACTION REQUIRED block. Never bury a request for the human inside a long summary.
```

---

## 3. Scope

**In scope (v1, by day 14)**
- 2026 baseline: income tax, resident tax, employee social insurance (health, pension, employment), national health insurance and national pension for the self-employed, child allowance.
- Four designs: government final draft, Rengo proposal, Daiwa proposal, food consumption tax cut.
- A custom design builder (sliders) for a generic refundable credit.
- Eight household archetypes (Section 7).
- Population view by income decile (approximate, Section 9.3).
- Static bilingual website (Section 10).
- Short report (Japanese and English) generated from the same outputs.

**Out of scope for v1**
- Behavioral responses (people changing hours worked). Static, no-behavior estimates only, stated clearly.
- Local variations in national health insurance premiums beyond one reference municipality (choose one and state it).
- Government microdata (individual survey records).

---

## 4. Repository layout

```
tedori-lab/
  SPEC.md                  # this file
  CLAUDE.md                # rules (Section 2)
  OPEN_QUESTIONS.md        # anything unresolved
  Makefile                 # make all = fetch-check, test, run, build site
  sources/                 # downloaded primary documents (PDF/HTML/CSV) + SOURCES.md index
  parameters/
    baseline_2026/         # YAML, one file per rule area
    designs/
      government_final.yaml
      rengo.yaml
      daiwa.yaml
      food_tax_cut.yaml
      custom_template.yaml
  households/              # 8 archetype YAML files
  engine/                  # Python package: wraps OpenFisca-Japan + reform loader
  population/              # synthetic households + weighting
  outputs/                 # generated CSV/JSON (never hand-edited)
  tests/
    hand_calcs/            # documented hand calculations
  site/                    # static website source
  report/                  # report templates (JA + EN)
  docs/
    LOG.md
    METHODS.md
    VALIDATION.md
    COVERAGE.md
```

---

## 5. Tech stack

- Python 3.11+, OpenFisca-Core, OpenFisca-Japan (GitHub: `project-inclusive/OpenFisca-Japan`), pandas, pytest.
- If OpenFisca-Japan cannot be installed or lacks needed rules, implement the missing rules as a separate OpenFisca extension in `engine/`, structured so it can be upstreamed. Record the decision in `docs/LOG.md`.
- Website: static site (plain HTML/JS or a lightweight static generator), charts with a small library (for example Observable Plot or Chart.js). Must work on a phone. No backend; the design builder runs on precomputed grids or a small JS port of the credit formula only (the credit formula, not the whole tax system).
- License: AGPL-3.0 (compatible with OpenFisca).
- Hosting: GitHub Pages or any free static host.

---

## 6. Primary sources (download into `sources/`, index in `sources/SOURCES.md`)

| Area | Where to look | What to extract |
|---|---|---|
| Government credit design | Cabinet Secretariat, Social Security National Council materials: https://www.cas.go.jp/jp/seisaku/kokuminkaigi/ (meeting pages under `contents/`, including the working-group meetings of May 27 and July 13, 2026) | All parameters of the final draft: eligibility, income definition, phase-in rate, maximum amount, plateau, phase-out, child additions, interaction with tax and social insurance, timing |
| Rengo design | https://www.jtuc-rengo.or.jp/activity/seisaku_jitsugen/teigen/?p=5465 and linked documents | Consumption-tax refund component and work-support benefit (refund of half of low-income workers' social insurance contributions); parameters |
| Daiwa design | https://www.dir.co.jp/report/research/law-research/tax/20251010_025349.pdf | "Social-insurance-refundable tax credit" parameters and their published estimates (use estimates only for cross-checking) |
| Food consumption tax cut | Council materials and party proposals as published | Rate change, start date, duration, goods covered |
| Income tax and resident tax 2026 | National Tax Agency (国税庁) official guides and worked examples; Ministry of Internal Affairs and Communications for resident tax | Employment income deduction, basic deduction (2026 rules), spouse and dependent deductions, rate schedule, resident tax rates and per-capita levy |
| Employee social insurance | Japan Health Insurance Association (協会けんぽ) premium tables (choose Tokyo, state it), Japan Pension Service (日本年金機構) contribution rates, employment insurance rates | Rates, caps, standard monthly remuneration bands, coverage thresholds (including the 1.06 and 1.3 million yen walls and any 2026 changes) |
| National health insurance and pension | One reference municipality's NHI rules (state which), Japan Pension Service | Premium formula, flat national pension contribution |
| Child allowance | Children and Families Agency (こども家庭庁) | 2026 amounts by child age and order |
| Household spending | e-Stat, Family Income and Expenditure Survey (家計調査), spending by income quintile or decile | Food spending and total taxable consumption by income group, for consumption-tax incidence |
| Population weighting | e-Stat, Comprehensive Survey of Living Conditions (国民生活基礎調査) and/or National Survey of Family Income, Consumption and Wealth (全国家計構造調査) published tables; NTA Statistical Survey of Actual Status for Salary (民間給与実態統計調査) | Household counts by type and income band; wage earners by income band (for calibration checks) |
| Existing tool | OpenFisca-Japan repository, docs, and Code for Japan design notes (https://scrapbox.io/c4j/OpenFisca-Japan_MCP) | What is implemented, how variables and parameters are structured, whether reforms can be exposed via its MCP server |

If a document cannot be fetched, record the URL in `OPEN_QUESTIONS.md` and ask the human to download it.

---

## 7. Household archetypes

Create one YAML file per household with: members, ages, employment type (employee / self-employed / pensioner / student), annual earned income per member, pension income, number and ages of children, municipality for local rules, and annual spending (food and other taxable consumption) derived from the Family Income and Expenditure Survey for their income group. Every derived value cites its table.

| ID | Household | Why it matters |
|---|---|---|
| H1 | Single part-time employee near the 1.3 million yen wall | Income walls |
| H2 | University student with a part-time job, dependent of parents | Dependent deduction rules |
| H3 | Dual-income employee couple, two children (one under 3, one in elementary school) | Typical working family |
| H4 | Single-earner employee, spouse working part-time | Spouse deductions and walls |
| H5 | Single parent employee, one child | Low-income support |
| H6 | Pensioner couple, both 70+ | Pension taxation, consumption-tax exposure |
| H7 | Self-employed (freelancer), single | NHI and national pension instead of employee schemes |
| H8 | High-income dual-earner couple, one child | Who gains at the top |

Incomes for H1 to H8: pick a reference income for each, and also run each household across an income grid (Section 9.2).

---

## 8. Policy designs

Each design is a reform file applied on top of `baseline_2026`. Required fields: `name_ja`, `name_en`, `source`, `start_year`, `parameters`, `status` (`resolved` / `unresolved`), and `notes`.

1. **government_final**: the July 13, 2026 final draft as published in council documents.
2. **rengo**: consumption-tax refund plus work-support benefit, per Rengo's documents.
3. **daiwa**: social-insurance-refundable tax credit, per Daiwa's report.
4. **food_tax_cut**: reduced rate on food as proposed; incidence approximated from household food spending (assume full pass-through to prices as the baseline assumption, and state it; optionally show a 50% pass-through sensitivity).
5. **custom**: a generic refundable credit with user-set phase-in rate, maximum, plateau end, phase-out rate, and per-child addition.

If a parameter of any design is not stated in the sources, mark it `unresolved`, show the design on the site with a visible "incomplete parameters" note, and list it in `OPEN_QUESTIONS.md`.

---

## 9. Outputs (all generated into `outputs/` as CSV and JSON)

### 9.1 Household comparison
For each household × design: annual change in disposable income (yen) versus baseline, broken into components (tax change, credit or benefit received, social insurance change, consumption-tax change).

### 9.2 The wall map (signature chart)
For each household type, across an income grid from 0 to 10 million yen in 10,000-yen steps: disposable income and the **effective marginal rate** (share of each extra 10,000 yen lost to tax, social insurance, and benefit withdrawal). Baseline versus each design. The walls must be visible as spikes.

### 9.3 Population view (approximate)
- Build synthetic households by household type and income band from published tables, then weight them so that counts match official totals.
- Output: winners, losers, and average change by income decile; total gross cost per design.
- Check: weighted totals (number of wage earners by income band, total households) against official statistics; report the gaps in `docs/VALIDATION.md`.
- Every population number on the site carries the label "approximation".

### 9.4 Cost
Total gross fiscal cost per design (approximate), with the method in `docs/METHODS.md`. Where a source publishes its own cost estimate, show it next to ours for comparison.

---

## 10. Website

Bilingual (Japanese default, English toggle). Pages:

1. **Home**: one-sentence lead finding with its number, the wall map, and a "pick your household" selector.
2. **Compare designs**: table and bar chart of 9.1 for a selected household; all four designs side by side.
3. **Design builder**: sliders for the custom credit; shows the resulting wall map and change by decile (precomputed grids or the JS credit formula).
4. **Population**: decile chart and cost, labelled approximate.
5. **Methods**: plain-language method, assumptions, limitations (no behavioral response, reference municipality, consumption-tax pass-through).
6. **Validation**: hand-calculation comparisons and calibration gaps, including mismatches.
7. **Sources and code**: every source with link, plus the repository link and the run command.
8. **Corrections log**: dated list of every correction.

Requirements: loads fast on a phone, accessible chart labels, every number traceable to an output file, no tracking beyond simple privacy-friendly analytics.

---

## 11. Milestones (14 days)

| # | Day | Deliverable | Acceptance criteria |
|---|---|---|---|
| 0 | 1 | Notification hooks set up and tested (Section 13.1), `docs/HUMAN_TODO.md` created, repo scaffold, `CLAUDE.md`, `SOURCES.md` with all Section 6 documents downloaded or listed as missing; `docs/COVERAGE.md` mapping OpenFisca-Japan coverage | Human confirms a test notification arrived; **CHECKPOINT**: human reviews sources and coverage |
| 1 | 1 to 2 | All four designs' parameters extracted into YAML with citations | Every parameter cited or marked unresolved; **CHECKPOINT** |
| 2 | 2 | Baseline 2026 for H1 to H8 with tests | Matches hand calculations within 1,000 yen per year for at least 5 households |
| 3 | 3 to 4 | All four designs implemented as reforms; first upstream-ready contribution identified | All designs run on all households; tests pass |
| 4 | 5 | Wall map and household comparison outputs | Charts render from `outputs/`; walls visible in baseline |
| 5 | 6 | Adversarial self-review (Section 12.3) and fixes | Review notes and fixes logged in `docs/LOG.md`; **CHECKPOINT** |
| 6 | 7 | Website v1 (pages 1, 2, 5, 6, 7) | Deployed; works on a phone |
| 7 | 8 | Population view and cost | Calibration gaps reported; labelled approximate |
| 8 | 8 | Design builder page | Sliders update wall map and deciles |
| 9 | 9 | Report (JA and EN) generated from outputs | One lead finding with its number; no recommendations; **CHECKPOINT** |
| 10 | 10 to 12 | Fixes from outside review; corrections log live | All corrections addressed |
| 11 | 13 | Press kit: 3 charts (PNG/SVG) and a one-page Japanese summary, generated from outputs | Every number matches the site |
| 12 | 14 | Public release | `make all` reproduces everything from a clean clone |

---

## 12. Validation and testing

### 12.1 Tests
- Unit tests for every rule, built from NTA worked examples or documented hand calculations.
- Regression tests that snapshot `outputs/` and fail on unexplained changes.

### 12.2 Cross-checks
- Take-home pay for H1, H3 and H8 at three income levels compared against at least one reputable public calculator; differences explained in `docs/VALIDATION.md`.
- Where Daiwa or the government publish example households or costs, compare and explain differences.

### 12.3 Adversarial self-review (Milestone 5, and before every release)
Review the work successively in each role and log findings:
1. OpenFisca-Japan maintainer: code quality, tests, upstream fit.
2. Certified tax accountant (税理士): wrong rules or numbers.
3. Ruling-party Diet staffer: bias against the government draft.
4. Opposition Diet staffer: bias toward the government draft.
5. Economics journalist: is the lead finding clear, true, and newsworthy?
6. Public-finance economist: weak method, overclaimed results.

### 12.4 Release checklist
- [ ] Every parameter cited or marked unresolved and shown as such
- [ ] Baseline within 1,000 yen of hand calculations for at least 5 households
- [ ] Same households, data and method for every design
- [ ] Approximations labelled everywhere they appear
- [ ] No text recommends a design, party or politician
- [ ] `make all` reproduces the site from a clean clone
- [ ] `docs/LOG.md` explains every rule in plain language

---

## 13. Human checkpoints and handoff protocol

Stop and ask the human before:
- Choosing between conflicting sources for any parameter.
- Choosing the reference municipality, income grid, or household reference incomes.
- Publishing anything (site, report, press kit).
- Opening any issue or pull request on OpenFisca-Japan (the human submits it under their own account).
- Any wording on the site that describes a political party or politician.
- Anything that needs the human's accounts, money, or identity (GitHub repo creation, GitHub Pages, domain, analytics, email).
- Any milestone CHECKPOINT in Section 11.

Also stop if you are blocked: a source cannot be downloaded, a tool will not install, or a test conflict cannot be resolved without a judgment call.

### 13.1 Notifications (set up in Milestone 0)

The human may not be watching the terminal, so set up Claude Code hooks that send a desktop notification when you stop and wait.
1. Check the current Claude Code hooks documentation (https://docs.claude.com, "Hooks") for the exact `.claude/settings.json` format. Do not rely on memory.
2. Detect the operating system and use its native notifier: macOS `osascript -e 'display notification "..." with title "Tedori Lab" sound name "Glass"'`, Windows a PowerShell toast (BurntToast or `New-BurntToastNotification` if installed, otherwise a `System.Windows.Forms` balloon), Linux `notify-send`.
3. Add hooks for the `Stop` event (turn finished) and the `Notification` event (Claude Code waiting for permission or input). Message: "Tedori Lab: your action is needed. Check the terminal."
4. Fire one test notification and ask the human to confirm it arrived. If it did not, troubleshoot (OS notification permissions for the terminal app, Focus/Do Not Disturb) and write the fix in `docs/LOG.md`.
5. Optional, only if the human asks: a phone notification via a free service such as ntfy.sh. Ask before adding any third-party service.

### 13.2 The HUMAN ACTION REQUIRED block

Every time you need the human, end your turn with this block and nothing after it. Write in plain English (add Japanese only if the human asks). Assume no prior knowledge of git, the terminal, or tax law.

```
==================== HUMAN ACTION REQUIRED ====================
Task ID: H-<number>               Milestone: <n>      Est. time: <minutes>
Type: DECISION | ACTION | REVIEW | BLOCKED

WHAT I NEED: <one sentence>

WHY: <one or two sentences on what breaks or stays wrong without it>

STEPS:
1. <exact click, URL, command, or file to open; one action per step>
2. ...
(Commands go in their own code lines, ready to copy and paste.)

FOR DECISIONS, THE OPTIONS:
A) <option> : consequence
B) <option> : consequence
My suggestion: <A or B> because <reason>. (For political wording, give no suggestion.)

WHAT TO REPLY: <the exact words or format, e.g. "H-3: A" or "H-3 done">

WHILE YOU DO THIS: <what I will work on next, or "I am paused">
================================================================
```

Rules for the block:
- One block per turn. If several things are needed, list the most urgent and point to `docs/HUMAN_TODO.md` for the rest.
- Every step must be specific enough to do without asking a follow-up question. Give full URLs, exact file paths, exact menu names, and exact commands.
- For REVIEW tasks, say exactly what to check and what "looks right" means (e.g. "Open `tests/hand_calcs/H1.md`. The take-home pay on line 12 should be between ¥X and ¥Y. Reply 'H-4 ok' or paste the number you see.").
- For BLOCKED tasks, say what you already tried.
- If the human's reply is unclear, ask one short follow-up, again using the block.

### 13.3 `docs/HUMAN_TODO.md`

Keep a running list so nothing is lost if the human steps away or the session ends:

```markdown
| ID | Milestone | Type | What is needed | Status | Answer / notes |
|----|-----------|------|----------------|--------|----------------|
| H-1 | 0 | ACTION | Confirm test notification arrived | open / done | ... |
```

At the start of every session, read `docs/HUMAN_TODO.md` first and remind the human of any open items with a HUMAN ACTION REQUIRED block before continuing.

---

## 14. `OPEN_QUESTIONS.md` format

```markdown
| ID | Question | Why it matters | Source checked | Status |
|----|----------|----------------|----------------|--------|
| Q1 | ... | ... | URL + page | open / answered |
```

---

## 15. Glossary

| Japanese | English |
|---|---|
| 給付付き税額控除 | Refundable tax credit |
| 社会保障国民会議 | Social Security National Council |
| 手取り | Take-home (disposable) income |
| 年収の壁 | Income walls (thresholds where take-home pay stalls or falls) |
| 社会保険料 | Social insurance contributions |
| 消費税減税 | Consumption tax cut |
| 実効限界負担率 | Effective marginal rate |
| 所得階級(十分位) | Income decile |
