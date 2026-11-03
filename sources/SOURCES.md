# Sources index

Most files were downloaded on **2026-10-29** with `curl`; files added later, from 2026-10-30 to 2026-11-03, have their download date in the table or in the parameter file that cites them. Paths are relative to `sources/`.
Every file's SHA-256 fingerprint is in `sources/SHA256SUMS`. Check all of them with `cd sources && shasum -a 256 -c SHA256SUMS` (every line should end in `OK`).
Plain-text copies of every PDF are in `sources/text/` (regenerate with `.venv/bin/python -I scripts/pdf_to_text.py sources`).

**Which files are in the public repository (checked 2026-11-01).** Documents from national ministries and agencies (内閣官房, こども家庭庁, 厚生労働省, 国税庁, 総務省, 統計局/e-Stat) are published under the 公共データ利用規約（第1.0版）/ 政府標準利用規約（第2.0版）, which allow redistribution with credit; 出典 is each file's publisher and URL below. 日本年金機構 pages are 転載フリー. Code for Japan's Scrapbox page is CC BY 4.0. **Not stored in git**, because their publishers do not allow redistribution or we found no terms that allow it: 大和総研 (Daiwa), 連合 (Rengo, two files), 新宿区 (Shinjuku City), other city and ward pages (大田区, 中央区, 足立区) and 協会けんぽ files. `make fetch-sources` downloads them from the publisher (list: `EXTERNAL.tsv`), and `make check-sources` checks their fingerprints; the three 協会けんぽ HTML pages change byte-for-byte on every download, so their original fingerprints are kept, unchecked, in `SHA256SUMS.volatile`.

Status key: **downloaded** = file is here; **landing page only** = we have the index page, the actual table/PDF still has to be picked and downloaded; **MISSING** = could not be fetched.

> **Important finding.** The spec (Section 1) calls the July 13, 2026 document the "final government draft". The council's own pages show that July 13 was the **draft interim summary** (中間とりまとめ（案）). It was followed by the adopted interim summary (July 29), a **Cabinet decision on the basic policy (Aug 5)**, a Cabinet-decided **outline for the food consumption tax cut plus a new "就業者負担軽減支援金" (worker burden-relief payment) (Sep 15)**, and a **bill submitted Oct 9**. See OPEN_QUESTIONS Q1 and Q2.

## 1. Government credit design (Cabinet Secretariat, 社会保障国民会議)

Index: https://www.cas.go.jp/jp/seisaku/kokuminkaigi/ (saved as `gov/kokuminkaigi_index.html`). These pages open in an ordinary browser; on 2026-11-03 the site answered "not found" to some automated tools (curl's default user agent), so `make fetch-sources` sends a browser user agent.

