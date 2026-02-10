import pandas as pd
import os
from datetime import datetime

# Canonical schema
REQUIRED_COLUMNS = {
    "Date",
    "Product_Name",
    "Category",
    "Units_Sold",
    "Stock_Remaining",
    "Cost_Price"
}

OPTIONAL_COLUMNS = {
    "Warehouse",
    "Supplier",
    "Restock_Units"
}

# Column auto-mapping
COLUMN_ALIASES = {
    "date": "Date",
    "product": "Product_Name",
    "item": "Product_Name",
    "product_name": "Product_Name",
    "category": "Category",
    "sales": "Units_Sold",
    "qty": "Units_Sold",
    "quantity": "Units_Sold",
    "units": "Units_Sold",
    "stock": "Stock_Remaining",
    "balance_stock": "Stock_Remaining",
    "remaining": "Stock_Remaining",
    "cost": "Cost_Price",
    "price": "Cost_Price",
    "cost_price": "Cost_Price",
    "warehouse": "Warehouse",
    "supplier": "Supplier",
    "restock": "Restock_Units"
}


def _standardize_columns(df):
    renamed = {}
    for col in df.columns:
        key = col.strip().lower().replace(" ", "_")
        if key in COLUMN_ALIASES:
            renamed[col] = COLUMN_ALIASES[key]
    return df.rename(columns=renamed)


def load_sales_data(file):
    """
    Load CSV/XLSX, auto-map columns, validate schema,
    and save uploaded file locally.
    """

    # -------------------------------------------
    # Load file
    # -------------------------------------------
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # -------------------------------------------
    # Auto-map column names
    # -------------------------------------------
    df.columns = df.columns.str.strip()
    df = _standardize_columns(df)

    # -------------------------------------------
    # Validate required columns
    # -------------------------------------------
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns after auto-mapping: {', '.join(missing)}"
        )

    # -------------------------------------------
    # Type normalization
    # -------------------------------------------
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if df["Date"].isna().any():
        raise ValueError("Invalid values found in Date column")

    # -------------------------------------------
    # Add optional columns if missing
    # -------------------------------------------
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = None

    # -------------------------------------------
    # Save uploaded file (cloud-ready)
    # -------------------------------------------
    os.makedirs("data/uploads", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = f"data/uploads/{timestamp}_{file.name}"

    if file.name.endswith(".csv"):
        df.to_csv(save_path, index=False)
    else:
        df.to_excel(save_path, index=False)

    return df, save_path

def data_quality_drilldown(df):
    return {
        "Missing values per column": df.isna().sum().to_dict(),
        "Negative Units_Sold": int((df["Units_Sold"] < 0).sum()),
        "Negative Stock_Remaining": int((df["Stock_Remaining"] < 0).sum()),
        "Zero-sales ratio": round((df["Units_Sold"] == 0).mean(), 2)
    }
