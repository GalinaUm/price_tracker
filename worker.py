from datetime import datetime, timezone

from celery import Celery
from celery.schedules import crontab

from core.config import settings
from database import SessionLocal
from models import PriceHistory, Product, PriceAlert
from price_service import fetch_price


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

        try:
            price = fetch_price(product.url)
        except Exception as e:
            return {"error": f"Could not fetch price for product {product_id}: {e}"}

        history = PriceHistory(
            product_id=product_id,
            price=price,
            checked_at=datetime.now(timezone.utc),
        )
        db.add(history)
        db.commit()
        db.refresh(history)

        alerts = db.query(PriceAlert).filter(
            PriceAlert.product_id == product.id
        ).all()

        triggered = []

        for alert in alerts:
            if price <= alert.target_price:
                triggered.append(alert.email)
                print(f"    ALERT: price {price} <= target {alert.target_price} for {alert.email}")

        return {
            "product_id": product.id,
            "price": price,
            "history_id": history.id,
            "triggered": triggered
        }
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