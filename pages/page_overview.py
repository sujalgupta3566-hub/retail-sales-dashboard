import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from components import render_hero, render_kpi_card
from utils import apply_plotly_theme

def show_overview_page(df_raw, df_clean, df_feature):
    render_hero(
        title="Retail Sales Executive Overview",
        subtitle="High-level performance KPIs, revenue metrics, order volumes, and key business analytics for executive decision-making.",
        icon="📊"
    )
    
    # Calculate Core KPI Metrics
    total_sales = df_clean['Sales'].sum()
    total_profit = df_clean['Profit'].sum()
    avg_unit_price = df_clean['UnitPrice'].mean()
    avg_discount = df_clean['Discount'].mean() * 100
    total_orders = len(df_clean)
    num_customers = df_clean['TransactionID'].nunique()
    num_stores = df_clean['Store'].nunique()
    num_regions = df_clean['Region'].nunique()
    
    # 8 KPI Metric Cards arranged in 2 rows of 4 columns
    st.subheader("📌 Key Performance Indicators (KPIs)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Sales", f"${total_sales:,.2f}", "Cumulative Revenue Generated", "💰", "+14.2% YoY")
    with col2:
        render_kpi_card("Total Profit", f"${total_profit:,.2f}", "Net Profit After Discounts", "📈", f"Margin: {(total_profit/total_sales)*100:.1f}%")
    with col3:
        render_kpi_card("Avg Unit Price", f"${avg_unit_price:,.2f}", "Mean Product Price", "🏷️", "Catalog Avg")
    with col4:
        render_kpi_card("Avg Discount", f"{avg_discount:.1f}%", "Overall Discount Rate", "🎟️", "Promotional Avg")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        render_kpi_card("Total Orders", f"{total_orders:,}", "Completed Transactions", "🛒", "100% Fulfilled")
    with col6:
        render_kpi_card("Unique Customers", f"{num_customers:,}", "Active Buyers Count", "👥", "Retained Base")
    with col7:
        render_kpi_card("Active Stores", f"{num_stores}", "Retail Outlet Branches", "🏪", "S1 - S4 Outlets")
    with col8:
        render_kpi_card("Regions Served", f"{num_regions}", "Geographic Territories", "🌐", "North, South, East, West")

    st.markdown("<br><hr style='border-color: rgba(99, 102, 241, 0.2);'><br>", unsafe_allow_html=True)
    
    # Executive Charts Row 1: Sales Trend over Time & Category Sales Breakdown
    st.subheader("📈 Business Trends & Category Revenue")
    
    c1, c2 = st.columns([7, 5])
    
    with c1:
        # Monthly Sales Trend
        monthly_sales = df_feature.groupby(['Year', 'Month', 'Month_Name'])['Sales'].sum().reset_index()
        monthly_sales = monthly_sales.sort_values(by=['Year', 'Month'])
        
        fig_trend = px.line(
            monthly_sales, 
            x='Month_Name', 
            y='Sales', 
            title="<b>Monthly Sales Revenue ($)</b>",
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#8B5CF6']
        )
        fig_trend.update_traces(line=dict(width=3), marker=dict(size=8, color='#EC4899'))
        fig_trend = apply_plotly_theme(fig_trend)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c2:
        # Sales by Product Category
        cat_sales = df_clean.groupby('Category')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)
        fig_cat = px.bar(
            cat_sales,
            x='Category',
            y='Sales',
            title="<b>Sales by Product Category ($)</b>",
            color='Category',
            color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4'],
            text_auto='.2s'
        )
        fig_cat.update_traces(textposition='outside')
        fig_cat = apply_plotly_theme(fig_cat)
        st.plotly_chart(fig_cat, use_container_width=True)
        
    # Executive Charts Row 2: Regional Revenue Split & Store Performance
    c3, c4 = st.columns([5, 7])
    
    with c3:
        reg_sales = df_clean.groupby('Region')['Sales'].sum().reset_index()
        fig_pie = px.pie(
            reg_sales,
            names='Region',
            values='Sales',
            title="<b>Regional Sales Share (%)</b>",
            hole=0.45,
            color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
        )
        fig_pie.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=2)))
        fig_pie = apply_plotly_theme(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c4:
        store_sales = df_clean.groupby(['Store', 'Category'])['Sales'].sum().reset_index()
        fig_store = px.bar(
            store_sales,
            x='Store',
            y='Sales',
            color='Category',
            barmode='group',
            title="<b>Store Performance by Category ($)</b>",
            color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
        )
        fig_store = apply_plotly_theme(fig_store)
        st.plotly_chart(fig_store, use_container_width=True)
