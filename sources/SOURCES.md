# Sources index

All files were downloaded on **2026-10-29** with `curl`. Paths are relative to `sources/`.
Every file's SHA-256 fingerprint is in `sources/SHA256SUMS`. Check all of them with `cd sources && shasum -a 256 -c SHA256SUMS` (every line should end in `OK`).
Plain-text copies of every PDF are in `sources/text/` (regenerate with `.venv/bin/python -I scripts/pdf_to_text.py sources`).

Status key: **downloaded** = file is here; **landing page only** = we have the index page, the actual table/PDF still has to be picked and downloaded; **MISSING** = could not be fetched.

> **Important finding.** The spec (Section 1) calls the July 13, 2026 document the "final government draft". The council's own pages show that July 13 was the **draft interim summary** (中間とりまとめ（案）). It was followed by the adopted interim summary (July 29), a **Cabinet decision on the basic policy (Aug 5)**, a Cabinet-decided **outline for the food consumption tax cut plus a new "就業者負担軽減支援金" (worker burden-relief payment) (Sep 15)**, and a **bill submitted Oct 9**. See OPEN_QUESTIONS Q1 and Q2.

## 1. Government credit design (Cabinet Secretariat, 社会保障国民会議)

Base URL: `https://www.cas.go.jp/jp/seisaku/kokuminkaigi/` (index saved as `gov/kokuminkaigi_index.html`)

| File | Title (as on the site) | Published | URL (under base + `contents/`) | Pages | Status |
|---|---|---|---|---|---|
| gov/20260527_index.html | 実務者会議（第12回）議事次第・資料 | 2026-05-27 | 20260527/index.html | – | downloaded |
| gov/20260527_00_agenda.pdf | 第12回 議事次第 | 2026-05-27 | 20260527/00_agenda.pdf | 1 | downloaded |
| gov/20260527_01_siryou1.pdf | 資料1 議題 | 2026-05-27 | 20260527/01_siryou1.pdf | 1 | downloaded |
| gov/20260527_02_siryou2.pdf | 資料2 給付付き税額控除のイメージ（中間とりまとめに向けた議論の整理） | 2026-05-27 | 20260527/02_siryou2.pdf | 4 | downloaded |
| gov/20260527_11_siryou1.pdf | 参考資料1 同上 参考資料 (charts) | 2026-05-27 | 20260527/11_siryou1.pdf | 12 | downloaded |
| gov/20260527_12_siryou2.pdf | 参考資料2 中間とりまとめに向けた議論の整理（第11回 5/20 資料7） | 2026-05-27 | 20260527/12_siryou2.pdf | 11 | downloaded |
| gov/20260527_minutes.pdf | 第12回 議事要旨 | 2026-05-27 meeting | 20260527/minutes.pdf | 9 | downloaded |
| gov/20260713_index.html | 実務者会議（第18回）議事次第・資料 | 2026-07-13 | 20260713/index.html | – | downloaded |
| gov/20260713_00_agenda.pdf | 第18回 議事次第 | 2026-07-13 | 20260713/00_agenda.pdf | 1 | downloaded |
| gov/20260713_01_siryou1.pdf | 資料1 議題 | 2026-07-13 | 20260713/01_siryou1.pdf | 1 | downloaded |
| gov/20260713_02_siryou2.pdf | 資料2 中間とりまとめ（案）（給付付き税額控除の本格導入部分） | 2026-07-13 | 20260713/02_siryou2.pdf | 5 | downloaded |
| gov/20260713_11_siryou1.pdf | 参考資料1 給付付き税額控除のイメージ（5/27 資料2の抜粋） | 2026-07-13 | 20260713/11_siryou1.pdf | 1 | downloaded |
| gov/20260713_minutes.pdf | 第18回 議事要旨 | 2026-07-13 meeting | 20260713/minutes.pdf | 7 | downloaded |
| gov/20260729-4_01_siryou1.pdf | 中間とりまとめ（社会保障国民会議 令和8年7月29日） | 2026-07-29 | 20260729-4/01_siryou1.pdf | 8 | downloaded |
| gov/20260729-4_02_siryou2.pdf | 「給付付き税額控除」のイメージ（中間とりまとめ） | 2026-07-29 | 20260729-4/02_siryou2.pdf | 3 | downloaded |
| gov/20260805_01_siryou1.pdf | 「給付付き税額控除」の制度導入の基本方針（令和8年8月5日閣議決定） | 2026-08-05 | 20260805/01_siryou1.pdf | 13 | downloaded |
| gov/20260805_02_siryou2.pdf | 参考資料1 | 2026-08-05 | 20260805/02_siryou2.pdf | 3 | downloaded |
| gov/20260805_03_siryou3.pdf | 参考資料2（7月30日総理会見のポイント） | 2026-08-05 | 20260805/03_siryou3.pdf | 8 | downloaded |

