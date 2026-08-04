from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
import datetime

router = APIRouter(prefix="/order_tracking", tags=["Order Tracking"])

@router.get("/{order_id}/history", response_model=List[schemas.OrderStatusHistoryResponse])
def get_order_history(order_id: str, db: Session = Depends(get_db)):
    # Check if order exists
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    history = db.query(models.OrderStatusHistory).filter(models.OrderStatusHistory.order_id == order_id).order_by(models.OrderStatusHistory.created_at.asc()).all()
    return history

@router.post("/{order_id}/status", response_model=schemas.OrderStatusHistoryResponse)
def update_order_status(order_id: str, status_update: schemas.OrderStatusHistoryBase, db: Session = Depends(get_db)):
    # Update main order status
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    order.status = status_update.status
    db.commit()
    
    # Add history entry
    db_history = models.OrderStatusHistory(
        order_id=order_id,
        status=status_update.status,
        note=status_update.note,
        created_at=datetime.datetime.utcnow()
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    
    return db_history
