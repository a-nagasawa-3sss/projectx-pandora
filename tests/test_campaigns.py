"""TC-01, TC-02 に対応する正常系テスト。"""

EXPECTED_CAMPAIGN_IDS = {"C001", "C002", "C003", "C004", "C005"}


def test_list_campaigns_returns_all_campaigns(client):
    """TC-01: 登録済みの全キャンペーンが配列で返却される。"""
    response = client.get("/campaigns")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert {c["id"] for c in data} == EXPECTED_CAMPAIGN_IDS


def test_get_campaign_detail_includes_unit_price(client):
    """TC-02: 指定したキャンペーンIDの詳細情報（unit_price含む）が返却される。"""
    response = client.get("/campaigns/C001")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "C001"
    assert data["billing_type"] == "CPM"
    assert data["unit_price"] == 330.0
