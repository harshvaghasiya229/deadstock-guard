# 📦 DeadStock Guard – Smart Inventory Forecasting for SMEs

![GitHub release](https://img.shields.io/github/v/release/harshvaghasiya229/deadstock-guard)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live-brightgreen)](https://deadstock-guard-assistant.streamlit.app/)

DeadStock Guard is a data-driven inventory analytics platform designed for small and medium enterprises (SMEs).
It helps businesses detect dead stock, forecast demand, predict stock-outs, and analyze inventory at a
warehouse and supplier level using time-series analysis.

## 🚀 Live Demo

## 👉 https://deadstock-guard-assistant.streamlit.app/

    Upload a CSV or Excel file to:
    - Detect dead stock
    - Forecast demand
    - View warehouse-level insights
    - Download PDF reports

## 🚀 Features

## 📊 Inventory Health Analysis

    Dead Stock, Slow Moving, and Healthy item classification
    Inventory turnover and blocked capital (₹) calculation

## 📈 Demand Forecasting

    30-day time-series demand forecast
    Forecast vs Current Stock visualization for stock-out prediction

## 🏭 Warehouse-wise Analytics

    Multi-warehouse support
    Warehouse-level forecasting and reporting

## 🚚 Supplier Performance Insights

    Supplier-wise restocking volume and purchase order count
    Visual charts for procurement decisions

## 🧪 Data Quality Intelligence

    Automatic schema validation and column auto-mapping
    Data quality score with drilldown report

## 📄 Automated Reporting

    One-click PDF inventory reports
    Warehouse-wise PDF generation

## 📥 Flexible Data Upload

    Supports CSV and Excel files
    Sample template download included

## 🛠 Tech Stack

    Frontend / UI: Streamlit, Plotly
    Data Processing: Pandas, NumPy
    Forecasting: Statsmodels (Time-Series Analysis)
    Reporting: ReportLab
    Deployment: Streamlit Cloud

## ▶️ Run Locally
    pip install -r requirements.txt
    streamlit run main.py

## 🎯 Problem Statement

    Manufacturing SMEs (Textile, Diamond, Brass, etc.) often over-order raw materials due to lack of forecasting tools, leading to idle inventory and blocked working capital.
    DeadStock Guard bridges this gap by converting raw sales data into clear, business-ready inventory insights.

## 🧠 Architecture

    The project follows a modular layered architecture with separate layers for:
    Data ingestion & validation
    Preprocessing
    Analytics & forecasting
    Visualization
    Reporting
    This makes the system scalable, maintainable, and production-ready.

## 📌 Use Cases

    SME inventory optimization
    Dead stock reduction
    Demand planning and stock-out prevention
    Academic final-year project
    Analytics portfolio project

## 🏷 Versioning

    Current stable release: **v1.0**
    Git tags are used to mark stable production-ready versions.

## 📜 License

    This project is developed for academic and learning purposes.
    You are free to explore, modify, and extend it.