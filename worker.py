from celery import Celery


app = Celery(
    "price_tracker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

app.conf.timezone = "UTC"


@app.task
def check_price(product_id: int):
    print(f"Checking price for product {product_id}...")
    return {"product_id": product_id, "price": 99.99}
