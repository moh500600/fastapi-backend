from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/skincare",
    tags=["skincare"],
)

@router.post("/", response_model=schemas.SkincareResponse)
def create_skincare_product(product: schemas.SkincareCreate, db: Session = Depends(get_db)):
    db_product = models.SkincareProduct(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[schemas.SkincareResponse])
def read_skincare_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.SkincareProduct).offset(skip).limit(limit).all()
    return products

@router.put("/{product_id}", response_model=schemas.SkincareResponse)
def update_skincare_product(product_id: int, product: schemas.SkincareCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.SkincareProduct).filter(models.SkincareProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
        
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_skincare_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.SkincareProduct).filter(models.SkincareProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"ok": True}
