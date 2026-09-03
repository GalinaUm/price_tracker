from datetime import datetime, timezone

from celery import Celery

from core.config import settings
from database import SessionLocal
from models import PriceHistory, Product


app = Celery(
    "price_tracker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

app.conf.timezone = "UTC"


@app.task
def check_price(product_id: int):
    print(f"Checking price for product {product_id}...")

    db = SessionLocal()
    try:
        product = db.get(Product, product_id)
        if not product:
            return {"error": "Product not found."}

        price = 99.99

        history = PriceHistory(
            product_id=product_id,
            price=price,
            checked_at=datetime.now(timezone.utc),
        )
        db.add(history)
        db.commit()
        db.refresh(history)

        return {"product_id": product.id, "price": price, "history_id": history.id}
    finally:
        db.close()
