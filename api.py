from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
import schemas

import routes_categories
import routes_medicines
import routes_skincare
import routes_medical_tools
import routes_medical_devices
import routes_payments
import routes_coupons
import routes_bank_transfers
import routes_orders
import routes_order_tracking

from database import engine, get_db


# إنشاء الجداول التي لا تزال غير موجودة في قاعدة البيانات
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Pharma Offers API",
    version="1.0.0",
)


# =========================================================
# مجلد الملفات المرفوعة
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "assets" / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/assets/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads",
)


# =========================================================
# إضافة Routers
# =========================================================

app.include_router(routes_categories.router)
app.include_router(routes_medicines.router)
app.include_router(routes_skincare.router)
app.include_router(routes_medical_tools.router)
app.include_router(routes_medical_devices.router)
app.include_router(routes_payments.router)
app.include_router(routes_coupons.router)
app.include_router(routes_bank_transfers.router)
app.include_router(routes_orders.router)
app.include_router(routes_order_tracking.router)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# اختبار تشغيل الباك إند
# =========================================================

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Pharma Offers API is running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


# =========================================================
# Offers
# =========================================================

@app.post(
    "/offers/",
    response_model=schemas.OfferResponse,
)
def create_offer(
    offer: schemas.OfferCreate,
    db: Session = Depends(get_db),
):
    db_offer = models.Offer(**offer.model_dump())

    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)

    return db_offer


@app.get(
    "/offers/",
    response_model=List[schemas.OfferResponse],
)
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


@app.get(
    "/offers/active",
    response_model=List[schemas.OfferResponse],
)
def get_active_offers(
    section: Optional[str] = None,
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

    selected_filter = section_filters.get(section)

    if selected_filter is not None:
        query = query.filter(selected_filter.is_(True))

    return query.order_by(models.Offer.order).all()


@app.put(
    "/offers/{offer_id}",
    response_model=schemas.OfferResponse,
)
def update_offer(
    offer_id: int,
    offer: schemas.OfferCreate,
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

    update_data = offer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_offer, key, value)

    db.commit()
    db.refresh(db_offer)

    return db_offer


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