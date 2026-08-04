from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/coupons",
    tags=["coupons"],
)

@router.post("/", response_model=schemas.CouponResponse)
def create_coupon(coupon: schemas.CouponCreate, db: Session = Depends(get_db)):
    db_item = models.Coupon(**coupon.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[schemas.CouponResponse])
def read_coupons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Coupon).offset(skip).limit(limit).all()
    return items

@router.get("/validate/{code}", response_model=schemas.CouponResponse)
def validate_coupon(code: str, db: Session = Depends(get_db)):
    coupon = db.query(models.Coupon).filter(models.Coupon.code == code).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="الكوبون غير صحيح")
    if coupon.status != 'active':
        raise HTTPException(status_code=400, detail="الكوبون غير فعال")
    if coupon.expiry_date and coupon.expiry_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="الكوبون منتهي الصلاحية")
    return coupon

@router.put("/{item_id}", response_model=schemas.CouponResponse)
def update_coupon(item_id: int, coupon: schemas.CouponCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Coupon).filter(models.Coupon.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    update_data = coupon.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_coupon(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Coupon).filter(models.Coupon.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Coupon not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
