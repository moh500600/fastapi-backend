from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/bank-transfers",
    tags=["bank_transfers"],
)

# Ensure uploads directory exists
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "api", "assets", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=schemas.BankTransferResponse)
async def upload_bank_transfer(
    order_id: str = Form(...),
    customer_name: str = Form(...),
    amount: float = Form(...),
    receipt: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save the file
    file_ext = receipt.filename.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as f:
        content = await receipt.read()
        f.write(content)
        
    relative_url = f"assets/uploads/{file_name}"

    # Create DB entry
    db_item = models.BankTransfer(
        order_id=order_id,
        customer_name=customer_name,
        amount=amount,
        receipt_url=relative_url,
        status="pending"
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[schemas.BankTransferResponse])
def read_bank_transfers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.BankTransfer).offset(skip).limit(limit).all()
    return items

@router.put("/{item_id}/status", response_model=schemas.BankTransferResponse)
def update_bank_transfer_status(item_id: int, status: str, db: Session = Depends(get_db)):
    db_item = db.query(models.BankTransfer).filter(models.BankTransfer.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Bank Transfer not found")
    
    db_item.status = status
    db.commit()
    db.refresh(db_item)
    return db_item
