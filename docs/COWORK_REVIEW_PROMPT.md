# Persona review of Tedori Lab: a prompt for Claude Cowork

Paste everything below the line into Claude Cowork. It reviews the live website only and changes nothing.

---

You are coordinating a review of a public website, Tedori Lab (手取りラボ). Split the work across many subagents. Each one plays one possible visitor (the personas are listed below), uses the live site the way that person would, and reports what went wrong for them. Then check the reported errors and combine everything into one report.

## The website

- Home: https://iamodd5.github.io/-tedori-lab/site/index.html
- Main pages (in the header): ホーム, 案の比較 (compare.html), 全世帯で見ると (population.html), 自分で案を作る (builder.html), レポート (report.html)
- About pages (in the footer): 計算方法 (methods.html), 検証 (validation.html), 出典とコード (sources.html), and 訂正の記録 (corrections.html), if it loads
- Japanese is the default. The "English" button at the top right switches the whole site to English.
- The code, data and step-by-step hand calculations are public: https://github.com/Iamodd5/-tedori-lab (hand calculations: `tests/hand_calcs/H1.md` to `H8.md`)

## Rules for every subagent

1. **Read only.** Do not sign in, create accounts, open GitHub issues, post or send anything, or type into forms on any other website. On Tedori Lab itself, the household menus, sliders, chart zoom and buttons are fine: they run in the browser and send nothing.
2. **Quote, don't paraphrase.** Every finding gives the page URL and copies the exact sentence, label or number it is about, in the language it appeared in. Never invent a quote or a number. If you can't find the text again, drop the finding.
3. **Keep apart "I didn't understand this" and "this is wrong".** Call something wrong only if you can show why: a calculation, a primary source with its URL, or a contradiction between two places on the site (quote both).
4. **Stay neutral.** Nobody recommends, praises or criticises any plan, party or politician, whether in persona or not. Personas may say what they wanted to know and couldn't find, but never which plan is better. Flag wording on the site that seems to favour or criticise a plan, in either direction.
5. **Arrive cold.** A persona knows only its own description and the home page URL, as a real visitor would. Do not hand it this prompt's description of the site. Expert personas may also use the GitHub repository and primary sources.
6. **Device and language.** Personas marked "phone" use a phone-sized window (about 375 × 812). If you can't resize the browser, say so in the report. Personas marked "EN" use the English version; all others use Japanese.
7. **Time-box.** About 15 minutes of browsing per persona. Write down where they would have given up in real life.

## Personas (run them as parallel subagents; in batches if needed)

Everyday visitors. Each starts on the home page with the task shown.

| # | Persona | Device / language | Task |
|---|---|---|---|
| P1 | 42, Saitama. Works part-time (年収120万円). Their spouse is a company employee (年収500万円). Two children. Heard about the "130万円の壁" on TV. | phone, JA | "If I work more and earn ¥1.4m, does our household end up with less money? Under which plans?" |
| P2 | 20, university student in Osaka. Part-time job, about ¥1.1m a year. A dependant of their parents. | phone, JA | "How much can I earn before my parents or I lose money?" |
| P3 | 35, single mother in Fukuoka. Employee earning ¥2.4m. One child aged 10. | phone, JA | "Would any of these plans give me more money? How much?" |
| P4 | 45, freelance designer in Nagoya. Business income ¥3m. On National Health Insurance. | desktop, JA | "Does this site cover self-employed people like me, and what changes for me?" |
| P5 | 72, retired, rural Akita. Couple living on pensions (¥2m and ¥0.8m). Uses a tablet with large text and rarely uses websites. | tablet, JA | "Does anything here change our pension income?" |
| P6 | 38 and 36, dual-income employees in Tokyo (¥4.5m and ¥3m). Two children (2 and 8). | phone, JA | "Which household on this site is most like us, and what happens to us?" |
| P7 | 50, manager in Tokyo earning ¥9m. Spouse earns ¥7m. One child. Expects to lose out and is sceptical. | desktop, JA | "Do we pay more under these plans? Is the site being straight with people like us?" |
| P8 | 28, non-regular worker in Sendai earning ¥1.8m. Short attention span, only reads headlines. | phone, JA | "Give me the answer in 30 seconds." |
| P9 | 33, engineer from another country, living and working in Japan (¥4m). Reads Japanese poorly. | desktop, EN | "What is this site saying, and does it apply to me?" Also check that the English is natural and every Japanese term is explained. |
| P10 | 17, high school student writing a civics report on refundable tax credits. | desktop, JA | "Explain what a refundable tax credit is and one finding from this site, in my own words." |
| P11 | 55, lives in Hokkaido and earns ¥3.5m. Notices that the examples live in Tokyo. | phone, JA | "Do these numbers apply to people outside Tokyo?" |
| P12 | 61, HR manager at a small company that employs many part-timers. | desktop, JA | "What does this mean for my part-time staff around ¥1.06m and ¥1.3m?" |

