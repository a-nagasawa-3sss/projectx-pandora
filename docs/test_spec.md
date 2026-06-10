# 広告配信プラットフォーム テスト仕様書

最終更新日: 2025-09-10
作成: QAチーム

## 1. 目的
本書は、広告配信プラットフォームAPIの主要機能に対するテストケースを定義する。

## 2. テスト環境
- テスト用DB（本番データとは別のサンプルデータ）を使用
- 代理店マージン率はテスト環境の `agencies` マスタ値（一律20%）を使用

---

## 3. テストケース一覧

### TC-01: キャンペーン一覧取得
- 対象: `GET /campaigns`
- 期待結果: 登録済みの全キャンペーンが配列で返却される
- 結果: OK

### TC-02: キャンペーン詳細取得
- 対象: `GET /campaigns/{campaign_id}`
- 期待結果: 指定したキャンペーンIDの詳細情報（unit_price含む）が返却される
- 結果: OK

### TC-03: 日次配信実績取得
- 対象: `GET /campaigns/{campaign_id}/delivery?from=&to=`
- 期待結果: 指定期間の `impressions`（表示回数の総数）, `clicks`, `conversions` が日付順に返却される
- 確認方法: テスト環境の配信ログ集計値とAPIレスポンスのimpressions合計値が一致すること
- 結果: OK（テスト環境データにて確認済み）

### TC-04: 請求金額計算（通常ケース）
- 対象: `GET /campaigns/{campaign_id}/invoices`
- 計算式:
  ```
  media_cost = 配信実績 × unit_price
  amount = media_cost × (1 + tax_rate) × (1 + agency_margin_rate)
  ```
- テストデータ例: media_cost = 100,000円, tax_rate = 0.10, agency_margin_rate = 0.20
  - 期待値: amount = 100,000 × 1.10 × 1.20 = 132,000円
- 結果: OK

### TC-05: 個別契約マージン率を持つキャンペーンの請求金額計算
- 対象: `GET /campaigns/{campaign_id}/invoices`
- 期待結果: `campaigns.contract_margin_rate` が設定されている場合、`agencies.margin_rate` ではなく `contract_margin_rate` を用いて計算されること
- 結果: 未実施（該当するテストデータが用意され次第実施予定）

---

## 4. 既知の課題
- TC-05 は対象データ未整備のため未実施のまま。

## 5. 改訂履歴

| 版数 | 日付 | 内容 |
| --- | --- | --- |
| 1.0 | 2025-09-10 | 初版作成 |
