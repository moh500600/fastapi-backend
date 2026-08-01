from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

import routes_categories
import routes_medicines

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pharma Offers API")

app.include_router(routes_categories.router)
app.include_router(routes_medicines.router)

# السماح للاتصالات من تطبيق فلاتر و واجهة الويب
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
api_dir = os.path.join(os.path.dirname(__file__), '..', 'api')
app.mount("/dashboard", StaticFiles(directory=api_dir), name="dashboard")

@app.post("/offers/", response_model=schemas.OfferResponse)
def create_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    db_offer = models.Offer(**offer.model_dump())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

@app.get("/offers/", response_model=List[schemas.OfferResponse])
def read_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    offers = db.query(models.Offer).offset(skip).limit(limit).all()
    return offers

@app.get("/offers/active", response_model=List[schemas.OfferResponse])
def get_active_offers(section: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Offer).filter(models.Offer.is_active == True)
    
    if section == "main_slider":
        query = query.filter(models.Offer.show_in_main_slider == True)
    elif section == "skincare":
        query = query.filter(models.Offer.show_in_skincare == True)
    elif section == "products":
        query = query.filter(models.Offer.show_in_products == True)
    elif section == "medical_devices":
        query = query.filter(models.Offer.show_in_medical_devices == True)
    elif section == "medical_tools":
        query = query.filter(models.Offer.show_in_medical_tools == True)
    elif section == "services":
        query = query.filter(models.Offer.show_in_services == True)
    elif section == "health":
        query = query.filter(models.Offer.show_in_health == True)
    elif section == "cart":
        query = query.filter(models.Offer.show_in_cart == True)
    elif section == "categories":
        query = query.filter(models.Offer.show_in_categories == True)
    elif section == "orders":
        query = query.filter(models.Offer.show_in_orders == True)

    return query.order_by(models.Offer.order).all()

@app.delete("/offers/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    db_offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not db_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    db.delete(db_offer)
    db.commit()
    return {"ok": True}
    db.commit()
    return {"ok": True}