Specialists. Each does the check shown, using the site, the GitHub repository and primary sources (the National Tax Agency, ministries, the Japan Pension Service, Shinjuku City, the plan authors' own documents).

| # | Persona | Device / language | Check |
|---|---|---|---|
| S1 | Certified tax accountant (税理士) | desktop, JA | Pick three of H1–H8 in `tests/hand_calcs/` and recalculate the 2026 income tax and resident tax from scratch. Flag any step or number you disagree with, giving the legal basis. |
| S2 | Social insurance specialist (社労士) / payroll officer | desktop, JA | Check the social insurance in the hand calculations: monthly standard pay grades, health, pension and employment insurance rates, the child and childcare support levy, and when a spouse leaves dependant status. |
| S3 | Economics journalist at a national newspaper | desktop, JA | Is the main finding on Home and in the Report clear, true and worth a story? Could you quote it accurately? Are the limits stated where a reader would see them? |
| S4 | Policy staffer for a ruling party | desktop, JA | Look for anything unfair to the government's plans: how they are described, why they "can't be calculated yet", and which numbers are shown first. |
| S5 | Policy staffer for an opposition party | desktop, JA | Look for anything that favours the government's plans or plays down problems with them. Check that the walls are described accurately. |
| S6 | Public-finance economist | desktop, EN | Check the all-household estimate and the cost: the method, the stated calibration gaps, the static (no behaviour change) assumption, and any claim stronger than the method supports. |
| S7 | Statistician / data scientist | desktop, EN | Check that the Checks page numbers match the output files in the repository, that the approximations are labelled wherever their numbers appear, and (if you can run code) whether `make all` from a clean clone reproduces `outputs/`. |
| S8 | Someone who knows the Daiwa Institute of Research proposal well, as its authors would | desktop, JA | Is the Daiwa plan described and calculated faithfully? Is the difference from Daiwa's own cost estimate explained fairly? |
| S9 | Someone who knows the Rengo (trade union confederation) proposal well | desktop, JA | Is the Rengo plan described accurately, and is the reason it can't be calculated yet correct? |
| S10 | Someone who knows the government documents (国民会議 materials, the Cabinet basic policy and the bill) well | desktop, JA | Are the government plans described accurately, with the right dates and amounts, and with nothing the documents don't say? |
| S11 | Accessibility specialist | desktop + phone, JA | Use the keyboard only and a screen reader if available. Check contrast, colour-only meaning (red for losses), chart labels and alternatives, focus order, zoom to 200%, and sideways scrolling on a phone. |
| S12 | Hostile critic who wants to discredit the site | desktop, JA | Find the single weakest number or claim, the one most likely to be used against the site. Then check whether it really is wrong. |

## What each subagent reports (fixed format)

```
PERSONA: <P# or S#>, <one-line description>
DEVICE / LANGUAGE: <...>  (say if you could not emulate a phone)
TASK: done / partly / gave up. <where they got stuck, in one or two sentences>
FINDINGS:
- [<P#>-1] page: <URL>
  quote: "<exact text or number as it appears>"
  type: wrong-number | wrong-fact | contradiction | confusing | missing-context | bias | accessibility | broken
  severity: high | medium | low
  why: <what the persona expected, or the calculation or source showing the error (with URL)>
  suggested wording or fix: <plain words; never a recommendation of a plan>
OVERALL: <three sentences: would this person trust the site, would they share it, and which single change would help them most>
```

Severity:
- **high**: a wrong number or fact, a claim the site can't support, wording that favours or criticises a plan, or anything that stopped the persona from finishing the task.
- **medium**: confusing enough that the persona misreads a result or gives up on a page.
- **low**: polish.

## Then verify (separate subagents)

For every finding of type wrong-number, wrong-fact, contradiction or bias, start a verifier subagent that did not write it. Its job is to show the finding is mistaken: recompute the number, open the primary source, and reread the page in both languages. It marks each finding:
- **CONFIRMED**, with the evidence;
- **NOT AN ERROR**, with the reason (for example, the site states the assumption on another page; quote it);
- **UNSURE**, with what would settle it.

Don't drop NOT AN ERROR findings: if a careful reader got it wrong, the page may still need clearer wording. Move them to "confusing".

## Final report

Combine everything into one Markdown file named `tedori-lab-persona-review-<today's date>.md`, then show it. Merge duplicates and list every persona that hit each one. Sections, in this order:

1. **Summary**: the ten most important findings, one line each.
2. **Confirmed errors** (wrong numbers, wrong facts, contradictions), with evidence.
3. **Possible bias** in either direction, with the verifier's verdict.
4. **Where people got confused**, ranked by how many personas hit it, with the exact text that confused them.
5. **Phone, accessibility and broken things.**
6. **Unsure findings**, and what would settle each.
7. **Task results**: one row per persona (done / partly / gave up, and where).
8. **What worked**: things several personas found clear or useful, kept short.

Keep every quote exact and every finding tagged with its page URL. The report goes back to the site's developer, who will check each item before changing anything. Note at the top that these are simulated visitors, not real people.
