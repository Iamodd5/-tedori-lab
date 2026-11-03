# Recheck of the persona-review fixes: a prompt for Claude Cowork

Paste everything below the line into the same Claude Cowork project that wrote the persona review of 2026-11-03 (`tedori-lab-persona-review-2026-11-03.md`). It reviews the live website and the public repository only, and changes nothing.

---

You reviewed Tedori Lab (手取りラボ) on 2026-11-03 with 24 simulated visitors (P1–P12, S1–S12) and verifier agents. Your report had 113 entries: E1–E22 (confirmed errors), B1–B6 (bias), C1–C64 (confusion), A1–A20 (phone, accessibility, broken) and U1 (unsure). If that report is still in this project, use it; the IDs below refer to it.

The site's developer (Claude Code) has since changed the site and published the changes. Your job now is to **check that work**: whether each fix is right, whether the reasoning behind it holds up, whether anything new is wrong, and whether visitors who got stuck can now finish. Be as sceptical of these fixes as you were of the original site. Where the developer's reasoning below is wrong, say so with evidence.

## What to check

- Live site: https://iamodd5.github.io/-tedori-lab/site/index.html (pages: index, compare, population, builder, report, methods, validation, sources, corrections)
- Repository, at the published commit: https://github.com/Iamodd5/-tedori-lab/tree/1204115
- Primary sources the developer used are saved in the repository under `sources/` (index: `sources/SOURCES.md`, section 12 lists the files added for these fixes). Laws are in `sources/law/` as e-Gov XML. City, ward and 協会けんぽ pages are not stored in git; their URLs are in `sources/EXTERNAL.tsv`.
- The full list of what changed, in plain words: `docs/LOG.md` (last section, "Milestone 10 (part 2)"), `docs/VALIDATION.md` section 11, and the website's 訂正の記録 / Corrections page (https://iamodd5.github.io/-tedori-lab/site/corrections.html).

## Rules for every subagent

1. **Read only.** No sign-ins, accounts, GitHub issues or comments, posts, messages, or typing into other websites. On Tedori Lab itself, menus, sliders, chart zoom and buttons are fine.
2. **Quote, don't paraphrase.** Every finding gives the URL (or repository file and line) and the exact text or number, in the language it appeared in. Never invent a quote or a number.
3. **Keep apart "I didn't understand this" and "this is wrong".** Call something wrong only with a calculation, a primary source with its URL, or two places on the site that contradict each other (quote both).
4. **Stay neutral.** Nobody recommends, praises or criticises any plan, party or politician. Flag wording that seems to favour or criticise a plan, in either direction, including wording the developer added.
5. **Device and language** as in the first review (phone personas at about 375 × 812; EN personas in English). Note: a first visit from a browser that isn't set to Japanese now opens in English; clear site data or use the language button if a persona needs Japanese.
6. **Today's date matters.** Some text is dated (for example the bill's status "2026年11月3日時点で衆議院で審議中"). Check whether it is still true on the day you run.

## What the developer changed, and why

Each line gives the ID from your report, what was done, and the reasoning. "Check" says what to verify.

### Rules in the calculation (these change numbers)

For each, the developer says the hand calculation in `tests/hand_calcs/` was corrected first, citing the source, and the test was seen failing before the code changed.

- **E15 (resident-tax rounding).** 特別区民税 (6%, 調整控除 3%) and 都民税 (4%, 2%) are now worked out separately and each rounded down to 100 yen; taxable income is rounded to 1,000 once. Reasoning: 地方税法20条の4の2第3項 rounds each tax; 第8項 joins them only when a whole amount is under 100 yen (`sources/law/chihozeiho_20270101.xml`); 大田区's worked example does the same. Result: H3 6,248,008, H5 2,208,436, H8 12,009,068 (each +100); several walls move by 100 yen. The burden-relief band just above the income-levy line (附則3条の3) now cuts each tax by its share of the excess before rounding.
  - **Conflict the developer kept visible:** MIC 資料３ p.18's figure shows one combined levy of 4,200 at income 1,124,200; by the law as read above it is 2,500 + 1,600 = 4,100. The test built from the figure is kept as an expected failure (OPEN_QUESTIONS Q22). **Check this reading of 附則3条の3 and 20条の4の2 specifically.**
