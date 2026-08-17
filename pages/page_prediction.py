import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from components import render_hero, render_kpi_card
from utils import predict_single_instance, apply_plotly_theme

def show_prediction_page(artifacts):
    render_hero(
        title="Real-Time Retail Sales Prediction Engine",
        subtitle="Configure transaction parameters to estimate projected sales revenue, net profit margin, and feature impact using the trained machine learning model.",
        icon="🔮"
    )
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🎛️ Transaction Input Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        quantity = st.slider("Quantity Purchased", min_value=1, max_value=10, value=4, step=1, help="Number of items purchased in transaction")
        unit_price = st.number_input("Unit Price ($)", min_value=5.0, max_value=500.0, value=145.0, step=5.0, help="Individual item retail price")
        discount = st.select_slider("Promotional Discount Rate", options=[0.0, 0.05, 0.10, 0.15, 0.20], value=0.10, format_func=lambda x: f"{int(x*100)}%", help="Discount percentage applied")
        
    with col2:
        category = st.selectbox("Product Category", options=['Electronics', 'Clothing', 'Home', 'Grocery'], index=0)
        store = st.selectbox("Store Branch Outlet", options=['S1', 'S2', 'S3', 'S4'], index=0)
        region = st.selectbox("Geographic Region", options=['East', 'West', 'North', 'South'], index=0)
        
    with col3:
        payment = st.selectbox("Payment Method", options=['Card', 'UPI', 'Cash'], index=0)
        loyalty = st.selectbox("Loyalty Program Member", options=['Yes', 'No'], index=0)
        customer_age = st.slider("Customer Age", min_value=18, max_value=70, value=35, step=1)
        gender = st.radio("Gender", options=['M', 'F'], horizontal=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    predict_btn = st.button("🔮 Predict Sales Revenue")
    
    if predict_btn or 'last_prediction' in st.session_state:
        input_dict = {
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'Discount': discount,
            'Category': category,
            'Store': store,
            'Region': region,
            'Payment': payment,
            'Loyalty': loyalty,
            'CustomerAge': customer_age,
            'Gender': gender
        }
        
        pred_sales = predict_single_instance(artifacts, input_dict)
        st.session_state['last_prediction'] = pred_sales
        
        # Financial estimations based on inputs
        est_discount_amt = unit_price * quantity * discount
        est_gross_revenue = unit_price * quantity
        est_margin_pct = 22.0 if category == 'Electronics' else 28.0 if category == 'Clothing' else 25.0 if category == 'Home' else 18.0
        est_profit = pred_sales * (est_margin_pct / 100)
        
        st.markdown("<br><hr style='border-color: rgba(99, 102, 241, 0.2);'><br>", unsafe_allow_html=True)
        st.subheader("🎯 Projected Financial Summary")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_kpi_card("Predicted Sales", f"${pred_sales:,.2f}", "Model Output", "💰", "Primary Target")
        with c2:
            render_kpi_card("Estimated Profit", f"${est_profit:,.2f}", f"Est. Margin: {est_margin_pct:.0f}%", "📈", "Net Revenue")
        with c3:
            render_kpi_card("Discount Amount", f"${est_discount_amt:,.2f}", f"Deducted @ {int(discount*100)}%", "🎟️", "Promo Cost")
        with c4:
            render_kpi_card("Gross Revenue", f"${est_gross_revenue:,.2f}", "Before Discount", "🏷️", "Pre-Promo")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Breakdown visualization
        c_left, c_right = st.columns([6, 6])
        
        with c_left:
            breakdown_df = pd.DataFrame({
                'Component': ['Net Sales Revenue', 'Estimated Net Profit', 'Discount Granted'],
                'Amount ($)': [pred_sales, est_profit, est_discount_amt]
            })
            fig_waterfall = px.bar(
                breakdown_df,
                x='Component',
                y='Amount ($)',
                text_auto='.2f',
                color='Component',
                title="<b>Transaction Value Waterfall ($)</b>",
                color_discrete_sequence=['#6366F1', '#10B981', '#EC4899']
            )
            fig_waterfall = apply_plotly_theme(fig_waterfall)
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
        with c_right:
            # Scenario comparison against averages
            avg_sales = artifacts['y_test'].mean()
            comp_df = pd.DataFrame({
                'Scenario': ['Average Transaction', 'Current Config Prediction'],
                'Sales ($)': [avg_sales, pred_sales]
            })
            fig_comp = px.bar(
                comp_df,
                x='Scenario',
                y='Sales ($)',
                text_auto='.2f',
                color='Scenario',
                title="<b>Prediction vs Catalog Average Transaction ($)</b>",
                color_discrete_sequence=['#64748B', '#8B5CF6']
            )
            fig_comp = apply_plotly_theme(fig_comp)
            st.plotly_chart(fig_comp, use_container_width=True)
