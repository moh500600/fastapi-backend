from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base
import datetime

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(500))
    image_url = Column(LONGTEXT)
    offer_type = Column(String(50))
    discount = Column(Integer, default=0)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)
    order = Column(Integer, default=1)
    button_text = Column(String(100), nullable=True)

    # التواجد في الأقسام (Switches)
    show_in_main_slider = Column(Boolean, default=True)
    show_in_skincare = Column(Boolean, default=False)
    show_in_products = Column(Boolean, default=False)
    show_in_medical_devices = Column(Boolean, default=False)
    show_in_medical_tools = Column(Boolean, default=False)
    show_in_services = Column(Boolean, default=False)
    show_in_health = Column(Boolean, default=False)
    show_in_cart = Column(Boolean, default=False)
    show_in_categories = Column(Boolean, default=False)
    show_in_orders = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(500))
    color = Column(String(50))
    image_url = Column(LONGTEXT)
    status = Column(String(50), default='active')
    created = Column(String(50)) # We'll store timestamp as string for simplicity like JS Date.now() or we could use DateTime. Let's use BigInteger for Date.now().
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    price = Column(Float)
    discount = Column(Float, default=0)
    categories = Column(String(255))
    company = Column(String(255))
    image_url = Column(LONGTEXT)
    composition = Column(Text)
    country = Column(String(100))
    code = Column(String(100))
    form_shape = Column(String(100))
    strength = Column(String(100))
    pack = Column(String(100))
    storage = Column(String(100))
    info_category = Column(String(255))
    side_effects = Column(Text)
    dose = Column(Text)
    barcode = Column(String(100))
    warnings = Column(Text)
    uses = Column(Text)
    faqs = Column(LONGTEXT)
    is_active = Column(Boolean, default=True)
    is_best_seller = Column(Boolean, default=False)
    is_new_arrival = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SkincareProduct(Base):
    __tablename__ = "skincare_products"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(255), index=True)
    name_en = Column(String(255))
    brand = Column(String(100))
    category = Column(String(100))
    price = Column(Float)
    cost_price = Column(Float, nullable=True)
    discount_price = Column(Float, nullable=True)
    tax = Column(String(50), nullable=True)
    discount_start = Column(DateTime, nullable=True)
    discount_end = Column(DateTime, nullable=True)
    stock = Column(Integer, default=0)
    min_order = Column(Integer, default=1)
    is_new = Column(Boolean, default=True)
    usage_instructions = Column(Text, nullable=True)
    warnings = Column(Text, nullable=True)
    shelf_life = Column(String(100), nullable=True)
    seo_keyword = Column(String(255), nullable=True)
    seo_description = Column(Text, nullable=True)
    product_url = Column(String(500), nullable=True)
    image_url = Column(LONGTEXT, nullable=True) # First image
    images = Column(LONGTEXT, nullable=True) # JSON array of additional images
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MedicalTool(Base):
    __tablename__ = "medical_tools"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(255), index=True)
    name_en = Column(String(255))
    category = Column(String(100))
    department = Column(String(100))
    brand = Column(String(100))
    manufacturer = Column(String(100))
    price = Column(Float)
    stock = Column(Integer, default=0)
    serial_number = Column(String(100))
    status = Column(String(50), default="active")
    purchase_date = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(LONGTEXT, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MedicalDevice(Base):
    __tablename__ = "medical_devices"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(255), index=True)
    name_en = Column(String(255))
    category = Column(String(100))
    department = Column(String(100))
    brand = Column(String(100))
    manufacturer = Column(String(100))
    price = Column(Float)
    stock = Column(Integer, default=0)
    serial_number = Column(String(100))
    status = Column(String(50), default="active")
    purchase_date = Column(DateTime, nullable=True)
    warranty_end = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(LONGTEXT, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(255), index=True)
    name_en = Column(String(255))
    type = Column(String(100))
    fee_percent = Column(Float, default=0.0)
    fee_fixed = Column(Float, default=0.0)
    status = Column(String(50), default="active")
    logo_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True)
    name = Column(String(255))
    discount_type = Column(String(50))
    discount_value = Column(Float)
    min_order = Column(Float, default=0.0)
    expiry_date = Column(DateTime)
    usage_count = Column(Integer, default=0)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class BankTransfer(Base):
    __tablename__ = "bank_transfers"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(100), index=True)
    customer_name = Column(String(255))
    amount = Column(Float)
    receipt_url = Column(String(255))
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(100), primary_key=True, index=True)
    customer_name = Column(String(255))
    customer_phone = Column(String(100))
    address = Column(String(500))
    subtotal = Column(Float)
    delivery_fee = Column(Float, default=0.0)
    tax = Column(Float)
    total = Column(Float)
    payment_method = Column(String(100))
    payment_mask = Column(String(100), nullable=True)
    status = Column(String(50), default="جديد")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(100), index=True)
    product_name = Column(String(255))
    qty = Column(Integer)
    price = Column(Float)
    image = Column(String(500), nullable=True)

class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(100), index=True)
    status = Column(String(50))
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


