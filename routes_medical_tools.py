from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/medical-tools",
    tags=["medical_tools"],
)

@router.post("/", response_model=schemas.MedicalToolResponse)
def create_medical_tool(tool: schemas.MedicalToolCreate, db: Session = Depends(get_db)):
    db_item = models.MedicalTool(**tool.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[schemas.MedicalToolResponse])
def read_medical_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.MedicalTool).offset(skip).limit(limit).all()
    return items

@router.put("/{item_id}", response_model=schemas.MedicalToolResponse)
def update_medical_tool(item_id: int, tool: schemas.MedicalToolCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.MedicalTool).filter(models.MedicalTool.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    update_data = tool.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_medical_tool(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.MedicalTool).filter(models.MedicalTool.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Tool not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
