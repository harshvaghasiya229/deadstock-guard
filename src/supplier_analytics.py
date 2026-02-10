import pandas as pd


def supplier_metrics(df):
    if "Restock_Units" not in df.columns or "Supplier" not in df.columns:
        return pd.DataFrame()

    po_df = df[df["Restock_Units"] > 0]

    if po_df.empty:
        return pd.DataFrame()

    return (
        po_df.groupby("Supplier")
        .agg(
            Total_Restock_Units=("Restock_Units", "sum"),
            Purchase_Orders=("Restock_Units", "count")
        )
        .reset_index()
    )
