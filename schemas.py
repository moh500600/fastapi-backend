from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OfferBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    offer_type: str
    discount: Optional[int] = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    order: Optional[int] = 1
    button_text: Optional[str] = None

    show_in_main_slider: bool = True
    show_in_skincare: bool = False
    show_in_products: bool = False
    show_in_medical_devices: bool = False
    show_in_medical_tools: bool = False
    show_in_services: bool = False
    show_in_health: bool = False
    show_in_cart: bool = False
    show_in_categories: bool = False
    show_in_orders: bool = False
    is_active: bool = True

class OfferCreate(OfferBase):
    pass

class OfferResponse(OfferBase):
    id: int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = 'active'
    created: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MedicineBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    discount: Optional[float] = 0
    categories: Optional[str] = None
    company: Optional[str] = None
    image_url: Optional[str] = None
    composition: Optional[str] = None
    country: Optional[str] = None
    code: Optional[str] = None
    form_shape: Optional[str] = None
    strength: Optional[str] = None
    pack: Optional[str] = None
    storage: Optional[str] = None
    info_category: Optional[str] = None
    side_effects: Optional[str] = None
    dose: Optional[str] = None
    barcode: Optional[str] = None
    warnings: Optional[str] = None
    uses: Optional[str] = None
    faqs: Optional[str] = None
    is_active: Optional[bool] = True

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