- **E4 (令和9年度 resident-tax limits).** Spouse/dependant income limit 580,000 → 620,000 (地方税法292条1項7号・9号 as amended by 令和8年法律第2号, 附則11条2項: from 令和9年度); working-student limit 750,000 → 890,000 (所得税法2条1項32号, applied by 地方税法314条の2第9項); resident-tax 特定親族特別控除 added (314条の2第1項第12号; bands from 大田区's 令和9年度 table). All other deduction amounts are now cited to the law, and the old "（近似）新宿区の2025年度分の案内" note is gone. Result: H2's wall at 1.49m → 1.5m is −75,572 (back at 1,590,000), plus a separate −18,458 wall at 1.63m → 1.64m (back at 1,670,000). Check: the amounts, and that nothing else changed for 令和9年度 (the developer relied on 中央区 and 足立区 pages saying 基礎控除 is unchanged).
- **E6 (NHI reduction earner count).** A 給与所得者等 is now someone with salary revenue over 550,000, or, without salary income, pension revenue over 600,000 (under 65) or 1,250,000 (65+); the 65+ 150,000 comes off pension income only, never below 0. Reasoning: 国民健康保険法施行令29条の7第6項第1号 and 附則5条 (`sources/law/kokuho_sekourei_333CO0000000362_asof20260401.xml`). Result: H6's walls at 1.68m → 1.69m (−17,888) and 2.3m → 2.31m (−28,301); take-home at a head pension of 1.7m is 2,414,941. Open points the developer flagged rather than decided: Shinjuku's table says 「以上」 where the order says 「を超える」 (matters only exactly at the thresholds; the engine follows the order); whether the 150,000 may push pension income below 0 (no example household is affected).
- **E3 (the 8.8万円 wage test).** The test now applies January–September 2026 only; from 2026-10-01 a part-timer working 20+ hours at a 51+ firm (not a student) is in employee insurance at any wage. Reasoning: 令和8年政令第275号 (施行期日 2026-10-01), 保発0911第6号, and 日本年金機構's notice of 2026-10-01. The year is split: 9/12 of the NHI and 9 months of national pension (国民年金法11条; NHI 月割 under 国保法8条 and the MHLW model ordinance), 3 months of employee premiums (厚生年金保険法19条). Result: H1 at salary 1,050,000: take-home 834,858 (was 814,839); the step 1.05m → 1.06m is +69,994 (was +90,013). The all-household estimate changed too (the lowest income group's average gain under the Daiwa plan: 8,659, was 9,209). Not modelled: the 最低賃金減額特例 exception; Shinjuku's own NHI ordinance text could not be read (login wall). **Check the month-counting and the NHI proration.**
- **Q30.** National pension ages (20 to under 60) are now read from parameters, cited to 国民年金法7条1項1号. No number changed.
- **C29 (consequence).** Rengo's plan abolishes the reduced 8% rate when its refund starts (税制改革構想 PDF p.33), so Rengo now also lists "no food spending for H1–H8" as a reason it can't be calculated.

### Text corrected

