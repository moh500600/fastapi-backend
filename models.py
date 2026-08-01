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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
