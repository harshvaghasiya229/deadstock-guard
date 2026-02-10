import streamlit as st
import plotly.express as px
import pandas as pd
import os

from src.loader import load_sales_data, data_quality_drilldown
from src.preprocessing import clean_data
from src.analysis import detect_dead_stock
from src.forecasting import forecast_next_30_days
from src.report import generate_pdf_report, generate_warehouse_pdfs
from src.supplier_analytics import supplier_metrics

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="DeadStock Guard",
    layout="wide",
    page_icon="📦"
)

st.title("📦 DeadStock Guard")
st.caption("Smart Inventory Forecasting for SMEs")

# --------------------------------------------------
# Sample File Download
# --------------------------------------------------
st.subheader("🧪 Download Sample Template")

sample_df = pd.DataFrame({
    "Date": ["2025-01-01"],
    "Product_Name": ["Cotton Shirt"],
    "Category": ["Textile"],
    "Warehouse": ["Ahmedabad_WH"],
    "Supplier": ["Supplier_A"],
    "Units_Sold": [5],
    "Stock_Remaining": [500],
    "Restock_Units": [0],
    "Cost_Price": [450]
})

st.download_button(
    label="⬇️ Download Sample File",
    data=sample_df.to_csv(index=False),
    file_name="deadstock_guard_sample.csv",
    mime="text/csv"
)

# --------------------------------------------------
# File Upload (CSV + XLSX)
# --------------------------------------------------
uploaded = st.file_uploader(
    "Upload sales file (CSV or Excel)",
    type=["csv", "xlsx"]
)

if uploaded:
    try:
        # Load + auto-map + save
        load_result = load_sales_data(uploaded)

        # Backward-compatible handling
        if isinstance(load_result, tuple):
            df, saved_path = load_result
            st.success(f"📁 File saved: `{saved_path}`")
        else:
            df = load_result

        df = clean_data(df)

        # --------------------------------------------------
        # Raw Data Preview
        # --------------------------------------------------
        st.subheader("📄 Raw Data Preview")
        st.dataframe(df.head(20), use_container_width=True)

        # --------------------------------------------------
        # 🧪 Data Quality Drilldown (ADD-ON)
        # --------------------------------------------------
        with st.expander("🧪 Data Quality Drilldown"):
            dq = data_quality_drilldown(df)
            st.json(dq)

        # --------------------------------------------------
        # Inventory Analysis (WAREHOUSE-AWARE)
        # --------------------------------------------------
        result = detect_dead_stock(df)

        dead_count = (result["Status"] == "Dead Stock").sum()
        slow_count = (result["Status"] == "Slow Moving").sum()
        healthy_count = (result["Status"] == "Healthy").sum()
        total_blocked = result[result["Status"] == "Dead Stock"]["Blocked_Value_₹"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🔴 Dead Stock Items", dead_count)
        col2.metric("🟡 Slow Moving Items", slow_count)
        col3.metric("🟢 Healthy Items", healthy_count)
        col4.metric("💰 Money Blocked", f"₹ {int(total_blocked):,}")

        # --------------------------------------------------
        # Forecast vs Stock (PRODUCT + WAREHOUSE FILTER)
        # --------------------------------------------------
        st.subheader("📈 Forecast vs Current Stock")

        col_f1, col_f2 = st.columns(2)

        with col_f1:
            selected_product = st.selectbox(
                "Select Product",
                sorted(df["Product_Name"].unique())
            )

        if "Warehouse" in df.columns and df["Warehouse"].notna().any():
            with col_f2:
                selected_warehouse = st.selectbox(
                    "Select Warehouse",
                    sorted(df["Warehouse"].dropna().unique())
                )

            filtered_df = df[
                (df["Product_Name"] == selected_product) &
                (df["Warehouse"] == selected_warehouse)
            ]

            stock_row = result[
                (result["Product"] == selected_product) &
                (result["Warehouse"] == selected_warehouse)
            ]
        else:
            filtered_df = df[df["Product_Name"] == selected_product]
            stock_row = result[result["Product"] == selected_product]

        forecast_df = forecast_next_30_days(filtered_df)

        if forecast_df is not None and not stock_row.empty:
            current_stock = stock_row["Current_Stock"].values[0]

            forecast_df["Cumulative_Demand"] = forecast_df["Forecasted_Units"].cumsum()
            forecast_df["Stock_Level"] = current_stock

            fig = px.line(
                forecast_df,
                x="Date",
                y=["Cumulative_Demand", "Stock_Level"],
                labels={"value": "Units", "variable": ""},
                title=f"Demand vs Stock – {selected_product}"
            )

            fig.update_traces(line=dict(width=3))
            fig.update_layout(
                height=350,
                legend=dict(orientation="h", y=-0.3),
                transition_duration=500
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Forecast not available for the selected product / warehouse.")

        # --------------------------------------------------
        # Inventory Table
        # --------------------------------------------------
        st.subheader("📊 Inventory Analysis Result")
        st.dataframe(result, use_container_width=True)

        # --------------------------------------------------
        # 🚚 Supplier Performance Charts (ADD-ON)
        # --------------------------------------------------
        st.subheader("🚚 Supplier Performance")

        sup_df = supplier_metrics(df)
        if not sup_df.empty:
            fig_sup = px.bar(
                sup_df,
                x="Supplier",
                y="Total_Restock_Units",
                title="Supplier-wise Restocked Units"
            )
            st.plotly_chart(fig_sup, use_container_width=True)
        else:
            st.info("No supplier restock data available.")

        # --------------------------------------------------
        # 📄 Single PDF Report (UNCHANGED)
        # --------------------------------------------------
        st.subheader("📄 Download Report")

        if st.button("Generate PDF Report"):
            pdf_path = "deadstock_guard_report.pdf"
            generate_pdf_report(result, pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=f,
                    file_name="deadstock_guard_report.pdf",
                    mime="application/pdf"
                )

            os.remove(pdf_path)

        # --------------------------------------------------
        # 🏭 Warehouse-wise PDF Reports (ADD-ON)
        # --------------------------------------------------
        st.subheader("🏭 Warehouse-wise PDF Reports")

        if st.button("Generate Warehouse-wise Reports"):
            pdfs = generate_warehouse_pdfs(result)

            if not pdfs:
                st.info("Warehouse data not available.")
            else:
                for pdf in pdfs:
                    with open(pdf, "rb") as f:
                        st.download_button(
                            f"⬇️ Download {pdf}",
                            f,
                            file_name=pdf,
                            mime="application/pdf"
                        )
                    os.remove(pdf)

    except ValueError as ve:
        st.error(f"❌ Data Validation Error: {ve}")
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")

else:
    st.info("📥 Upload a CSV or Excel file to begin analysis.")
