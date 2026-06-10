from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# 配信実績関連のエンドポイントを定義するルーター
router = APIRouter(prefix="/campaigns", tags=["delivery"])

# キャンペーンの配信実績を取得するエンドポイント
@router.get("/{campaign_id}/delivery", response_model=list[schemas.DeliveryDaily])
def get_delivery(
    campaign_id: str,
    date_from: date | None = Query(default=None, alias="from"),
    date_to: date | None = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
):
    # キャンペーンが存在するか確認
    campaign = db.get(models.Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="campaign not found")
    # 配信実績をクエリ
    query = db.query(models.DeliveryDaily).filter(models.DeliveryDaily.campaign_id == campaign_id)
    if date_from is not None:
        query = query.filter(models.DeliveryDaily.date >= date_from)
    if date_to is not None:
        query = query.filter(models.DeliveryDaily.date <= date_to)
    # 日付順で返す
    return query.order_by(models.DeliveryDaily.date).all()