- **E1.** Methods page (both languages): the Rengo reason is now that the refund amounts aren't published; the documents and their date are named. `sources/SOURCES.md` intro updated.
- **E2, A4.** `docs/VALIDATION.md` rewritten: the H4 wall row is back inside the table with −258,226 (2,682%); §7 says 1,640,000; older values are labelled as history.
- **E5, C13, C14.** The tax comparators are described as the 2024 survey's own estimate of tax from reported incomes, "not tax actually collected", on Checks, All households and the report. Part-year earners were added to the calibration (5,982,206 at ¥1m or less, so about 9.69 million in all; the model's 15.28 million is about 1.6 times that). The report's limits and the All households page now mention the low-earner excess and the high-earner shortfall.
- **E7, E8, E18, B2, B3, B4, C16, C47, C48.** Both government plan descriptions rewritten (home page, plan details; All households page; report): the bill's status and date; the 支援金 starts April 2027 and takes its full form from FY2029; two half-year payments in FY2029; the four conditions including the spouse-income test (not in FY2027–28); children under 16 in FY2027–28; the 就業促進特例加算 (also in FY2027–28, per 大綱 p.8 注); income-linked payments; "not decided yet" instead of "not published". English cap: "no larger than the expected revenue from the remaining 1% consumption tax on food". Sources: 大綱 2026-09-15 pp.8–13, bill summary 2026-10-09 p.1, 衆議院 議案 page (checked 2026-11-03).
- **B1, E13, C15, C22.** New opening paragraph on Home and in the report (quote it and judge it). The plan count ("いま計算できるのは1つの案だけ") is generated from the data. 手取り is defined as "after tax and insurance, plus child allowance". A sentence says the government plan is a cash payment by municipalities that the government calls a "first step".
- **B5.** The report now says the Daiwa plan's wall remains (「壁は残ります」) and that the government's 年収の壁 top-up can't be calculated yet. It does not say H4 would receive it.
- **B6.** English label "stopgap" → "bridge".
- **E9, C7, C23.** Each listed wall now gives its cause, worked out from the change in each tax and premium at that step (new `wall_causes` in `outputs/wall_map.json`; tested against `tests/hand_calcs/wall_H4.md`). Small dips (under ¥10,000) get a neutral reason; walls of ¥10,000 or more beyond the top three are counted separately.
- **E10.** Not changed to 10,000-yen steps (the developer's reason: tax rounding to 100 yen makes a 10,000-step chart noisy, and mixing step sizes would confuse more). Instead: a note under the chart explaining the 100,000-yen steps, and ▼ marks on the take-home chart at the listed walls. METHODS.md's "same information" sentence corrected.
- **E11, C38.** Methods: the cash cap counts employee health (with care) and pension for employees, NHI and national pension for other workers. New Daiwa approximations: NHI counts only toward the head's cap; the spouse's national pension counts toward her own cap even when the head deducts it.
- **E12.** Home and report give the general reason ("amounts not decided or published; click a plan for its reasons"). The bridge plan is shown only as one package, so no number for the tax-rate half alone; the methods page says so.
- **E14.** Income 0 is now left out of the "extra ¥100,000" chart as it already was from the list; a note says why. (A test was changed for this; it is listed in VALIDATION.md section 11.)
- **E16, E17.** The Checks range is computed from the output files (now 12,882–19,937 after the E15 fix). Methods says the Checks page is hand-written and tested against the outputs.
- **E19.** Recovery points are worded as found "in ¥10,000 steps" (the exact crossing is not computed).
- **E20.** The premium note now says: health and care rates from March 2026, employment insurance from April, the child levy new from April, the pension rate (18.3%) unchanged. The levy is still charged for all 12 months, as a labelled approximation; the developer did not switch to 9 months, to keep all rate changes on one convention. **Say whether you think that is acceptable.**
- **E21, E22.** VALIDATION §5 now says 680,000; Q19 text corrected. The two citations in `government_final.yaml` fixed.
- **C1.** Internal codes (HUMAN_TODO, Milestone, spec, CLAUDE.md) removed from rendered methods and validation text; question numbers such as (Q13) now link to `OPEN_QUESTIONS.md` on GitHub.

### Pages and accessibility

- **C2, C6.** A note on Home, in the report and in methods on what changes outside Tokyo (協会けんぽ rate by prefecture; NHI and parts of resident tax by municipality). A note that age and children change results.
- **C4, C9, C17, C18, C19.** The Home example box and the report lead now: say "today's rules, before any plan"; state the spouse works under 20 hours and isn't in her employer's insurance; label the row "change in take-home"; give the cause; carry the （近似） label for who deducts the spouse's national pension; and note the April 2026 contract-based dependant test.
- **C5, C11, C32, C42, C57.** Compare page: why income tax rises under Daiwa for households that lose; why ±0 for H2 and H6; the 2026 take-home split into each tax and premium; a note on the 65+ care premium (H6) and the 児童扶養手当 (H5); a message instead of an empty chart when nothing changes.
- **C10, C24.** Compare page says the result is for the current income and links to the Home chart for that household; the chosen household is kept across pages (`?hh=` and the browser's storage).
- **C3, C26, C33, C53, C54, C55.** All households page: national totals to ¥0.1 trillion; the reason for the gap with Daiwa's own estimate in Japanese; "net effect" written in words; the share of households that see no change in groups that gain on average; Daiwa's report named; static-estimate and （近似） labels at the cost table.
- **C12 (partly).** Who each plan covers: self-employed people under the government plan and Daiwa; Rengo's first scheme is for employees only; pensioners not in work. Foreign residents were not researched.
- **C28.** A note that the "106万円の壁" condition ended on 2026-10-01; H1's notes explain the split year.
- **C29, C35, C36, C37, C50, C51.** Rengo: scope, version and date, the reduced-rate abolition, the taper, Rengo's own cost figures. Daiwa: the proposal's name, "everyone subject to income tax (including people paying 0)", the eight variants and which one is calculated, the formula written with "0" for the deduction.
- **C34.** Home shows each calculable plan's figure at the same wall.
- **C39, C40, C41, C43, C31, C45, C60, C63.** Notes for H2 (世帯 = the student alone; the deferral's income limit, labelled approximation), H6, H3, H7 (business income after expenses, no blue-return deduction), the population page (examples are not group averages), the builder's definition, "Tedori (手取り) means take-home pay".
- **A1.** Tooltips use short plan names and two-line titles; measured 311 px inside a 321 px chart on a 375 px screen, both languages.
- **A2.** Each slider is named by its own label (`aria-labelledby`) with `aria-valuetext`.
- **A3, A9, A18.** Chart labels in the page language on Home, Compare and Build your own (on the published version the two All households charts still have fixed English labels; fixed locally after publishing, not yet live); landmark names in both languages; English documents marked `lang="en"`; the language button no longer has a mixed-language label; `<main>` and a skip link; document headings moved down one level; builder subheading is an h2.
- **A5.** "数字の表を見る" under the wall charts (every ¥100,000 of the range shown).
- **A6.** Full screen is a modal dialog: the rest of the page is inert, focus returns to the button.
- **A7, A10, A13.** Scroll padding under the sticky header; the header links wrap on a phone (all five visible); header focus ring drawn inside.
- **A8, A15.** The builder's second line is dotted; the Daiwa line and cash bars use #B87A00 (3.6:1 on white); stacked bars have white borders.
- **A12.** Government documents are full clickable links. The site answered "not found" to curl's default user agent but 200 to a browser one (`make` sends a browser user agent).
- **A14, A16, A17, A20.** All ten group labels on phone charts; the "can't calculate yet" box is `role="status"`; ＋/− zoom buttons and 24 px grips; English on a first visit when the browser isn't Japanese.

### Not done, on purpose or not yet

- **U1 / Q38 (health + levy rounding):** kept as separate rounding with a （近似） label. The MHLW/こども家庭庁 Q&A of 2026-02-12 (Q6) says to round once, combined, but it has been withdrawn (the developer saved an Internet Archive copy). Left to the project owner.
- **C27 (H2's parents):** a note only; adding the parents needs a parent income, which the project owner must choose.
- **C64 (who made the site):** left to the project owner.
- Not done yet: C44 (income range of each group), C49 (order of the plans), C61 (English glosses in the specialist notes), A11 (only shorter plan names; no card layout), A19 (tap snapping), C3's suggested extra column computed with Daiwa's own inputs, C6's editable ages, C10's salary box, C40's modelling of the deferral limit (Q39). Two new open questions: Q37 (resident-tax spouse deduction for earners between 9m and 10m) and Q39.
- Q7 (Daiwa's later reports, which S8 reported) has not been checked by the developer.

## How to run the recheck (subagents)

1. **Verifiers, one per group of IDs** (E1–E22, B1–B6, then the C and A items in batches). Each verifier did not write the fix it checks. For every ID: open the page or file, quote what it says now, and give a verdict:
   - **FIXED**: the problem is gone and the new text or number is right;
   - **PARTLY**: better, but something named is still wrong or missing;
   - **NOT FIXED**: the problem is still there;
   - **NEW PROBLEM**: the fix introduced an error or a bias (give the evidence).
   For the four calculation rules (E3, E4, E6, E15), recompute at least one number by hand from the cited law and the hand calculation in `tests/hand_calcs/` (H1 revision in `wall_H1.md`, H3/H5/H8 revisions, H6 revision), and check the citation says what the developer says it says.
2. **Regression sweep.** Two agents compare the published commit with the previous one (https://github.com/Iamodd5/-tedori-lab/compare/4e1c6be...1204115) and look for anything that broke or changed without being listed on the Corrections page.
3. **Corrections page audit.** One agent checks each 2026-11-03 entry on https://iamodd5.github.io/-tedori-lab/site/corrections.html against the before and after versions: are the numbers right, and is every published number that changed listed?
4. **Neutrality pass.** S4 (ruling-party staffer) and S5 (opposition staffer) re-read every rewritten plan description and the new opening paragraph, quoting anything that leans either way.
5. **Personas who got stuck, again.** Run P1, P2, P3, P5, P8, P9, P11, P12 and S11 cold on their original tasks and devices. Record whether they now finish, and where they stop if not.
6. **Verify new claims.** Any new finding of type wrong-number, wrong-fact, contradiction or bias goes to a separate verifier, as in the first review (CONFIRMED / NOT AN ERROR / UNSURE).

Use the same finding format as the first review for new findings.

## Report

Write one Markdown file, `tedori-lab-recheck-<today's date>.md`, then show it. Note at the top that the visitors are simulated. Sections:

1. **Summary**: counts of FIXED / PARTLY / NOT FIXED / NEW PROBLEM, and the five most important points.
2. **Verdict table**: one row per original ID (all 113), with the verdict, one line of evidence, and the page or file.
3. **Calculation rules (E3, E4, E6, E15)**: your own recomputation and whether the developer's reading of each law holds, including the MIC p.18 conflict and the E3 month-counting.
4. **New problems and regressions**, with evidence and verdicts.
5. **Corrections page audit.**
6. **Bias**, in either direction, in the new text.
7. **Personas rerun**: done / partly / gave up, and where.
8. **Where you disagree with the developer's reasoning**, and why (for example E10, E20, U1, or anything under "Not done").

Keep every quote exact and every finding tagged with its URL or file. The report goes back to the developer, who will check each item before changing anything.
