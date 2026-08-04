from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
import datetime

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Create the order
    db_order = models.Order(
        id=order.id,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        address=order.address,
        subtotal=order.subtotal,
        delivery_fee=order.delivery_fee,
        tax=order.tax,
        total=order.total,
        payment_method=order.payment_method,
        payment_mask=order.payment_mask,
        status=order.status,
        notes=order.notes,
        created_at=datetime.datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Create the order items
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_name=item.product_name,
            qty=item.qty,
            price=item.price,
            image=item.image
        )
        db.add(db_item)
    
    # Also add an initial status history entry
    db_history = models.OrderStatusHistory(
        order_id=db_order.id,
        status=db_order.status,
        note="تم إنشاء الطلب"
    )
    db.add(db_history)
    db.commit()

    return get_order_by_id(db_order.id, db)

@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
    for order in orders:
        items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all()
        order.items = items
    return orders

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order_by_id(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    order.items = items
    return order
