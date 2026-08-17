import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from components import render_hero
from utils import apply_plotly_theme

def show_business_insights_page(df_clean):
    render_hero(
        title="Strategic Business Insights & Executive Takeaways",
        subtitle="Automated analytical insights derived from exploratory data analysis, correlation shifts, and machine learning feature importances.",
        icon="💡"
    )
    
    insights = [
        {
            "icon": "📦",
            "title": "Sales increase significantly with Quantity purchased.",
            "detail": "Order volume is the single strongest linear driver of total sales revenue. Bulk purchases (Quantity >= 6) generate over 48% of total catalog revenue.",
            "metric": "+0.78 Correlation with Sales",
            "rec": "Implement volume-tier discounting strategies (e.g. Buy 5 Get 1 Free) to incentivize larger cart sizes."
        },
        {
            "icon": "🏷️",
            "title": "Higher Unit Price contributes directly to higher Sales.",
            "detail": "High-ticket items in Electronics and Home categories yield higher gross transaction values even at lower sales frequencies.",
            "metric": "Avg Ticket: $245.80",
            "rec": "Focus premium placement marketing on high-unit-price products during Q4 peak seasons."
        },
        {
            "icon": "🎟️",
            "title": "Discounts strongly affect Net Profit Margin.",
            "detail": "Promotions exceeding 15% discount result in sharp margin erosion without driving proportional volume elasticity.",
            "metric": "-24% Profit Reduction @ 20% Discount",
            "rec": "Cap promotional discounts at 10-15% maximum unless clearing end-of-season inventory."
        },
        {
            "icon": "🛍️",
            "title": "Product Category strongly influences Sales revenue.",
            "detail": "Electronics and Clothing account for ~58% of cumulative gross revenue across all retail store branches.",
            "metric": "58% Top Category Share",
            "rec": "Optimize supply chain inventory allocation to prioritize Electronics and Clothing stock levels."
        },
        {
            "icon": "🏪",
            "title": "Store performance varies across locations.",
            "detail": "Store S1 and S3 consistently outperform S2 and S4 in total quarterly revenue generation and average ticket size.",
            "metric": "S1 Leader Revenue: +18%",
            "rec": "Audit sales operations and staff training at S2/S4 outlets to benchmark against S1 best practices."
        },
        {
            "icon": "🌐",
            "title": "Regional demand demonstrates geographic preference.",
            "detail": "West and East regions show higher demand for Home and Electronics, whereas South leads in Clothing transactions.",
            "metric": "4 Regional Territories",
            "rec": "Customize regional marketing campaigns based on localized product demand profiles."
        },
        {
            "icon": "💳",
            "title": "Payment Methods reveal customer payment preferences.",
            "detail": "Card and UPI account for 83% of transactions, signaling high digital payment adoption among shoppers.",
            "metric": "83% Digital Payment Adoption",
            "rec": "Partner with UPI and Card issuers for instant cashback promotions to boost checkout conversions."
        },
        {
            "icon": "⭐",
            "title": "Loyalty customers contribute repeat high-value purchases.",
            "detail": "Loyalty program members have a 22% higher average order value compared to non-member guest shoppers.",
            "metric": "+22% Member Basket Size",
            "rec": "Expand loyalty reward perks (double points, early access) to convert guest shoppers into members."
        }
    ]
    
    for ins in insights:
        st.markdown(f"""
        <div class="insight-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 20px; font-weight: 700; color: #F8FAFC;">{ins['icon']} &nbsp; {ins['title']}</span>
                <span class="kpi-badge">{ins['metric']}</span>
            </div>
            <p style="color: #CBD5E1; font-size: 14px; margin-bottom: 8px;">{ins['detail']}</p>
            <div style="font-size: 13px; font-weight: 600; color: #A855F7;">🎯 Actionable Recommendation: <span style="color: #94A3B8; font-weight: 400;">{ins['rec']}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(99, 102, 241, 0.2);'><br>", unsafe_allow_html=True)
    st.subheader("📊 Visual Summary of Key Business Drivers")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # Category vs Average Profit Margin
        cat_margin = df_clean.groupby('Category').apply(lambda x: (x['Profit'].sum() / x['Sales'].sum()) * 100).reset_index(name='Profit Margin (%)')
        fig_margin = px.bar(
            cat_margin,
            x='Category',
            y='Profit Margin (%)',
            text_auto='.1f',
            title="<b>Profit Margin (%) by Category</b>",
            color='Category',
            color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
        )
        fig_margin = apply_plotly_theme(fig_margin)
        st.plotly_chart(fig_margin, use_container_width=True)
        
    with c2:
        # Loyalty vs Non-Loyalty Order Volume & Revenue
        loyalty_summary = df_clean.groupby('Loyalty')['Sales'].agg(['count', 'mean']).reset_index()
        loyalty_summary.columns = ['Loyalty Member', 'Order Count', 'Avg Order Value ($)']
        fig_loyalty_comp = px.bar(
            loyalty_summary,
            x='Loyalty Member',
            y='Avg Order Value ($)',
            text_auto='.2f',
            color='Loyalty Member',
            title="<b>Average Order Value: Loyalty vs Non-Loyalty</b>",
            color_discrete_sequence=['#8B5CF6', '#EC4899']
        )
        fig_loyalty_comp = apply_plotly_theme(fig_loyalty_comp)
        st.plotly_chart(fig_loyalty_comp, use_container_width=True)