Not yet downloaded (available on the index page if needed later): agendas/materials of the other 30+ expert and working-group meetings (Feb–Sep 2026), member list, 20261009 `siryou5.pdf` 参照条文 (3.8 MB, statutory cross-references).

## 2. Food consumption tax cut (+ worker burden-relief payment)

| File | Title | Published | URL (under base + `contents/`) | Pages | Status |
|---|---|---|---|---|---|
| gov/20260915_01_siryou1.pdf | 飲食料品消費税率の臨時的な引下げ及び就業者負担軽減支援金の導入に関する大綱（令和8年9月15日閣議決定） | 2026-09-15 | 20260915/01_siryou1.pdf | 16 | downloaded |
| gov/20260915_02_siryou2.pdf | 同 概要資料 | 2026-09-15 | 20260915/02_siryou2.pdf | 3 | downloaded |
| gov/20261009_siryou1.pdf | 法律案 概要 | 2026-10-09 | 20261009/siryou1.pdf | 1 | downloaded |
| gov/20261009_siryou2.pdf | 法律案 要綱 | 2026-10-09 | 20261009/siryou2.pdf | 8 | downloaded |
| gov/20261009_siryou3.pdf | 法律案・理由 | 2026-10-09 | 20261009/siryou3.pdf | 83 | downloaded |
| gov/20261009_siryou4.pdf | 新旧対照表 | 2026-10-09 | 20261009/siryou4.pdf | 37 | downloaded |

Party proposals (spec Section 6 "party proposals as published"): **not collected yet**. Choosing which party documents to include touches political wording, so it is listed as a human decision (HUMAN_TODO H-3 / OPEN_QUESTIONS Q2).

## 3. Rengo design

| File | URL | Status |
|---|---|---|
| rengo/rengo_p5465.html | https://www.jtuc-rengo.or.jp/activity/seisaku_jitsugen/teigen/?p=5465 | **MISSING** – the site returned a "メンテナンス中" (under maintenance) page on 2026-10-29. Kept only as evidence. OPEN_QUESTIONS Q3. |

## 4. Daiwa design

| File | Title | Published | URL | Pages | Status |
|---|---|---|---|---|---|
| daiwa/daiwa_20251010.pdf | 働く低所得者の負担を軽減する「社会保険料還付付き税額控除」の提案 ― 追加財政負担なしで課税最低限（年収の壁）178 万円達成も可能（大和総研, p.1） | 2025-10-10 (p.1) | https://www.dir.co.jp/report/research/law-research/tax/20251010_025349.pdf | 8 | downloaded |

Note: this report predates the council's work. Whether Daiwa published an updated design in 2026 has not been checked yet (OPEN_QUESTIONS Q7).

## 5. Income tax and resident tax (2026 rules)

| File | Title | URL | Status |
|---|---|---|---|
| tax/nta_1410_kyuyo_shotoku_kojo.html | NTA タックスアンサー No.1410 給与所得控除 | https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm | downloaded |
| tax/nta_1199_kiso_kojo.html | No.1199 基礎控除 | …/shotoku/1199.htm | downloaded |
| tax/nta_2260_shotokuzei_ritsu.html | No.2260 所得税の税率 | …/shotoku/2260.htm | downloaded |
| tax/nta_1191_haigusha_kojo.html | No.1191 配偶者控除 | …/shotoku/1191.htm | downloaded |
| tax/nta_1195_haigusha_tokubetsu.html | No.1195 配偶者特別控除 | …/shotoku/1195.htm | downloaded |
| tax/nta_1180_fuyo_kojo.html | No.1180 扶養控除 | …/shotoku/1180.htm | downloaded |
| tax/nta_1177_tokutei_shinzoku.html | No.1177 特定親族特別控除 | …/shotoku/1177.htm | downloaded |
| tax/nta_1600_koteki_nenkin.html | No.1600 公的年金等の課税関係 | …/shotoku/1600.htm | downloaded |
| tax/soumu_kojin_juminzei.html | 総務省 個人住民税 | https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html | downloaded |