| File | Title (as on the site) | Published | URL | Pages | Status |
|---|---|---|---|---|---|
| gov/20260527_index.html | 実務者会議（第12回）議事次第・資料 | 2026-05-27 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260527/index.html | – | downloaded |
| gov/20260527_00_agenda.pdf | 第12回 議事次第 | 2026-05-27 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260527/00_agenda.pdf | 1 | downloaded |
| gov/20260527_01_siryou1.pdf | 資料1 議題 | 2026-05-27 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260527/01_siryou1.pdf | 1 | downloaded |
| gov/20260527_02_siryou2.pdf | 資料2 給付付き税額控除のイメージ（中間とりまとめに向けた議論の整理） | 2026-05-27 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260527/02_siryou2.pdf | 4 | downloaded |
| gov/20260527_11_siryou1.pdf | 参考資料1 同上 参考資料 (charts) | 2026-05-27 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260527/11_siryou1.pdf | 12 | downloaded |
| gov/20260527_12_siryou2.pdf | 参考資料2 中間とりまとめに向けた議論の整理（第11回 5/20 資料7） | 2026-05-27 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260527/12_siryou2.pdf | 11 | downloaded |
| gov/20260527_minutes.pdf | 第12回 議事要旨 | 2026-05-27 meeting | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260527/minutes.pdf | 9 | downloaded |
| gov/20260713_index.html | 実務者会議（第18回）議事次第・資料 | 2026-07-13 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260713/index.html | – | downloaded |
| gov/20260713_00_agenda.pdf | 第18回 議事次第 | 2026-07-13 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260713/00_agenda.pdf | 1 | downloaded |
| gov/20260713_01_siryou1.pdf | 資料1 議題 | 2026-07-13 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260713/01_siryou1.pdf | 1 | downloaded |
| gov/20260713_02_siryou2.pdf | 資料2 中間とりまとめ（案）（給付付き税額控除の本格導入部分） | 2026-07-13 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260713/02_siryou2.pdf | 5 | downloaded |
| gov/20260713_11_siryou1.pdf | 参考資料1 給付付き税額控除のイメージ（5/27 資料2の抜粋） | 2026-07-13 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260713/11_siryou1.pdf | 1 | downloaded |
| gov/20260713_minutes.pdf | 第18回 議事要旨 | 2026-07-13 meeting | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260713/minutes.pdf | 7 | downloaded |
| gov/20260729-4_01_siryou1.pdf | 中間とりまとめ（社会保障国民会議 令和8年7月29日） | 2026-07-29 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260729-4/01_siryou1.pdf | 8 | downloaded |
| gov/20260729-4_02_siryou2.pdf | 「給付付き税額控除」のイメージ（中間とりまとめ） | 2026-07-29 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260729-4/02_siryou2.pdf | 3 | downloaded |
| gov/20260805_01_siryou1.pdf | 「給付付き税額控除」の制度導入の基本方針（令和8年8月5日閣議決定） | 2026-08-05 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260805/01_siryou1.pdf | 13 | downloaded |
| gov/20260805_02_siryou2.pdf | 参考資料1 | 2026-08-05 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260805/02_siryou2.pdf | 3 | downloaded |
| gov/20260805_03_siryou3.pdf | 参考資料2（7月30日総理会見のポイント） | 2026-08-05 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260805/03_siryou3.pdf | 8 | downloaded |

Not yet downloaded (available on the index page if needed later): agendas/materials of the other 30+ expert and working-group meetings (Feb–Sep 2026), member list, 20261009 `siryou5.pdf` 参照条文 (3.8 MB, statutory cross-references).

## 2. Food consumption tax cut (+ worker burden-relief payment)

| File | Title | Published | URL | Pages | Status |
|---|---|---|---|---|---|
| gov/20260915_01_siryou1.pdf | 飲食料品消費税率の臨時的な引下げ及び就業者負担軽減支援金の導入に関する大綱（令和8年9月15日閣議決定） | 2026-09-15 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260915/01_siryou1.pdf | 16 | downloaded |
| gov/20260915_02_siryou2.pdf | 同 概要資料 | 2026-09-15 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260915/02_siryou2.pdf | 3 | downloaded |
| gov/20261009_siryou1.pdf | 法律案 概要 | 2026-10-09 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20261009/siryou1.pdf | 1 | downloaded |
| gov/20261009_siryou2.pdf | 法律案 要綱 | 2026-10-09 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20261009/siryou2.pdf | 8 | downloaded |
| gov/20261009_siryou3.pdf | 法律案・理由 | 2026-10-09 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20261009/siryou3.pdf | 83 | downloaded |
| gov/20261009_siryou4.pdf | 新旧対照表 | 2026-10-09 | https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20261009/siryou4.pdf | 37 | downloaded |

Party proposals: **not collected yet**. Choosing which party documents to include touches political wording, so it is a decision for the project owner (OPEN_QUESTIONS Q12).

## 3. Rengo design

