# 広告配信プラットフォーム IF仕様書

最終更新日: 2025-12-05
作成: プラットフォーム開発チーム

## 1. 概要
本書は、広告配信プラットフォームAPI（以下「本API」）のインターフェース仕様を定義する。
代理店・媒体社向け管理画面、および各社の社内システムから本APIを利用する際の参照仕様とする。

## 2. 共通事項
- ベースURL: `http://<host>:<port>/`
- レスポンス形式: JSON
- 文字コード: UTF-8
- 日付形式: `YYYY-MM-DD`

## 3. マスタ系API

### 3.1 広告主一覧取得
`GET /advertisers`

| フィールド | 型 | 説明 |
| --- | --- | --- |
| id | string | 広告主ID |
| name | string | 広告主名 |

### 3.2 代理店一覧取得
`GET /agencies`

| フィールド | 型 | 説明 |
| --- | --- | --- |
| id | string | 代理店ID |
| name | string | 代理店名 |
| margin_rate | number | 代理店マージン率（一律） |

### 3.3 媒体社一覧取得
`GET /publishers`

| フィールド | 型 | 説明 |
| --- | --- | --- |
| id | string | 媒体社ID |
| name | string | 媒体社名 |

## 4. キャンペーンAPI

### 4.1 キャンペーン一覧取得
`GET /campaigns`

### 4.2 キャンペーン詳細取得
`GET /campaigns/{campaign_id}`

| フィールド | 型 | 説明 |
| --- | --- | --- |
| id | string | キャンペーンID |
| name | string | キャンペーン名 |
| advertiser_id | string | 広告主ID |
| agency_id | string | 代理店ID |
| publisher_id | string | 媒体社ID |
| billing_type | string | 課金形態（CPM / CPC） |
| unit_price | number | 単価（税抜、円）。CPMの場合は1,000表示あたり、CPCの場合は1クリックあたりの単価 |
| budget | number | キャンペーン予算（円） |
| start_date | string | 配信開始日 |
| end_date | string | 配信終了日 |

## 5. 配信実績API

### 5.1 日次配信実績取得
`GET /campaigns/{campaign_id}/delivery?from={開始日}&to={終了日}`

| フィールド | 型 | 説明 |
| --- | --- | --- |
| date | string | 対象日 |
| impressions | integer | 配信した広告の表示回数（総数） |
| clicks | integer | クリック数 |
| conversions | integer | コンバージョン数 |

`from` / `to` を省略した場合は、キャンペーンの全期間の実績を返す。

## 6. 請求API

### 6.1 キャンペーン別請求情報取得
`GET /campaigns/{campaign_id}/invoices`

### 6.2 請求情報詳細取得
`GET /invoices/{invoice_id}`

| フィールド | 型 | 説明 |
| --- | --- | --- |
| id | string | 請求ID |
| campaign_id | string | キャンペーンID |
| billing_month | string | 請求対象月（YYYY-MM） |
| media_cost | number | メディアコスト（円） |
| tax_rate | number | 消費税率 |
| agency_margin_rate | number | 適用された代理店マージン率 |
| amount | number | 請求金額（円） |

## 7. 改訂履歴

| 版数 | 日付 | 内容 |
| --- | --- | --- |
| 1.0 | 2025-09-01 | 初版作成 |
| 1.1 | 2025-12-05 | 請求APIのフィールドを追加 |
