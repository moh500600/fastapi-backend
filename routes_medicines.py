from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/medicines",
    tags=["medicines"],
)

@router.post("/", response_model=schemas.MedicineResponse)
def create_medicine(medicine: schemas.MedicineCreate, db: Session = Depends(get_db)):
    db_medicine = models.Medicine(**medicine.model_dump())
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

@router.get("/", response_model=List[schemas.MedicineResponse])
def get_all_medicines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicines = db.query(models.Medicine).offset(skip).limit(limit).all()
    return medicines

@router.get("/active", response_model=List[schemas.MedicineResponse])
def get_active_medicines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicines = db.query(models.Medicine).filter(models.Medicine.is_active == True).offset(skip).limit(limit).all()
    return medicines

@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    db_medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    db.delete(db_medicine)
    db.commit()
    return {"ok": True}
