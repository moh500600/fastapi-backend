from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/medical-devices",
    tags=["medical_devices"],
)

@router.post("/", response_model=schemas.MedicalDeviceResponse)
def create_medical_device(device: schemas.MedicalDeviceCreate, db: Session = Depends(get_db)):
    db_item = models.MedicalDevice(**device.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[schemas.MedicalDeviceResponse])
def read_medical_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.MedicalDevice).offset(skip).limit(limit).all()
    return items

@router.put("/{item_id}", response_model=schemas.MedicalDeviceResponse)
def update_medical_device(item_id: int, device: schemas.MedicalDeviceCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.MedicalDevice).filter(models.MedicalDevice.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Device not found")
    
    update_data = device.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_medical_device(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.MedicalDevice).filter(models.MedicalDevice.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
