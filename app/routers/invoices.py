from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# 請求関連のエンドポイントを定義するルーター
router = APIRouter(tags=["invoices"])

# キャンペーンに紐づく請求の一覧を取得するエンドポイント
@router.get("/campaigns/{campaign_id}/invoices", response_model=list[schemas.Invoice])
def list_campaign_invoices(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.get(models.Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="campaign not found")
    return db.query(models.Invoice).filter(models.Invoice.campaign_id == campaign_id).all()

# 請求の詳細を取得するエンドポイント
@router.get("/invoices/{invoice_id}", response_model=schemas.Invoice)
def get_invoice(invoice_id: str, db: Session = Depends(get_db)):
    invoice = db.get(models.Invoice, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="invoice not found")
    return invoice
