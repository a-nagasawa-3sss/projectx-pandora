# 広告配信プラットフォーム DB定義書

最終更新日: 2025-11-10
作成: プラットフォーム開発チーム

## 1. ER概要
- advertisers（広告主マスタ）
- agencies（代理店マスタ）
- publishers（媒体社マスタ）
- campaigns（キャンペーン）
- delivery_daily（日次配信実績）
- invoices（請求）

campaigns は advertisers / agencies / publishers のそれぞれに紐づく。
delivery_daily / invoices は campaigns に紐づく。

---

## 2. advertisers（広告主マスタ）

| カラム名 | 型 | 説明 |
| --- | --- | --- |
| id | TEXT (PK) | 広告主ID |
| name | TEXT | 広告主名 |

---

## 3. agencies（代理店マスタ）

| カラム名 | 型 | 説明 |
| --- | --- | --- |
| id | TEXT (PK) | 代理店ID |
| name | TEXT | 代理店名 |
| margin_rate | REAL | 代理店マージン率（全キャンペーン共通） |

---

## 4. publishers（媒体社マスタ）

| カラム名 | 型 | 説明 |
| --- | --- | --- |
| id | TEXT (PK) | 媒体社ID |
| name | TEXT | 媒体社名 |

---

## 5. campaigns（キャンペーン）

| カラム名 | 型 | 説明 |
| --- | --- | --- |
| id | TEXT (PK) | キャンペーンID |
| name | TEXT | キャンペーン名 |
| advertiser_id | TEXT (FK) | 広告主ID（advertisers.id） |
| agency_id | TEXT (FK) | 代理店ID（agencies.id） |
| publisher_id | TEXT (FK) | 媒体社ID（publishers.id） |
| billing_type | TEXT | 課金形態（CPM / CPC） |
| unit_price | REAL | 単価（税抜）。CPMは1,000imp単価、CPCは1クリック単価 |
| contract_margin_rate | REAL | キャンペーン個別の契約マージン率（任意設定。未設定の場合は agencies.margin_rate を適用） |
| budget | REAL | 予算（円） |
| start_date | TEXT | 配信開始日（YYYY-MM-DD） |
| end_date | TEXT | 配信終了日（YYYY-MM-DD） |

---

## 6. delivery_daily（日次配信実績）

| カラム名 | 型 | 説明 |
| --- | --- | --- |
| id | INTEGER (PK) | 連番 |
| campaign_id | TEXT (FK) | キャンペーンID |
| date | TEXT | 対象日（YYYY-MM-DD） |
| impressions | INTEGER | 表示回数（総数） |
| clicks | INTEGER | クリック数 |
| conversions | INTEGER | コンバージョン数 |

---

## 7. invoices（請求）

| カラム名 | 型 | 説明 |
| --- | --- | --- |
| id | TEXT (PK) | 請求ID |
| campaign_id | TEXT (FK) | キャンペーンID |
| billing_month | TEXT | 請求対象月（YYYY-MM） |
| media_cost | REAL | メディアコスト（円、税抜） |
| tax_rate | REAL | 消費税率 |
| agency_margin_rate | REAL | 適用された代理店マージン率 |
| amount | REAL | 請求金額（円、税込） |

---

## 8. 改訂履歴

| 版数 | 日付 | 内容 |
| --- | --- | --- |
| 1.0 | 2025-08-20 | 初版作成 |
| 1.1 | 2025-11-10 | campaigns に contract_margin_rate を追加（個別契約マージン対応） |
