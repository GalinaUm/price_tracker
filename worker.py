from celery import Celery


app = Celery(
    "price_tracker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

app.conf.timezone = "UTC"


@app.task
def check_price():
    return "price checked"