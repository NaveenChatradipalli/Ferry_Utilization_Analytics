
# ⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics System

An end-to-end data analytics and interactive dashboard solution designed to evaluate operational efficiency, passenger activity load, and capacity utilization for the ferry services operating out of **Jack Layton Ferry Terminal** (Toronto Island Ferry Tickets dataset, 2015–2025).

---

## 📋 Project Overview
Ferries operating from Jack Layton Ferry Terminal to Centre Island, Hanlan’s Point, and Ward’s Island experience major demand fluctuations alongside fixed vessel capacity and staffing constraints. This project establishes a rigorous operational analytics framework to:
- Quantify ferry capacity utilization using historical ticket sales and redemption data.
- Identify high-congestion and under-utilized (idle) operating intervals.
- Support data-driven resource allocation, cost optimization, and seasonal schedule planning.

---

## 📊 Key Performance Indicators (KPIs) Tracked
* **Capacity Utilization Ratio:** Measures overall ferry load efficiency relative to maximum historical capacity.
* **Congestion Pressure Index:** Identifies over-utilized intervals exceeding high-load volume thresholds.
* **Idle Capacity Percentage:** Quantifies under-utilization during off-peak operating intervals.
* **Peak Strain Duration:** Tracks the length of sustained high-pressure congestion periods.
* **Operational Variability Score:** Assesses the stability of passenger utilization patterns using the Coefficient of Variation.

---

## 🛠️ Tech Stack & Libraries
* **Python** (Core data processing and analytics)
* **Pandas & NumPy** (Data ingestion, cleaning, temporal segmentation, and feature engineering)
* **Matplotlib** (Exploratory visual generation)
* **Streamlit** (Interactive web application framework for live stakeholder dashboards)

---

## 📂 Repository Structure
```text
📦 Ferry_Utilization_Analytics
├── app.py                            # Streamlit web application dashboard code
├── Ferry_Capacity_Utilization.ipynb  # Jupyter Notebook containing EDA and analytical methodology
├── Toronto Island Ferry Tickets.csv  # Historical ticket dataset (2015–2025)
├── requirements.txt                  # Python package dependencies
└── README.md                         # Project documentation
