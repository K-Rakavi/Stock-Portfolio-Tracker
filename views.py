# ✅ FINAL FIXED VIEWS.PY — Uses User-Selected Buy Date & Accurate Summaries

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Portfolio, Stock
from .forms import PortfolioForm
from .utils import log_action
from datetime import date, timedelta
from django.http import JsonResponse
from decimal import Decimal, getcontext
import yfinance as yf

getcontext().prec = 10  # Set precision for Decimal


def get_price_on_date(ticker, buy_date):
    try:
        start_date = buy_date - timedelta(days=1)
        end_date = buy_date + timedelta(days=1)
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
        if not hist.empty:
            close_price = hist['Close'].iloc[0]
            return round(Decimal(close_price), 2)
    except Exception as e:
        print(f"Error fetching historical price for {ticker} on {buy_date}: {e}")
    return Decimal('0.00')


def portfolio_view(request):
    holdings = Portfolio.objects.select_related('stock', 'user')
    enriched_data = []
    user_summaries = {}
    price_cache = {}

    for h in holdings:
        ticker = h.stock.ticker

        if ticker not in price_cache:
            from .utils import get_latest_price
            price_cache[ticker] = get_latest_price(ticker)

        today_price, yesterday_price, change, trend = price_cache[ticker]
        current_value = round(Decimal(today_price) * h.quantity, 2)
        investment = h.investment if h.investment is not None else Decimal('0.00')
        profit_loss = round(current_value - investment, 2)

        enriched_data.append({
            "user": h.user,
            "ticker": ticker,
            "quantity": h.quantity,
            "buy_date": h.buy_date,
            "buy_price": h.buy_price,
            "investment": investment,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "today_price": today_price,
            "yesterday_price": yesterday_price,
            "change": change,
            "trend": trend,
        })

        if h.user not in user_summaries:
            user_summaries[h.user] = {
                "total_investment": Decimal('0.00'),
                "total_current_value": Decimal('0.00'),
                "total_profit_loss": Decimal('0.00'),
            }

        user_summaries[h.user]["total_investment"] += investment
        user_summaries[h.user]["total_current_value"] += current_value
        user_summaries[h.user]["total_profit_loss"] = user_summaries[h.user]["total_current_value"] - user_summaries[h.user]["total_investment"]

    # Round final totals for display
    for summary in user_summaries.values():
        summary["total_investment"] = round(summary["total_investment"], 2)
        summary["total_current_value"] = round(summary["total_current_value"], 2)
        summary["total_profit_loss"] = round(summary["total_profit_loss"], 2)

    return render(request, "portfolio.html", {
        "portfolio_data": enriched_data,
        "user_summaries": user_summaries,
    })


def add_portfolio_entry(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            # Lock the buy price and investment ONLY if not already set
            if obj.buy_price is None:
                historical_price = get_price_on_date(obj.stock.ticker, obj.buy_date)
                if historical_price == Decimal('0.00'):
                    from django.contrib import messages
                    messages.error(request, "Failed to fetch price. Please try again later.")
                    return render(request, 'add_portfolio.html', {'form': form})
                obj.buy_price = Decimal(historical_price)
                obj.investment = round(obj.buy_price * obj.quantity, 2)

            obj.save()
            return redirect('/')
    else:
        form = PortfolioForm()
    return render(request, 'add_portfolio.html', {'form': form})


def stock_trend_view(request, ticker):
    from .utils import get_latest_price
    today_price, yesterday_price, change, trend = get_latest_price(ticker)

    return JsonResponse({
        "ticker": ticker,
        "trend": trend or "no data",
        "today_price": today_price or 0.0,
        "yesterday_price": yesterday_price or 0.0,
        "change": change or 0.0,
        "message": generate_trend_message(ticker, today_price, yesterday_price, change, trend)
    })

def generate_trend_message(ticker, today, yesterday, change, trend):
    message = f"{ticker} has "
    if trend == "up":
        message += "increased"
    elif trend == "down":
        message += "decreased"
    else:
        message += "shown no change."

    message += f"\n\nPrice Yesterday: ₹{yesterday:.2f}"
    message += f"\nPrice Today: ₹{today:.2f}"
    message += f"\nChange: ₹{change:.2f}"

    return message
