# ================================================================
# FERRY CAPACITY UTILIZATION & OPERATIONAL EFFICIENCY DASHBOARD
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(
    page_title="Ferry Capacity Utilization & Operational Efficiency Analytics",
    page_icon="⛴️",
    layout="wide"
)

# 2. Load and Cache Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Toronto Island Ferry Tickets.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values('Timestamp').reset_index(drop=True)
    
    # Clean anomalies
    df['Sales Count'] = df['Sales Count'].clip(lower=0)
    df['Redemption Count'] = df['Redemption Count'].clip(lower=0)
    
    # Feature Engineering
    df['Total Activity Load'] = df['Sales Count'] + df['Redemption Count']
    
    max_load = df['Total Activity Load'].max()
    df['Operational Load Index'] = df['Total Activity Load'] / (max_load if max_load > 0 else 1)
    
    idle_threshold = df['Total Activity Load'].quantile(0.25)
    df['Idle Capacity Indicator'] = (df['Total Activity Load'] <= idle_threshold).astype(int)
    
    congestion_threshold = df['Total Activity Load'].quantile(0.90)
    df['Is_Congested'] = (df['Total Activity Load'] >= congestion_threshold).astype(int)
    
    # Temporal Extractions
    df['Year'] = df['Timestamp'].dt.year
    df['Month'] = df['Timestamp'].dt.month
    df['Hour'] = df['Timestamp'].dt.hour
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()
    
    def get_season(month):
        if month in [6, 7, 8]:
            return 'Summer (Peak)'
        elif month in [12, 1, 2]:
            return 'Winter (Off-Season)'
        else:
            return 'Spring / Autumn'
            
    df['Season'] = df['Month'].apply(get_season)
    return df

df = load_data()

# --- SIDEBAR USER CAPABILITIES & FILTERS ---
st.sidebar.header("🎛️ Dashboard Controls & Filters")

# Date Filter (Year range selector)
years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("Select Years", years, default=years[-3:] if len(years)>=3 else years)

# Season Filter
seasons = df['Season'].unique()
selected_seasons = st.sidebar.multiselect("Select Seasons", seasons, default=seasons)

# Granularity Toggle
granularity = st.sidebar.selectbox(
    "Select Temporal Granularity", 
    ["15-Minute Interval", "Hourly", "Daily"]
)

# Filter dataframe
filtered_df = df[df['Year'].isin(selected_years) & df['Season'].isin(selected_seasons)]

# --- MAIN DASHBOARD HEADER ---
st.title("⛴️ Ferry Operations & Capacity Utilization Dashboard")
st.markdown("### Jack Layton Ferry Terminal Analytics Portal (2015–2025)")
st.markdown("---")

if filtered_df.empty:
    st.warning("⚠️ No records match your filter selections. Please expand your year or season filters.")
else:
    # --- MODULE 4: KPI SUMMARY CARDS ---
    st.subheader("📊 Key Performance Indicator (KPI) Summary Cards")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = filtered_df['Sales Count'].sum()
    total_redemptions = filtered_df['Redemption Count'].sum()
    capacity_util_ratio = filtered_df['Operational Load Index'].mean() * 100
    congestion_index = filtered_df['Is_Congested'].mean() * 100
    idle_pct = filtered_df['Idle Capacity Indicator'].mean() * 100
    
    col1.metric("Total Passenger Activity", f"{(total_sales + total_redemptions):,}")
    col2.metric("Capacity Utilization Ratio", f"{capacity_util_ratio:.2f}%")
    col3.metric("Congestion Pressure Index", f"{congestion_index:.2f}%")
    col4.metric("Idle Capacity Percentage", f"{idle_pct:.1f}%")
    
    st.markdown("---")

    # --- MODULE 1: CAPACITY UTILIZATION TIMELINE ---
    st.subheader("📈 Capacity Utilization Timeline")
    st.markdown("Tracking total passenger activity load across selected time frames.")
    
    # Resample based on granularity toggle
    if granularity == "Hourly":
        timeline_data = filtered_df.set_index('Timestamp').resample('h')['Total Activity Load'].sum().reset_index()
    elif granularity == "Daily":
        timeline_data = filtered_df.set_index('Timestamp').resample('D')['Total Activity Load'].mean().reset_index()
    else:
        timeline_data = filtered_df[['Timestamp', 'Total Activity Load']]
        
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(timeline_data['Timestamp'], timeline_data['Total Activity Load'], color='#1f77b4', linewidth=1)
    ax.set_title(f"Activity Load Timeline ({granularity} Resolution)", fontsize=11, fontweight='bold')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Total Activity Load (Sales + Redemptions)")
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # --- MODULE 2 & 3: HEATMAPS & SEASONAL EFFICIENCY ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🔥 Hourly Congestion Patterns")
        st.markdown("Average passenger pressure across hours of the day.")
        hourly_congestion = filtered_df.groupby('Hour')['Total Activity Load'].mean().reset_index()
        
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.bar(hourly_congestion['Hour'], hourly_congestion['Total Activity Load'], color='#ff7f0e')
        ax2.set_title("Mean Activity Load by Hour", fontsize=10, fontweight='bold')
        ax2.set_xlabel("Hour of Day (0-23)")
        ax2.set_ylabel("Average Load")
        ax2.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig2)

    with col_right:
        st.subheader("☀️ Seasonal Efficiency Comparison")
        st.markdown("Comparative utilization across operating seasons.")
        seasonal_eff = filtered_df.groupby('Season')['Total Activity Load'].mean().reset_index()
        
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.bar(seasonal_eff['Season'], seasonal_eff['Total Activity Load'], color='#2ca02c')
        ax3.set_title("Mean Activity Load by Season", fontsize=10, fontweight='bold')
        ax3.set_xlabel("Season")
        ax3.set_ylabel("Average Load")
        plt.xticks(rotation=10)
        ax3.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig3)

    # --- THRESHOLD-BASED EFFICIENCY ALERTS (VISUAL) ---
    st.markdown("---")
    st.subheader("🚨 Threshold-Based Operational Efficiency Alerts")
    
    congested_count = filtered_df['Is_Congested'].sum()
    idle_count = filtered_df['Idle Capacity Indicator'].sum()
    
    alert_col1, alert_col2 = st.columns(2)
    with alert_col1:
        if congested_count > 0:
            st.error(f"**High Congestion Alert:** Detected **{congested_count:,}** intervals exceeding high-load threshold (>90th percentile). Recommended action: Increase vessel deployment and manage terminal queues.")
        else:
            st.success("**Congestion Status:** Normal operations. No extreme congestion thresholds breached in current filter selection.")
            
    with alert_col2:
        if idle_count > 0:
            st.info(f"**Under-Utilization Notice:** Detected **{idle_count:,}** idle capacity intervals (bottom quartile). Recommended action: Optimize crew rotations and reduce off-peak trip frequency.")
        else:
            st.success("**Idle Capacity Status:** Healthy activity levels across all selected intervals.")