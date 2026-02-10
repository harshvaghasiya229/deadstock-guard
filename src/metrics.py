def predict_stock_out(current_stock, avg_daily_sales):
    if avg_daily_sales == 0:
        return None
    return int(current_stock / avg_daily_sales)

def money_blocked(stock, cost_price):
    return stock * cost_price

def predict_stock_out_days(current_stock, avg_daily_sales):
    if avg_daily_sales <= 0:
        return None
    return int(current_stock / avg_daily_sales)

def predict_stock_out_days(current_stock, avg_daily_sales, lead_time_days=7):
    """
    Predict stock-out considering supplier lead time
    """
    if avg_daily_sales <= 0:
        return None

    days_left = current_stock / avg_daily_sales
    return int(days_left - lead_time_days)
