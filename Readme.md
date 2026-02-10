📦 DeadStock Guard
Smart Inventory & Demand Forecasting for SMEs

DeadStock Guard is a data-driven supply chain analytics web application designed to help small and medium enterprises (SMEs) reduce losses caused by dead stock, overstocking, and poor demand planning.

The system ingests historical sales data (CSV/XLSX), validates and cleans it automatically, and transforms it into actionable inventory insights through an intuitive, non-technical dashboard.

🚀 Features

📊 Inventory Health Analysis

Dead Stock, Slow Moving, and Healthy item classification

Inventory turnover and blocked capital (₹) calculation

📈 Demand Forecasting

30-day time-series demand forecast

Forecast vs Current Stock visualization for stock-out prediction

🏭 Warehouse-wise Analytics

Multi-warehouse support

Warehouse-level forecasting and reporting

🚚 Supplier Performance Insights

Supplier-wise restocking volume and purchase order count

Visual charts for procurement decisions

🧪 Data Quality Intelligence

Automatic schema validation and column auto-mapping

Data quality score with drilldown report

📄 Automated Reporting

One-click PDF inventory reports

Warehouse-wise PDF generation

📥 Flexible Data Upload

Supports CSV and Excel files

Sample template download included

🛠 Tech Stack

Frontend / UI: Streamlit, Plotly

Data Processing: Pandas, NumPy

Forecasting: Statsmodels (Time-Series Analysis)

Reporting: ReportLab

Deployment: Streamlit Cloud

▶️ Run Locally
pip install -r requirements.txt
streamlit run main.py

🎯 Problem Statement

Manufacturing SMEs (Textile, Diamond, Brass, etc.) often over-order raw materials due to lack of forecasting tools, leading to idle inventory and blocked working capital.
DeadStock Guard bridges this gap by converting raw sales data into clear, business-ready inventory insights.

🧠 Architecture

The project follows a modular layered architecture with separate layers for:

Data ingestion & validation

Preprocessing

Analytics & forecasting

Visualization

Reporting

This makes the system scalable, maintainable, and production-ready.

📌 Use Cases

SME inventory optimization

Dead stock reduction

Demand planning and stock-out prevention

Academic final-year project

Analytics portfolio project

📜 License

This project is developed for academic and learning purposes.
You are free to explore, modify, and extend it.