from fastapi import FastAPI

import models
from database import Base, engine

app = FastAPI(
    title="Price Tracker",
    description="Следим за ценами на товары",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Price tracker is running"}