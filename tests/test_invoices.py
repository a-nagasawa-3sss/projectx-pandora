"""TC-04 のテスト"""

def test_invoice_amount_matches_calculation_formula(client):
    """TC-04: amount = media_cost * (1 + tax_rate) * (1 + agency_margin_rate) の計算式に基づいて、請求金額が正しく計算されていること、請求IDを指定して詳細を取得できること。"""
    response = client.get("/campaigns/C001/invoices")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    invoice = data[0]
    expected_amount = round(
        invoice["media_cost"] * (1 + invoice["tax_rate"]) * (1 + invoice["agency_margin_rate"]),
        2,
    )
    assert invoice["amount"] == expected_amount

def test_get_invoice_detail(client):
    """TC-04: 請求IDを指定して詳細を取得できること。"""
    response = client.get("/invoices/INV-2026-05-C001")

    assert response.status_code == 200
    data = response.json()
    assert data["campaign_id"] == "C001"
    assert data["billing_month"] == "2026-05"