| File | URL | Status |
|---|---|---|
| rengo/zeiseikaikakukoso20250528.pdf | 連合「税制改革構想（第4次）」（改訂版）, 2025-05-28, 58 pages — https://www.jtuc-rengo.or.jp/activity/kurashi/zei/data/zeiseikaikakukoso20250528.pdf | Downloaded 2026-11-01. **Not in git** (no redistribution terms found; fetched by `make`). |
| rengo/kokuminkaigi_20260519_siryou3.pdf | 2026年度 連合の重点政策 (社会保障国民会議 2026-05-19 資料3), 5 pages — https://www.cas.go.jp/jp/seisaku/kokuminkaigi/contents/20260519/03_siryou3.pdf | Downloaded 2026-11-01. Written by Rengo, so treated like Rengo's own files: **not in git**, fetched by `make`. |

The original page (…/teigen/?p=5465) and the whole 政策提言 section still showed "メンテナンス中" on 2026-11-01.

## 4. Daiwa design

| File | Title | Published | URL | Pages | Status |
|---|---|---|---|---|---|
| daiwa/daiwa_20251010.pdf | 働く低所得者の負担を軽減する「社会保険料還付付き税額控除」の提案 ― 追加財政負担なしで課税最低限（年収の壁）178 万円達成も可能（大和総研, p.1） | 2025-10-10 (p.1) | https://www.dir.co.jp/report/research/law-research/tax/20251010_025349.pdf | 8 | downloaded |

Note: this report predates the council's work. Whether Daiwa published an updated design in 2026 is still to be checked (OPEN_QUESTIONS Q7).

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

The NTA's 年末調整のしかた (2026 edition) with its worked examples is in section 11.

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

The 2026 part-time coverage rules (the 88,000-yen monthly wage test ended on 2026-10-01) and the April 2026 dependant test are in section 12.

## 7. National health insurance and national pension

| File | Title | URL | Status |
|---|---|---|---|
| social/nenkin_kokumin_hokenryo.html | 日本年金機構 国民年金保険料 | https://www.nenkin.go.jp/service/kokunen/hokenryo/hokenryo.html | downloaded |
| – | Reference municipality NHI rules | – | Shinjuku ward, chosen 2026-10-30; files in section 11 |

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

| File | Title (publisher, date) | URL | Status and use |
|---|---|---|---|
| stats/zkk2024_shotoku_3-32-1.xlsx | 令和6年全国家計構造調査 所得 第3-32-1表 年間収入階級，世帯類型，所得構成別1世帯当たり年間収入額（総務省統計局, 2026-08-28） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040482919&fileKind=0 | downloaded 2026-11-01; population view households (H-17: A) |
| stats/zkk2024_kakei_1-21.xlsx | 令和6年全国家計構造調査 家計収支 第1-21表 年間収入階級・十分位階級別1世帯当たり1か月間の収入と支出（総務省統計局, 2025-12-19） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040379252&fileKind=0 | downloaded 2026-11-01; food spending (H-17: A) |
| stats/kakei2025_sosetai_3.xlsx | 家計調査 2025年 総世帯 第3表 年間収入五分位・十分位階級別（総務省統計局, 2026-02-06） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040409804&fileKind=0 | downloaded 2026-11-01; check only |
| stats/kiso2025_setai_2.csv | 2025年国民生活基礎調査 世帯票 第2表 世帯数－構成割合，世帯構造・年次別（厚生労働省, 2026-07-15） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040472271&fileKind=1 | downloaded 2026-11-01; check only |
| stats/minkan_r7_3.xlsx | 令和7年分民間給与実態統計調査 第3表 給与階級別の総括表（国税庁, e-Stat copy, 2026-09-29） | https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040505068&fileKind=0 | downloaded 2026-11-01; check only |

The tables were chosen by the project owner on 2026-11-01 (options in `docs/M7_DATA_OPTIONS.md`). All five are national statistics published under the 公共データ利用規約 1.0 and are stored in this repository.

## 10. Existing tool

