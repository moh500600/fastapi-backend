from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)

@router.post("/", response_model=schemas.PaymentMethodResponse)
def create_payment_method(payment: schemas.PaymentMethodCreate, db: Session = Depends(get_db)):
    db_item = models.PaymentMethod(**payment.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[schemas.PaymentMethodResponse])
def read_payment_methods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.PaymentMethod).offset(skip).limit(limit).all()
    return items

@router.put("/{item_id}", response_model=schemas.PaymentMethodResponse)
def update_payment_method(item_id: int, payment: schemas.PaymentMethodCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.PaymentMethod).filter(models.PaymentMethod.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    
    update_data = payment.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_payment_method(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.PaymentMethod).filter(models.PaymentMethod.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
