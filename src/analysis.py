import pandas as pd
from src.metrics import predict_stock_out_days


def detect_dead_stock(df, days=60, lead_time_days=7):
    latest_date = df["Date"].max()
    results = []

    grouped = df.groupby(["Product_Name", "Warehouse"])

    for (product, warehouse), group in grouped:
        group = group.sort_values("Date")

        recent = group[group["Date"] >= latest_date - pd.Timedelta(days=days)]

        total_sales = recent["Units_Sold"].sum()
        avg_daily_sales = total_sales / days if days > 0 else 0

        opening_stock = recent.iloc[0]["Stock_Remaining"]
        closing_stock = recent.iloc[-1]["Stock_Remaining"]
        avg_inventory = (opening_stock + closing_stock) / 2

        turnover = total_sales / avg_inventory if avg_inventory > 0 else 0

        current_stock = group.iloc[-1]["Stock_Remaining"]
        category = group.iloc[-1]["Category"]
        cost_price = group.iloc[-1]["Cost_Price"]

        # Inventory status logic
        if turnover < 0.2 and current_stock > 0:
            status = "Dead Stock"
        elif turnover < 0.5:
            status = "Slow Moving"
        else:
            status = "Healthy"

        # Lead-time aware stock-out prediction
        days_to_stockout = predict_stock_out_days(
            current_stock,
            avg_daily_sales,
            lead_time_days
        )

        # ✅ ADD BACK BLOCKED VALUE
        blocked_value = current_stock * cost_price

        results.append({
            "Product": product,
            "Warehouse": warehouse,
            "Category": category,
            "Inventory_Turnover": round(turnover, 2),
            "Avg_Daily_Sales": round(avg_daily_sales, 2),
            "Current_Stock": int(current_stock),
            "Blocked_Value_₹": int(blocked_value),
            "Days_To_StockOut": days_to_stockout,
            "Status": status
        })

    return pd.DataFrame(results)
