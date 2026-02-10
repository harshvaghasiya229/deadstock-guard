def clean_data(df):
    df = df.dropna(subset=["Date", "Product_Name"])
    df["Units_Sold"] = df["Units_Sold"].fillna(0)
    df["Blocked_Value"] = df["Stock_Remaining"] * df["Cost_Price"]
    df["Stock_Remaining"] = df["Stock_Remaining"].fillna(method="ffill")
    return df