| Item | Location | Notes |
|---|---|---|
| OpenFisca-Japan repository | https://github.com/project-inclusive/OpenFisca-Japan | Inspected at commit `1f8d13dbe735b064373fe67377859454dd750b9c` (2026-08-26). Not vendored into this repo; see `docs/COVERAGE.md`. |
| scrapbox_openfisca_mcp.json | https://scrapbox.io/api/pages/c4j/OpenFisca-Japan_MCP/text | Code for Japan design note on the OpenFisca-Japan MCP server. downloaded |

## 11. Added 2026-10-30

| File | Title | Published | URL | Used for |
|---|---|---|---|---|
| tax/nta_nencho2026_all.pdf | 令和8年分 年末調整のしかた (full) | 2026-10 | https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/nencho_all.pdf | employment-income table (pp.47–54), deduction tables (pp.55–56), worked example (pp.57–59) |
| tax/nta_nencho2026_102.pdf | 同 「昨年と比べて変わった点」 | 2026-10 | https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/102.pdf | 2026 changes |
| tax/nta_nencho2026_index.html | 同 index page | 2026-10 | https://www.nta.go.jp/publication/pamph/gensen/nencho2026/01.htm | – |
| tax/nta_r8_kiso_qa.pdf | 令和8年度税制改正（所得税の基礎控除の引上げ等関係）Ｑ＆Ａ | 2026-05 | https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf | timing of 2026 changes |
| tax/nta_1600_fig01.png, fig02.png | No.1600 pension-income tables (images) | 2026 | https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/img/1600_01.png | public pension deduction |
| tax/nta_1171_hitorioya.html | No.1171 ひとり親控除 | 2026 | https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1171.htm | single-parent deduction |
| tax/nta_1175_kinro_gakusei.html | No.1175 勤労学生控除 | 2026 | https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1175.htm | working-student deduction |
| tax/nta_1411_shotoku_kingaku_chosei.html | No.1411 所得金額調整控除 | 2026 | https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1411.htm | income-adjustment deduction |
| tax/soumu_kojin_juminzei_kiso_kojo_r8.pdf | 個人住民税の基礎控除等について（総務省 資料３） | 2026-05-29 | https://www.soumu.go.jp/main_content/001075462.pdf | resident tax follows the new employment deduction; basic deduction stays 430,000 |
| shinjuku/hoken01_001028.html | 新宿区 国民健康保険料の計算方法（令和8年度） | 2026 | https://www.city.shinjuku.lg.jp/hoken/hoken01_001028.html | NHI rates |
| shinjuku/hoken01_002030.html | 新宿区 保険料の減免について | 2026 | https://www.city.shinjuku.lg.jp/hoken/hoken01_002030.html | NHI reductions |
| shinjuku/000452428.pdf | 新宿区 令和8年度 国民健康保険料 概算早見表 | 2026 | https://www.city.shinjuku.lg.jp/content/000452428.pdf | NHI test oracle |
| shinjuku/file04_03_00001.html | 新宿区 住民税について | 2025-02-17 | https://www.city.shinjuku.lg.jp/hoken/file04_03_00001.html | resident-tax exemption limits |
| shinjuku/000434385.pdf | 新宿区 令和7年度住民税 税額の算出方法等 | 2025 | https://www.city.shinjuku.lg.jp/content/000434385.pdf | resident deductions, 調整控除, per-capita levy |
| social/mhlw_koyohoken_ritsu_r8.pdf | 令和8年度 雇用保険料率のご案内 | 2026 | https://www.mhlw.go.jp/content/001692566.pdf | employment insurance 0.5% |
| social/mhlw_tekiyoukakudai_taisho.html | 社会保険加入の要件（適用拡大特設サイト） | 2026 | https://www.mhlw.go.jp/tekiyoukakudai/jugyouin/taisho/ | part-time coverage rules |
| social/nenkin_tanjikan.html | 日本年金機構 短時間労働者の適用拡大 | 2026-10-01 | https://www.nenkin.go.jp/service/kounen/tekiyo/jigyosho/tanjikan.html | part-time coverage rules |
| social/kyoukaikenpo_hifuyosha_r8.html | 協会けんぽ 令和8年度被扶養者資格の再確認 | 2026 | https://www.kyoukaikenpo.or.jp/about/business/dependent_status/001/index.html | dependant income limits |

