# Sources index

All files were downloaded on **2026-10-29** with `curl`. Paths are relative to `sources/`.
`sha256` is the first 12 hex characters of the file's SHA-256 (run `shasum -a 256 <file>` to check).
Plain-text copies of every PDF are in `sources/text/` (regenerate with `.venv/bin/python -I scripts/pdf_to_text.py sources`).

Status key: **downloaded** = file is here; **landing page only** = we have the index page, the actual table/PDF still has to be picked and downloaded; **MISSING** = could not be fetched.

> **Important finding.** The spec (Section 1) calls the July 13, 2026 document the "final government draft". The council's own pages show that July 13 was the **draft interim summary** (中間とりまとめ（案）). It was followed by the adopted interim summary (July 29), a **Cabinet decision on the basic policy (Aug 5)**, a Cabinet-decided **outline for the food consumption tax cut plus a new "就業者負担軽減支援金" (worker burden-relief payment) (Sep 15)**, and a **bill submitted Oct 9**. See OPEN_QUESTIONS Q1 and Q2.

## 1. Government credit design (Cabinet Secretariat, 社会保障国民会議)

Base URL: `https://www.cas.go.jp/jp/seisaku/kokuminkaigi/` (index saved as `gov/kokuminkaigi_index.html`, sha256 709c4a278e9b)

| File | Title (as on the site) | Published | URL (under base + `contents/`) | Pages | sha256 | Status |
|---|---|---|---|---|---|---|
| gov/20260527_index.html | 実務者会議（第12回）議事次第・資料 | 2026-05-27 | 20260527/index.html | – | 9c1a5d1661e8 | downloaded |
| gov/20260527_00_agenda.pdf | 第12回 議事次第 | 2026-05-27 | 20260527/00_agenda.pdf | 1 | 1f6ad8a934c3 | downloaded |
| gov/20260527_01_siryou1.pdf | 資料1 議題 | 2026-05-27 | 20260527/01_siryou1.pdf | 1 | cb1e75241557 | downloaded |
| gov/20260527_02_siryou2.pdf | 資料2 給付付き税額控除のイメージ（中間とりまとめに向けた議論の整理） | 2026-05-27 | 20260527/02_siryou2.pdf | 4 | 13dad4f93b0a | downloaded |
| gov/20260527_11_siryou1.pdf | 参考資料1 同上 参考資料 (charts) | 2026-05-27 | 20260527/11_siryou1.pdf | 12 | 9feeff1232af | downloaded |
| gov/20260527_12_siryou2.pdf | 参考資料2 中間とりまとめに向けた議論の整理（第11回 5/20 資料7） | 2026-05-27 | 20260527/12_siryou2.pdf | 11 | 3761a4d55b03 | downloaded |
| gov/20260527_minutes.pdf | 第12回 議事要旨 | 2026-05-27 meeting | 20260527/minutes.pdf | 9 | 9eb5b9f5e8c1 | downloaded |
| gov/20260713_index.html | 実務者会議（第18回）議事次第・資料 | 2026-07-13 | 20260713/index.html | – | a9e613ba9743 | downloaded |
| gov/20260713_00_agenda.pdf | 第18回 議事次第 | 2026-07-13 | 20260713/00_agenda.pdf | 1 | 44711c18a6ef | downloaded |
| gov/20260713_01_siryou1.pdf | 資料1 議題 | 2026-07-13 | 20260713/01_siryou1.pdf | 1 | a5d4009cb7b8 | downloaded |
| gov/20260713_02_siryou2.pdf | 資料2 中間とりまとめ（案）（給付付き税額控除の本格導入部分） | 2026-07-13 | 20260713/02_siryou2.pdf | 5 | 6f0055b2290a | downloaded |
| gov/20260713_11_siryou1.pdf | 参考資料1 給付付き税額控除のイメージ（5/27 資料2の抜粋） | 2026-07-13 | 20260713/11_siryou1.pdf | 1 | 58c42ff296a4 | downloaded |
| gov/20260713_minutes.pdf | 第18回 議事要旨 | 2026-07-13 meeting | 20260713/minutes.pdf | 7 | 8840b18d0c1b | downloaded |
| gov/20260729-4_01_siryou1.pdf | 中間とりまとめ（社会保障国民会議 令和8年7月29日） | 2026-07-29 | 20260729-4/01_siryou1.pdf | 8 | 5a5f1d348bc9 | downloaded |
| gov/20260729-4_02_siryou2.pdf | 「給付付き税額控除」のイメージ（中間とりまとめ） | 2026-07-29 | 20260729-4/02_siryou2.pdf | 3 | e4ef4b57d7d9 | downloaded |
| gov/20260805_01_siryou1.pdf | 「給付付き税額控除」の制度導入の基本方針（令和8年8月5日閣議決定） | 2026-08-05 | 20260805/01_siryou1.pdf | 13 | de69eb4267cc | downloaded |
| gov/20260805_02_siryou2.pdf | 参考資料1 | 2026-08-05 | 20260805/02_siryou2.pdf | 3 | 75b3f617630b | downloaded |
| gov/20260805_03_siryou3.pdf | 参考資料2（7月30日総理会見のポイント） | 2026-08-05 | 20260805/03_siryou3.pdf | 8 | 01d9ffd4037b | downloaded |