Still needed (Milestone 2): NTA official worked examples for withholding / year-end adjustment (年末調整のしかた 2026 edition) to build tests.

## 6. Employee social insurance

| File | Title | URL | Status |
|---|---|---|---|
| social/kyoukaikenpo_rates.html | 協会けんぽ 都道府県毎の保険料率 (index) | https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/premium_prefectures/ | downloaded |
| social/kyoukaikenpo_r08.html | 同 令和8年度 | …/premium_prefectures/r08 | downloaded |
| social/kyoukaikenpo_R8_13tokyo.pdf | 令和8年度 東京都 保険料額表 | https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf | downloaded |
| social/kyoukaikenpo_13tokyo2_r8.pdf | 東京都 (2) | https://www.kyoukaikenpo.or.jp/assets/13tokyo2_r8.pdf | downloaded |
| social/kyoukaikenpo_13tokyo3_r8.pdf | 東京都 (3) | https://www.kyoukaikenpo.or.jp/assets/13tokyo3_r8.pdf | downloaded |
| social/nenkin_kosei_hokenryo.html | 日本年金機構 厚生年金保険料額表 | https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/index.html | downloaded (linked PDFs not yet) |
| social/mhlw_koyohoken_ritsu.html | 厚労省 雇用保険料率 | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000108634.html | downloaded |

Still needed: the 2026 coverage-threshold rules for part-time workers (the "1.06 million yen wall" changes) and the 被扶養者 1.3 million rule as currently in force.

## 7. National health insurance and national pension

| File | Title | URL | Status |
|---|---|---|---|
| social/nenkin_kokumin_hokenryo.html | 日本年金機構 国民年金保険料 | https://www.nenkin.go.jp/service/kokunen/hokenryo/hokenryo.html | downloaded |
| – | Reference municipality NHI rules | – | **waiting for human decision** (HUMAN_TODO H-5) |

## 8. Child allowance

| File | Title | URL | Status |
|---|---|---|---|
| child/cfa_jidoteate.html | こども家庭庁 児童手当制度のご案内 | https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai | downloaded |

## 9. Household spending and population weighting

| File | Title | URL | Status |
|---|---|---|---|
| stats/estat_kakei.html | 総務省統計局 家計調査 | https://www.stat.go.jp/data/kakei/index.html | landing page only |
| stats/stat_zenkoku_kakei_kozo.html | 全国家計構造調査 2024 | https://www.stat.go.jp/data/zenkokukakei/2024/index.html | landing page only |
| stats/mhlw_kokumin_seikatsu_kiso.html | 厚労省 国民生活基礎調査 | https://www.mhlw.go.jp/toukei/list/20-21.html | landing page only |
| stats/nta_minkan_kyuyo.html | 国税庁 民間給与実態統計調査 | https://www.nta.go.jp/publication/statistics/kokuzeicho/minkan/toukei.htm | landing page only |

The specific e-Stat tables (spending by income decile; household counts by type and income band; wage earners by income band) will be picked and downloaded in Milestones 2 and 7. They are not needed for Milestones 0–1.

## 10. Existing tool

| Item | Location | Notes |
|---|---|---|
| OpenFisca-Japan repository | https://github.com/project-inclusive/OpenFisca-Japan | Inspected at commit `1f8d13dbe735b064373fe67377859454dd750b9c` (2026-08-26). Not vendored into this repo; see `docs/COVERAGE.md`. |
| scrapbox_openfisca_mcp.json | https://scrapbox.io/api/pages/c4j/OpenFisca-Japan_MCP/text | Code for Japan design note on the OpenFisca-Japan MCP server. downloaded |
