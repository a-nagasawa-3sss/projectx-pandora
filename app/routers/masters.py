from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# マスタ関連のエンドポイントを定義するルーター
router = APIRouter(tags=["masters"])

# 広告主の一覧を取得するエンドポイント
@router.get("/advertisers", response_model=list[schemas.Advertiser])
def list_advertisers(db: Session = Depends(get_db)):
    return db.query(models.Advertiser).all()

# 広告主の詳細を取得するエンドポイント
@router.get("/advertisers/{advertiser_id}", response_model=schemas.Advertiser)
def get_advertiser(advertiser_id: str, db: Session = Depends(get_db)):
    advertiser = db.get(models.Advertiser, advertiser_id)
    if advertiser is None:
        raise HTTPException(status_code=404, detail="advertiser not found")
    return advertiser

# 広告代理店の一覧を取得するエンドポイント
@router.get("/agencies", response_model=list[schemas.Agency])
def list_agencies(db: Session = Depends(get_db)):
    return db.query(models.Agency).all()

# 広告代理店の詳細を取得するエンドポイント
@router.get("/agencies/{agency_id}", response_model=schemas.Agency)
def get_agency(agency_id: str, db: Session = Depends(get_db)):
    agency = db.get(models.Agency, agency_id)
    if agency is None:
        raise HTTPException(status_code=404, detail="agency not found")
    return agency

# 媒体社の一覧を取得するエンドポイント
@router.get("/publishers", response_model=list[schemas.Publisher])
def list_publishers(db: Session = Depends(get_db)):
    return db.query(models.Publisher).all()

# 媒体社の詳細を取得するエンドポイント
@router.get("/publishers/{publisher_id}", response_model=schemas.Publisher)
def get_publisher(publisher_id: str, db: Session = Depends(get_db)):
    publisher = db.get(models.Publisher, publisher_id)
    if publisher is None:
        raise HTTPException(status_code=404, detail="publisher not found")
    return publisher
