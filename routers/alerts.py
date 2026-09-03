from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("/", response_model=schemas.PriceAlertOut)
def create_alert(alert: schemas.PriceAlertCreate, db: Session = Depends(get_db)):
    product = db.get(models.Product, alert.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(models.PriceAlert).filter(
        models.PriceAlert.product_id == alert.product_id,
        models.PriceAlert.email == alert.email,
    ).first()

    if existing:
        raise HTTPException(
            status_code=400, detail="Alert already exists for this product and email"
        )

    db_alert = models.PriceAlert(
        product_id=product.id,
        email=alert.email,
        target_price=alert.target_price,
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/", response_model=list[schemas.PriceAlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(models.PriceAlert).all()


@router.get("/{alert_id}", response_model=schemas.PriceAlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(models.PriceAlert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