Not yet downloaded (available on the index page if needed later): agendas/materials of the other 30+ expert and working-group meetings (Feb–Sep 2026), member list, 20261009 `siryou5.pdf` 参照条文 (3.8 MB, statutory cross-references).

## 2. Food consumption tax cut (+ worker burden-relief payment)

| File | Title | Published | URL (under base + `contents/`) | Pages | sha256 | Status |
|---|---|---|---|---|---|---|
| gov/20260915_01_siryou1.pdf | 飲食料品消費税率の臨時的な引下げ及び就業者負担軽減支援金の導入に関する大綱（令和8年9月15日閣議決定） | 2026-09-15 | 20260915/01_siryou1.pdf | 16 | 203240dbe52f | downloaded |
| gov/20260915_02_siryou2.pdf | 同 概要資料 | 2026-09-15 | 20260915/02_siryou2.pdf | 3 | 1ad7718d3b8f | downloaded |
| gov/20261009_siryou1.pdf | 法律案 概要 | 2026-10-09 | 20261009/siryou1.pdf | 1 | be082ca32316 | downloaded |
| gov/20261009_siryou2.pdf | 法律案 要綱 | 2026-10-09 | 20261009/siryou2.pdf | 8 | 6a4b9b9713ec | downloaded |
| gov/20261009_siryou3.pdf | 法律案・理由 | 2026-10-09 | 20261009/siryou3.pdf | 83 | df47e67c8d3c | downloaded |
| gov/20261009_siryou4.pdf | 新旧対照表 | 2026-10-09 | 20261009/siryou4.pdf | 37 | 4197db761b83 | downloaded |

Party proposals (spec Section 6 "party proposals as published"): **not collected yet**. Choosing which party documents to include touches political wording, so it is listed as a human decision (HUMAN_TODO H-3 / OPEN_QUESTIONS Q2).

## 3. Rengo design

| File | URL | sha256 | Status |
|---|---|---|---|
| rengo/rengo_p5465.html | https://www.jtuc-rengo.or.jp/activity/seisaku_jitsugen/teigen/?p=5465 | 28714c5d6efe | **MISSING** – the site returned a "メンテナンス中" (under maintenance) page on 2026-10-29. Kept only as evidence. OPEN_QUESTIONS Q3. |

## 4. Daiwa design

| File | Title | Published | URL | Pages | sha256 | Status |
|---|---|---|---|---|---|---|
| daiwa/daiwa_20251010.pdf | Daiwa Institute of Research report (tax / law research) | 2025-10-10 (from URL) | https://www.dir.co.jp/report/research/law-research/tax/20251010_025349.pdf | 8 | d36484687528 | downloaded |

Note: this report predates the council's work. Whether Daiwa published an updated design in 2026 has not been checked yet (OPEN_QUESTIONS Q7).

## 5. Income tax and resident tax (2026 rules)

| File | Title | URL | sha256 | Status |
|---|---|---|---|---|
| tax/nta_1410_kyuyo_shotoku_kojo.html | NTA タックスアンサー No.1410 給与所得控除 | https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm | df763b025905 | downloaded |
| tax/nta_1199_kiso_kojo.html | No.1199 基礎控除 | …/shotoku/1199.htm | 21507083e62c | downloaded |
| tax/nta_2260_shotokuzei_ritsu.html | No.2260 所得税の税率 | …/shotoku/2260.htm | 638f0d78c962 | downloaded |
| tax/nta_1191_haigusha_kojo.html | No.1191 配偶者控除 | …/shotoku/1191.htm | 0725ae1600fe | downloaded |
| tax/nta_1195_haigusha_tokubetsu.html | No.1195 配偶者特別控除 | …/shotoku/1195.htm | ee1364c58db7 | downloaded |
| tax/nta_1180_fuyo_kojo.html | No.1180 扶養控除 | …/shotoku/1180.htm | c92803d8c75a | downloaded |
| tax/nta_1177_tokutei_shinzoku.html | No.1177 特定親族特別控除 | …/shotoku/1177.htm | f75c20fcbf5e | downloaded |
| tax/nta_1600_koteki_nenkin.html | No.1600 公的年金等の課税関係 | …/shotoku/1600.htm | b1462536b390 | downloaded |
| tax/soumu_kojin_juminzei.html | 総務省 個人住民税 | https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html | 2a35217817d5 | downloaded |

