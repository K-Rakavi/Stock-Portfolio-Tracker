import pymongo
from django.utils.timezone import now
from django.core.cache import cache
import yfinance as yf

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['stocktracker']
log_col = db['logs']

def log_action(user_id, action):
    log_col.insert_one({
        "user_id": user_id,
        "action": action,
        "timestamp": now()
    })
def get_latest_price(ticker):
    cache_key = f"price_{ticker}"
    cached = cache.get(cache_key)

    if cached:
        return cached  # Use cached version if available

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="2d")

        if len(data) < 2:
            result = (0.0, 0.0, 0.0, "no data")
        else:
            close_yesterday = data['Close'].iloc[-2]
            close_today = data['Close'].iloc[-1]
            change = round(close_today - close_yesterday, 2)
            trend = "up" if change > 0 else "down" if change < 0 else "no change"
            result = (round(close_today, 2), round(close_yesterday, 2), change, trend)

        # Cache the result for 15 minutes (900 seconds)
        cache.set(cache_key, result, timeout=900)
        return result

    except Exception as e:
        print("Error fetching price:", e)
        return (0.0, 0.0, 0.0, "error")






