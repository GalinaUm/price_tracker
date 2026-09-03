import httpx

COINGECKO_BASE = "https://api.coingecko.com/api/v3/simple/price"


def fetch_price(symbol: str) -> float:
    """Возвращает текущую цену монеты в USD."""
    resp = httpx.get(
        COINGECKO_BASE,
        params={"ids": symbol, "vs_currencies": "usd"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    price = data[symbol]["usd"]
    return float(price)