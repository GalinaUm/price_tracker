from datetime import datetime, timezone

from celery import Celery
from celery.schedules import crontab

from core.config import settings
from database import SessionLocal
from models import PriceHistory, Product


app = Celery(
    "price_tracker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

app.conf.timezone = "UTC"

app.conf.beat_schedule = {
    "check_prices_every_minute": {
        "task": "worker.check_all_prices",
        "schedule": crontab(minute="*/1"),
    }
}


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


@app.task
def check_all_prices():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        for product in products:
            check_price.delay(product.id)
        return {"scheduled": len(products)}
    finally:
        db.close()