from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from routers import alerts, history, products
from worker import check_price

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Tracker")

app.include_router(alerts.router)
app.include_router(history.router)
app.include_router(products.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return {"message": "Price tracker is running"}


@app.post("/check/{product_id}")
def trigger_check(product_id: int):
    task = check_price.delay(product_id)
    return {"task_id": task.id, "status": "queued"}