Fingerprints for every file are in `sources/SHA256SUMS` (69 files).

## 12. Added later: laws, cabinet orders and local guides

Laws and cabinet orders (not copyrighted, 著作権法13条) and national documents are stored in git; city, ward and 協会けんぽ pages are fetched by `make` (EXTERNAL.tsv).

| File | Title | Published | URL | Used for |
|---|---|---|---|---|
| law/chihozeiho_20270101.xml | 地方税法, text in force from 2027-01-01 (令和8年法律第2号; applies to 令和9年度) | 2026-03-31 | https://laws.e-gov.go.jp/api/2/law_data/325AC0000000226_20270101_508AC0000000002?law_full_text_format=xml&response_format=xml | resident-tax deductions, limits, rates, 調整控除, rounding (20条の4の2), relief band (附則3条の3) |
| law/chihozeiho.xml, law/chihozeiho_revisions.json | 地方税法 as in force on 2026-11-03, and its revision list | 2026-11-01 | https://laws.e-gov.go.jp/api/1/lawdata/325AC0000000226 | check of which text applies when |
| law/chihozeiho_sekourei_20270101.xml | 地方税法施行令, text from 2027-01-01 | 2026 | https://laws.e-gov.go.jp/law/325CO0000000245 | single-parent child's income limit |
| law/shotokuzeiho_20261201.xml | 所得税法, text from 2026-12-01 (令和8年法律第12号) | 2026-03-31 | https://laws.e-gov.go.jp/law/340AC0000000033 | working-student limit 890,000 |
| law/kokuho_sekourei_333CO0000000362_asof20260401.xml, law/kokuho_sekourei_333CO0000000362.xml | 国民健康保険法施行令 (2026-04-01 and current) | 2026 | https://laws.e-gov.go.jp/api/1/lawdata/333CO0000000362 | NHI reduction: who counts as an earner (29条の7第6項第1号, 附則5条) |
| law/koyo_hoken_ho_349AC0000000116.xml | 雇用保険法 (downloaded 2026-11-03) | 2026 | https://laws.e-gov.go.jp/api/1/lawdata/349AC0000000116 | 6条: who is outside employment insurance (no pay condition) |
| social/mhlw_r8_minimum_wage_ichiran.pdf | 厚生労働省 令和8年度地域別最低賃金 全国一覧 (downloaded 2026-11-03) | 2026 | https://www.mhlw.go.jp/content/11200000/001753404.pdf | lowest rate in force October–December 2026: 1,023 yen (特定減額特例, wall_H1.md revision 2) |
| law/seirei_R8_275_shikoukijitsu.pdf | 令和8年政令第275号 (start date 2026-10-01) | 2026-09-11 | https://www.mhlw.go.jp/hourei/doc/hourei/H260911T0020.pdf | end of the 88,000-yen wage test |
| law/kenkou_hoken_ho_211AC0000000070.xml, law/kousei_nenkin_hoken_ho_329AC0000000115.xml, law/kokumin_nenkin_ho_334AC0000000141.xml, law/kokumin_kenkou_hoken_ho_333AC0000000192.xml | 健康保険法, 厚生年金保険法, 国民年金法, 国民健康保険法 | 2026 | https://laws.e-gov.go.jp/ | coverage from 2026-10-01; premiums counted by month; national pension ages 20–59 (国民年金法7条) |
| social/mhlw_tsuchi_R80911_hohatsu0911_6.pdf | 保発0911第6号 | 2026-09-11 | https://www.mhlw.go.jp/hourei/doc/tsuchi/T260915T0020.pdf | wage test ends 2026-10-01 |
| social/nenkin_oshirase_20261001_chingin_yoken_teppai.html | 日本年金機構 賃金要件の撤廃 | 2026-10-01 | https://www.nenkin.go.jp/oshirase/taisetu/jigyosho/2026/202610/100104.html | wage test ends 2026-10-01 |
| social/mhlw_tekiyoukakudai_qa.html | 厚労省 適用拡大 Q&A | 2026 | https://www.mhlw.go.jp/tekiyoukakudai/qa/ | wage test ends October 2026 |
| social/nenkin_oshirase_20260501_hifuyosha.html | 日本年金機構 被扶養者の年間収入（労働契約による判定） | 2026-05-01 | https://www.nenkin.go.jp/oshirase/taisetu/jigyosho/2026/202605/0501.html | April 2026 dependant test |
| social/mhlw_nenshu_kabe_taiou_001_00002.html | 厚労省「年収の壁」への対応 | 2026 | https://www.mhlw.go.jp/stf/taiou_001_00002.html | temporary income increase (事業主の証明) |
| social/nenkin_gakusei_nofu_tokurei.html | 日本年金機構 学生納付特例 | 2026-10-16 | https://www.nenkin.go.jp/service/kokunen/menjo/20150514.html | student deferral income limit |
| social/mhlw_jimurenraku_R80216_shienkin_qa_T260216S0101.pdf, social/mhlw_jimurenraku_R80216_shienkin_T260216S0100.pdf | 子ども・子育て支援金に関するＱ＆Ａ and covering letter (MHLW, こども家庭庁). Internet Archive copy (captured 2026-02-17); the MHLW link returns 404 | 2026-02-12 | https://www.mhlw.go.jp/content/T260216S0101.pdf | rounding of the employee share (Q38) |
| social/mhlw_kokuho_jourei_junsoku_S340127.html | 国民健康保険条例準則 (MHLW model ordinance) | 1959, consolidated | MHLW 法令等データベース (URL not recorded when saved) | NHI prorated by month |
| shinjuku/000452430.pdf | 新宿区 令和8年度 国民健康保険料の軽減判定 早見表 | 2026 | https://www.city.shinjuku.lg.jp/content/000452430.pdf | NHI reduction earners (not in git) |
| shinjuku/hoken01_000001_00058.html | 新宿区 保険料納入通知書の見方 | 2026-05-18 | https://www.city.shinjuku.lg.jp/kenkou/hoken01_000001_00058.html | NHI 月割 (not in git) |
| shinjuku/file02_03_00001.html | 新宿区 保険料について | 2026-03-25 | https://www.city.shinjuku.lg.jp/hoken/file02_03_00001.html | NHI from the month of joining (not in git) |
| shinjuku/hoken01_002065_00003.html | 新宿区 保険料 | 2026 | https://www.city.shinjuku.lg.jp/kenkou/hoken01_002065_00003.html | NHI (not in git) |
| social/kyoukaikenpo_hihusyoumeisyo2311.pdf | 協会けんぽ 一時的な収入増加の事業主証明 (様式) | 2023-11 | https://www.kyoukaikenpo.or.jp/assets/hihusyoumeisyo2311.pdf | temporary income increase (not in git) |
| tax/ota_keisan_no_shikumi.html | 大田区 住民税の計算のしくみ | 2026-10-27 | https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/keisannosikumi.html | worked example of separate rounding (not in git) |
| tax/ota_shotokukojo.html | 大田区 所得控除 | 2026-08-31 | https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/shotokukojyo.html | 令和9年度 deduction tables (not in git) |
| tax/chuo_r9_juminzei_kaisei.html | 中央区 令和9年度から適用される個人住民税の主な改正 | 2026-09-01 | https://www.city.chuo.lg.jp/a0009/kurashi/zeikin/juuminzei/r9kaisei.html | 令和9年度 limits (not in git) |
| tax/adachi_r9_juminzei_kaisei.html | 足立区 令和9年度から適用される主な税制改正等 | 2026-11-02 | https://www.city.adachi.tokyo.jp/ze/2027zeisei.html | 令和9年度 changes (not in git) |

