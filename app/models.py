from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

# マスタとトランザクションのモデルを定義
class Advertiser(Base):
    __tablename__ = "advertisers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    campaigns: Mapped[list["Campaign"]] = relationship(back_populates="advertiser")

# 広告代理店のモデル
class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    margin_rate: Mapped[float] = mapped_column(Float, nullable=False)

    campaigns: Mapped[list["Campaign"]] = relationship(back_populates="agency")

# 媒体社のモデル
class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    campaigns: Mapped[list["Campaign"]] = relationship(back_populates="publisher")

# キャンペーンのモデル
class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    advertiser_id: Mapped[str] = mapped_column(ForeignKey("advertisers.id"), nullable=False)
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"), nullable=False)
    publisher_id: Mapped[str] = mapped_column(ForeignKey("publishers.id"), nullable=False)
    billing_type: Mapped[str] = mapped_column(String, nullable=False)  # "CPM" or "CPC"
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    advertiser: Mapped["Advertiser"] = relationship(back_populates="campaigns")
    agency: Mapped["Agency"] = relationship(back_populates="campaigns")
    publisher: Mapped["Publisher"] = relationship(back_populates="campaigns")
    deliveries: Mapped[list["DeliveryDaily"]] = relationship(back_populates="campaign")
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="campaign")

# キャンペーンの日次配信実績のモデル
class DeliveryDaily(Base):
    __tablename__ = "delivery_daily"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    campaign_id: Mapped[str] = mapped_column(ForeignKey("campaigns.id"), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    impressions: Mapped[int] = mapped_column(Integer, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, nullable=False)
    conversions: Mapped[int] = mapped_column(Integer, nullable=False)

    campaign: Mapped["Campaign"] = relationship(back_populates="deliveries")

# 請求のモデル
class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(ForeignKey("campaigns.id"), nullable=False)
    billing_month: Mapped[str] = mapped_column(String, nullable=False)  # "YYYY-MM"
    media_cost: Mapped[float] = mapped_column(Float, nullable=False)
    tax_rate: Mapped[float] = mapped_column(Float, nullable=False)
    agency_margin_rate: Mapped[float] = mapped_column(Float, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)

    campaign: Mapped["Campaign"] = relationship(back_populates="invoices")
