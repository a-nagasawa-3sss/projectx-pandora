"""DBの初期化とサンプルデータ投入を行うスクリプト。

実行方法:
    python data/seed.py

このスクリプトは pandora/data/pandora.db を作成（既存の場合は再作成）し、
マスタデータ・配信実績・請求データを投入する。
あわせて媒体社側の配信ログ（pandora/data/logs/publisher_delivery_log.csv）も生成する。
"""

import csv
import random
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import models  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent
LOGS_DIR = DATA_DIR / "logs"

BILLING_MONTH = "2026-05"
DAYS = [date(2026, 5, 1) + timedelta(days=i) for i in range(31)]

TAX_RATE = 0.10

# キャンペーンごとの配信実績生成パラメータ
# bot_rate: 媒体社の生ログ上のインプレッション数のうち、
#           bot/不正アクセスとしてプラットフォーム側で除外される割合
DELIVERY_PARAMS = {
    "C001": {"impressions_range": (28000, 35000), "ctr": 0.012, "cvr": 0.03, "bot_rate": 0.0},
    "C002": {"impressions_range": (45000, 58000), "ctr": 0.009, "cvr": 0.025, "bot_rate": 0.12},
    "C003": {"impressions_range": (20000, 27000), "ctr": 0.015, "cvr": 0.02, "bot_rate": 0.0},
    "C004": {"impressions_range": (18000, 24000), "ctr": 0.045, "cvr": 0.05, "bot_rate": 0.0},
    "C005": {"impressions_range": (15000, 20000), "ctr": 0.011, "cvr": 0.028, "bot_rate": 0.025},
}


def generate_delivery_rows(params, days, rng):
    rows = []
    for d in days:
        raw_impressions = rng.randint(*params["impressions_range"])
        valid_impressions = round(raw_impressions * (1 - params["bot_rate"]))
        clicks = max(1, round(valid_impressions * params["ctr"] * rng.uniform(0.85, 1.15)))
        conversions = max(0, round(clicks * params["cvr"] * rng.uniform(0.7, 1.3)))
        rows.append(
            {
                "date": d,
                "raw_impressions": raw_impressions,
                "valid_impressions": valid_impressions,
                "clicks": clicks,
                "conversions": conversions,
            }
        )
    return rows


def main():
    rng = random.Random(42)

    # DBファイルを作り直す
    db_path = DATA_DIR / "pandora.db"
    if db_path.exists():
        db_path.unlink()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # --- マスタデータ ---
    advertisers = [
        models.Advertiser(id="A001", name="株式会社サンライズフーズ"),
        models.Advertiser(id="A002", name="株式会社テックウェーブ"),
        models.Advertiser(id="A003", name="株式会社グリーンコスメ"),
    ]

    # 代理店マージン率はマスタ上は一律20%
    agencies = [
        models.Agency(id="AG001", name="アドバンスメディア", margin_rate=0.20),
        models.Agency(id="AG002", name="ブリッジコミュニケーションズ", margin_rate=0.20),
        models.Agency(id="AG003", name="フォーカスプランニング", margin_rate=0.20),
    ]

    publishers = [
        models.Publisher(id="P001", name="ニュースポータル Daily Spark"),
        models.Publisher(id="P002", name="動画配信サービス ClipNest"),
        models.Publisher(id="P003", name="SNS情報アプリ Trendy"),
    ]

    db.add_all(advertisers + agencies + publishers)
    db.flush()

    # --- キャンペーン ---
    # unit_price は実態としては税込価格で登録されている
    # （DB定義書・IF仕様書上は「税抜」と説明されているが実データは税込）
    campaigns = [
        models.Campaign(
            id="C001",
            name="サンライズフーズ春の新商品キャンペーン",
            advertiser_id="A001",
            agency_id="AG001",
            publisher_id="P001",
            billing_type="CPM",
            unit_price=330.0,
            budget=600000.0,
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 31),
        ),
        models.Campaign(
            id="C002",
            name="テックウェーブ新製品ローンチ動画広告",
            advertiser_id="A002",
            agency_id="AG002",
            publisher_id="P002",
            billing_type="CPM",
            unit_price=550.0,
            budget=900000.0,
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 31),
        ),
        models.Campaign(
            id="C003",
            name="テックウェーブSNSプロモーション",
            advertiser_id="A002",
            agency_id="AG002",
            publisher_id="P003",
            billing_type="CPM",
            unit_price=400.0,
            budget=500000.0,
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 31),
        ),
        models.Campaign(
            id="C004",
            name="グリーンコスメ検索連動広告",
            advertiser_id="A003",
            agency_id="AG003",
            publisher_id="P001",
            billing_type="CPC",
            unit_price=45.0,
            budget=300000.0,
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 31),
        ),
        models.Campaign(
            id="C005",
            name="サンライズフーズ動画リターゲティング",
            advertiser_id="A001",
            agency_id="AG001",
            publisher_id="P002",
            billing_type="CPM",
            unit_price=280.0,
            budget=400000.0,
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 31),
        ),
    ]
    db.add_all(campaigns)
    db.flush()

    campaigns_by_id = {c.id: c for c in campaigns}
    agencies_by_id = {a.id: a for a in agencies}

    # --- 配信実績・媒体社配信ログ ---
    publisher_log_rows = []
    delivery_by_campaign = {}

    for campaign_id, params in DELIVERY_PARAMS.items():
        rows = generate_delivery_rows(params, DAYS, rng)
        delivery_by_campaign[campaign_id] = rows

        for row in rows:
            db.add(
                models.DeliveryDaily(
                    campaign_id=campaign_id,
                    date=row["date"],
                    impressions=row["valid_impressions"],
                    clicks=row["clicks"],
                    conversions=row["conversions"],
                )
            )

        # 媒体社P002（ClipNest）が配信するキャンペーンのみ、媒体社側の生ログを出力する
        # 媒体社側は bot/不正アクセスを除外する前の「総表示回数」を記録している
        if campaigns_by_id[campaign_id].publisher_id == "P002":
            for row in rows:
                publisher_log_rows.append(
                    {
                        "date": row["date"].isoformat(),
                        "campaign_id": campaign_id,
                        "campaign_name": campaigns_by_id[campaign_id].name,
                        "impressions": row["raw_impressions"],
                        "clicks": row["clicks"],
                        "conversions": row["conversions"],
                    }
                )

    # --- 請求データ ---
    # 実装済みの請求計算ロジック（不具合を含む）:
    #   media_cost = 配信実績 * unit_price（CPMは1000imp単価、CPCは1クリック単価）
    #   amount = media_cost * (1 + tax_rate) * (1 + agency_margin_rate)
    # unit_price は実態として税込のため、(1 + tax_rate) を乗じる本処理は二重課税になっている。
    # また agency_margin_rate は agencies マスタの一律値を参照するため、
    # C003 の特別契約マージン率（15%）が反映されていない。
    for campaign in campaigns:
        rows = delivery_by_campaign[campaign.id]
        if campaign.billing_type == "CPM":
            total_impressions = sum(r["valid_impressions"] for r in rows)
            media_cost = total_impressions / 1000 * campaign.unit_price
        else:  # CPC
            total_clicks = sum(r["clicks"] for r in rows)
            media_cost = total_clicks * campaign.unit_price

        agency_margin_rate = agencies_by_id[campaign.agency_id].margin_rate
        amount = media_cost * (1 + TAX_RATE) * (1 + agency_margin_rate)

        db.add(
            models.Invoice(
                id=f"INV-{BILLING_MONTH}-{campaign.id}",
                campaign_id=campaign.id,
                billing_month=BILLING_MONTH,
                media_cost=round(media_cost, 2),
                tax_rate=TAX_RATE,
                agency_margin_rate=agency_margin_rate,
                amount=round(amount, 2),
            )
        )

    db.commit()

    # --- プラットフォーム側APIアクセスログの出力 ---
    # 5月分の請求が確定した6月上旬に、各代理店担当者がAPIで実績・請求を確認した記録。
    write_platform_access_log(LOGS_DIR / "platform_access.log", campaigns_by_id, rng)

    db.close()

    # --- 媒体社配信ログCSVの出力 ---
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    publisher_log_path = LOGS_DIR / "publisher_delivery_log.csv"
    with publisher_log_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["date", "campaign_id", "campaign_name", "impressions", "clicks", "conversions"]
        )
        writer.writeheader()
        for row in publisher_log_rows:
            writer.writerow(row)

    print(f"DB created at: {db_path}")
    print(f"Publisher delivery log written to: {publisher_log_path}")
    print(f"Platform access log written to: {LOGS_DIR / 'platform_access.log'}")


