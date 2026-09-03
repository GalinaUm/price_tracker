from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)

    price_alerts = relationship("PriceAlert", back_populates="product")
    price_history = relationship("PriceHistory", back_populates="product")


class PriceAlert(Base):
    __tablename__ = "price_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    email = Column(String, nullable=False)
    target_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    product = relationship("Product", back_populates="price_alerts")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    product = relationship("Product", back_populates="price_history")
