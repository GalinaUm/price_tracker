from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal

router = APIRouter(prefix="/products", tags=["products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db:Session = Depends(get_db)):
    existing = db.query(models.Product).filter(
        models.Product.url == product.url
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")
    db_product = models.Product(name=product.name, url=product.url)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[schemas.ProductOut])
def list_products(db:Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db:Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product