def write_platform_access_log(path, campaigns_by_id, rng):
    agency_clients = {
        "AG001": "10.0.12.31",
        "AG002": "10.0.12.45",
        "AG003": "10.0.12.58",
    }

    entries = []
    for day_offset in range(5):  # 2026-06-01 〜 2026-06-05
        log_date = date(2026, 6, 1) + timedelta(days=day_offset)
        for campaign in campaigns_by_id.values():
            client_ip = agency_clients[campaign.agency_id]

            # 配信実績の確認
            hour, minute, second = rng.randint(9, 18), rng.randint(0, 59), rng.randint(0, 59)
            entries.append(
                (
                    log_date,
                    hour,
                    minute,
                    second,
                    client_ip,
                    f"GET /campaigns/{campaign.id}/delivery?from=2026-05-01&to=2026-05-31",
                    200,
                    rng.randint(40, 220),
                )
            )

            # 請求情報の確認
            hour, minute, second = rng.randint(9, 18), rng.randint(0, 59), rng.randint(0, 59)
            entries.append(
                (
                    log_date,
                    hour,
                    minute,
                    second,
                    client_ip,
                    f"GET /campaigns/{campaign.id}/invoices",
                    200,
                    rng.randint(20, 120),
                )
            )

            # AG002はC003の請求内容を繰り返し確認している（マージン率の問い合わせの裏付け）
            if campaign.id == "C003" and day_offset >= 2:
                for _ in range(rng.randint(1, 3)):
                    hour, minute, second = rng.randint(9, 18), rng.randint(0, 59), rng.randint(0, 59)
                    entries.append(
                        (
                            log_date,
                            hour,
                            minute,
                            second,
                            client_ip,
                            f"GET /campaigns/{campaign.id}/invoices",
                            200,
                            rng.randint(20, 120),
                        )
                    )

    entries.sort(key=lambda e: (e[0], e[1], e[2], e[3]))

    with path.open("w", encoding="utf-8") as f:
        for log_date, hour, minute, second, client_ip, request_line, status, duration_ms in entries:
            timestamp = f"{log_date.isoformat()}T{hour:02d}:{minute:02d}:{second:02d}+09:00"
            f.write(f'{timestamp} {client_ip} "{request_line}" {status} {duration_ms}ms\n')


if __name__ == "__main__":
    main()
