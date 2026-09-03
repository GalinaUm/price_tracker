from fastapi import FastAPI

from database import Base, engine
from routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Tracker")

app.include_router(products.router)

@app.get("/")
def home():
    return {"message": "Price tracker is running"}