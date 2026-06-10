from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# キャンペーン関連のエンドポイントを定義するルーター
router = APIRouter(prefix="/campaigns", tags=["campaigns"])

# キャンペーンの一覧を取得するエンドポイント
@router.get("", response_model=list[schemas.Campaign])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).all()

# キャンペーンの詳細を取得するエンドポイント
@router.get("/{campaign_id}", response_model=schemas.Campaign)
def get_campaign(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.get(models.Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="campaign not found")
    return campaign