Still needed (Milestone 2): NTA official worked examples for withholding / year-end adjustment (年末調整のしかた 2026 edition) to build tests.

## 6. Employee social insurance

| File | Title | URL | sha256 | Status |
|---|---|---|---|---|
| social/kyoukaikenpo_rates.html | 協会けんぽ 都道府県毎の保険料率 (index) | https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/premium_prefectures/ | 96f0473d35cf | downloaded |
| social/kyoukaikenpo_r08.html | 同 令和8年度 | …/premium_prefectures/r08 | a37fdcfb4926 | downloaded |
| social/kyoukaikenpo_R8_13tokyo.pdf | 令和8年度 東京都 保険料額表 | https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf | 1c5abc10951a | downloaded |
| social/kyoukaikenpo_13tokyo2_r8.pdf | 東京都 (2) | https://www.kyoukaikenpo.or.jp/assets/13tokyo2_r8.pdf | f760babd0492 | downloaded |
| social/kyoukaikenpo_13tokyo3_r8.pdf | 東京都 (3) | https://www.kyoukaikenpo.or.jp/assets/13tokyo3_r8.pdf | 58724bf6a7a7 | downloaded |
| social/nenkin_kosei_hokenryo.html | 日本年金機構 厚生年金保険料額表 | https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/index.html | d0f242ee4a39 | downloaded (linked PDFs not yet) |
| social/mhlw_koyohoken_ritsu.html | 厚労省 雇用保険料率 | https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000108634.html | 2c4e9dac9ba2 | downloaded |

Still needed: the 2026 coverage-threshold rules for part-time workers (the "1.06 million yen wall" changes) and the 被扶養者 1.3 million rule as currently in force.

## 7. National health insurance and national pension

| File | Title | URL | sha256 | Status |
|---|---|---|---|---|
| social/nenkin_kokumin_hokenryo.html | 日本年金機構 国民年金保険料 | https://www.nenkin.go.jp/service/kokunen/hokenryo/hokenryo.html | 3dc7a93c7eca | downloaded |
| – | Reference municipality NHI rules | – | – | **waiting for human decision** (HUMAN_TODO H-5) |

## 8. Child allowance

| File | Title | URL | sha256 | Status |
|---|---|---|---|---|
| child/cfa_jidoteate.html | こども家庭庁 児童手当制度のご案内 | https://www.cfa.go.jp/policies/kokoseido/jidouteate/annai | a14fe7f49417 | downloaded |

## 9. Household spending and population weighting

| File | Title | URL | sha256 | Status |
|---|---|---|---|---|
| stats/estat_kakei.html | 総務省統計局 家計調査 | https://www.stat.go.jp/data/kakei/index.html | 3196a5e796d3 | landing page only |
| stats/stat_zenkoku_kakei_kozo.html | 全国家計構造調査 2024 | https://www.stat.go.jp/data/zenkokukakei/2024/index.html | 678eb22c50ce | landing page only |
| stats/mhlw_kokumin_seikatsu_kiso.html | 厚労省 国民生活基礎調査 | https://www.mhlw.go.jp/toukei/list/20-21.html | 347996dc843c | landing page only |
| stats/nta_minkan_kyuyo.html | 国税庁 民間給与実態統計調査 | https://www.nta.go.jp/publication/statistics/kokuzeicho/minkan/toukei.htm | 1d87d2dbaafa | landing page only |

The specific e-Stat tables (spending by income decile; household counts by type and income band; wage earners by income band) will be picked and downloaded in Milestones 2 and 7. They are not needed for Milestones 0–1.

## 10. Existing tool

| Item | Location | Notes |
|---|---|---|
| OpenFisca-Japan repository | https://github.com/project-inclusive/OpenFisca-Japan | Inspected at commit `1f8d13dbe735b064373fe67377859454dd750b9c` (2026-08-26). Not vendored into this repo; see `docs/COVERAGE.md`. |
| scrapbox_openfisca_mcp.json | https://scrapbox.io/api/pages/c4j/OpenFisca-Japan_MCP/text | Code for Japan design note on the OpenFisca-Japan MCP server. sha256 ece8076e7e63. downloaded |
