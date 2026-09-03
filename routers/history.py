from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/", response_model=list[schemas.PriceHistoryOut])
def list_history(
        product_id: int,
        db: Session = Depends(get_db),
):
    return (
        db.query(models.PriceHistory)
        .filter(models.PriceHistory.product_id == product_id)
        .order_by(models.PriceHistory.checked_at.desc())
        .all()
    )