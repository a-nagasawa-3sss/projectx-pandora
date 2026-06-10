"""TC-03 に対応する正常系テスト。"""


def test_get_delivery_returns_daily_records_in_date_order(client):
    """TC-03: 指定期間のimpressions/clicks/conversionsが日付順に返却される。"""
    response = client.get("/campaigns/C001/delivery?from=2026-05-01&to=2026-05-31")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 31

    dates = [row["date"] for row in data]
    assert dates == sorted(dates)
    assert dates[0] == "2026-05-01"
    assert dates[-1] == "2026-05-31"

    for row in data:
        assert {"date", "impressions", "clicks", "conversions"} <= row.keys()
        assert row["impressions"] >= 0
        assert row["clicks"] >= 0
        assert row["conversions"] >= 0
