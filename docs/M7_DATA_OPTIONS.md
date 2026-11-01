# Milestone 7: which official tables to use (Q8, H-17)

Checked 2026-11-01. Every file below downloads from e-Stat (HTTP 200). All are national government statistics under the 公共データ利用規約 1.0, so they can be stored in the repository with credit.

## The candidate tables

| Key | Survey and table | What it gives | Limits |
|-----|------------------|---------------|--------|
| F1 | 全国家計構造調査 2024, 家計収支 表1-21 ([file](https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040379252&fileKind=0), published 2025-12-19) | Monthly spending by 年間収入十分位, separately for 総世帯, 二人以上 and 単身, with 食料, 酒類 and 外食 split out | Covers October–November 2024 only (no full-year average) |
| F2 | 家計調査 2025, 総世帯 第3表 ([file](https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040409804&fileKind=0), published 2026-02-06) | Full-year average spending by income decile, same food rows | Single-person sample is small; no single-person deciles |
| H1 | 国民生活基礎調査 2025 (2024 income), 所得票 第24表 and 第25表 ([第24表 CSV](https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040473383&fileKind=1), published 2026-07-15) | Households by type (single, couple, couple with children, lone parent, elderly, with children) and ¥0.5m income band | Given as shares per 10,000 households; income is 所得 (a different definition from F1/F2's 年間収入) |
| H2 | 全国家計構造調査 2024, 所得 表3-32-1 ([file](https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040482919&fileKind=0), published 2026-08-28) | Households by 78 types × 年間収入 band, with number of earners | Very detailed; needs more work to group into our eight types |
| C1 | 民間給与実態統計調査 令和7年分 第3表 ([e-Stat copy](https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040505068&fileKind=0), published 2026-09-29) | Full-year private-sector wage earners by ¥1m pay band, men and women | Private sector only; people, not households. Used only as a check |
| C2 | 国民生活基礎調査 2025, 世帯票 第2表 ([CSV](https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040472271&fileKind=1)) | Total households: 55,058 thousand | Used to scale H1, and as a check |

## The options

- **A. One survey for spending and households: F1 + H2.** Food spending and household counts use the same people, the same income definition and the same household types. F2 and C1/C2 are used only as checks.
- **B. Most-cited sources for each part: F1 + H1 (scaled by C2).** The household counts come from the survey most often quoted for income distribution. Two income definitions must be lined up, which is an extra approximation.
- **C. Full-year spending: F2 + H1 (scaled by C2).** Spending is a full-year average but has no single-person deciles. Same income-definition mismatch as B.

C1 is a calibration check in every option.
