from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    url: str


class ProductOut(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        from_attributes = True


class PriceAlertCreate(BaseModel):
    product_id: int
    email: str
    target_price: float


class PriceAlertOut(BaseModel):
    id: int
    product_id: int
    email: str
    target_price: float
    created_at: datetime

    class Config:
        from_attributes = True


class PriceHistoryOut(BaseModel):
    id: int
    product_id: int
    price: float
    checked_at: datetime

    class Config:
        from_attributes = True