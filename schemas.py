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
    is_best_seller: Optional[bool] = False
    is_new_arrival: Optional[bool] = False

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SkincareBase(BaseModel):
    name_ar: str
    name_en: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: float
    cost_price: Optional[float] = None
    discount_price: Optional[float] = None
    tax: Optional[str] = None
    discount_start: Optional[datetime] = None
    discount_end: Optional[datetime] = None
    stock: Optional[int] = 0
    min_order: Optional[int] = 1
    is_new: Optional[bool] = True
    usage_instructions: Optional[str] = None
    warnings: Optional[str] = None
    shelf_life: Optional[str] = None
    seo_keyword: Optional[str] = None
    seo_description: Optional[str] = None
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    images: Optional[str] = None
    is_active: Optional[bool] = True

class SkincareCreate(SkincareBase):
    pass

class SkincareResponse(SkincareBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MedicalToolBase(BaseModel):
    name_ar: str
    name_en: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    price: float
    stock: Optional[int] = 0
    serial_number: Optional[str] = None
    status: Optional[str] = "active"
    purchase_date: Optional[datetime] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True

class MedicalToolCreate(MedicalToolBase):
    pass

class MedicalToolResponse(MedicalToolBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class MedicalDeviceBase(BaseModel):
    name_ar: str
    name_en: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    price: float
    stock: Optional[int] = 0
    serial_number: Optional[str] = None
    status: Optional[str] = "active"
    purchase_date: Optional[datetime] = None
    warranty_end: Optional[datetime] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True

class MedicalDeviceCreate(MedicalDeviceBase):
    pass

class MedicalDeviceResponse(MedicalDeviceBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class PaymentMethodBase(BaseModel):
    name_ar: str
    name_en: Optional[str] = None
    type: Optional[str] = None
    fee_percent: Optional[float] = 0.0
    fee_fixed: Optional[float] = 0.0
    status: Optional[str] = "active"
    logo_url: Optional[str] = None

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodResponse(PaymentMethodBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class CouponBase(BaseModel):
    code: str
    name: str
    discount_type: Optional[str] = None
    discount_value: Optional[float] = 0.0
    min_order: Optional[float] = 0.0
    expiry_date: Optional[datetime] = None
    usage_count: Optional[int] = 0
    status: Optional[str] = "active"

class CouponCreate(CouponBase):
    pass

class CouponResponse(CouponBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class BankTransferBase(BaseModel):
    order_id: str
    customer_name: str
    amount: float
    receipt_url: str
    status: Optional[str] = "pending"

class BankTransferCreate(BankTransferBase):
    pass

class BankTransferResponse(BankTransferBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_name: str
    qty: int
    price: float
    image: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: str

    class Config:
        orm_mode = True

class OrderStatusHistoryBase(BaseModel):
    status: str
    note: Optional[str] = None

class OrderStatusHistoryCreate(OrderStatusHistoryBase):
    order_id: str

class OrderStatusHistoryResponse(OrderStatusHistoryBase):
    id: int
    order_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    address: Optional[str] = None
    subtotal: float
    delivery_fee: float = 0.0
    tax: float
    total: float
    payment_method: str
    payment_mask: Optional[str] = None
    status: str = "جديد"
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    id: str
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        orm_mode = True
