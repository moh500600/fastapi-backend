from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import routes_categories
import routes_medicines
import schemas
from database import engine, get_db


# إنشاء جداول قاعدة البيانات إن لم تكن موجودة
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Pharma Offers API",
    version="1.0.0",
)


# إضافة مسارات الأقسام والأدوية
app.include_router(routes_categories.router)
app.include_router(routes_medicines.router)


# السماح لتطبيق Flutter وواجهة الويب بالاتصال بالباك إند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# مسار اختبار الباك إند
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Pharma Offers API is running",
    }


@app.post("/offers/", response_model=schemas.OfferResponse)
def create_offer(
    offer: schemas.OfferCreate,
    db: Session = Depends(get_db),
):
    db_offer = models.Offer(**offer.model_dump())

    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)

    return db_offer


@app.get("/offers/", response_model=List[schemas.OfferResponse])
def read_offers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Offer)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/offers/active", response_model=List[schemas.OfferResponse])
def get_active_offers(
    section: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Offer).filter(
        models.Offer.is_active.is_(True)
    )

    section_filters = {
        "main_slider": models.Offer.show_in_main_slider,
        "skincare": models.Offer.show_in_skincare,
        "products": models.Offer.show_in_products,
        "medical_devices": models.Offer.show_in_medical_devices,
        "medical_tools": models.Offer.show_in_medical_tools,
        "services": models.Offer.show_in_services,
        "health": models.Offer.show_in_health,
        "cart": models.Offer.show_in_cart,
        "categories": models.Offer.show_in_categories,
        "orders": models.Offer.show_in_orders,
    }

    if section in section_filters:
        query = query.filter(section_filters[section].is_(True))

    return query.order_by(models.Offer.order).all()


@app.delete("/offers/{offer_id}")
def delete_offer(
    offer_id: int,
    db: Session = Depends(get_db),
):
    db_offer = (
        db.query(models.Offer)
        .filter(models.Offer.id == offer_id)
        .first()
    )

    if not db_offer:
        raise HTTPException(
            status_code=404,
            detail="Offer not found",
        )

    db.delete(db_offer)
    db.commit()

    return {
        "ok": True,
        "message": "Offer deleted successfully",
    }
