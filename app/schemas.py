from datetime import date

from pydantic import BaseModel, ConfigDict

# データベースモデルをAPIのレスポンスモデルに変換するためのPydanticモデルを定義
class Advertiser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str

# 広告代理店のモデル
class Agency(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    margin_rate: float

# 媒体社のモデル
class Publisher(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str

# キャンペーンのモデル
class Campaign(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    advertiser_id: str
    agency_id: str
    publisher_id: str
    billing_type: str
    unit_price: float
    budget: float
    start_date: date
    end_date: date

# キャンペーンの日次配信実績のモデル
class DeliveryDaily(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    impressions: int
    clicks: int
    conversions: int

# 請求のモデル
class Invoice(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    campaign_id: str
    billing_month: str
    media_cost: float
    tax_rate: float
    agency_margin_rate: float
    amount: float
