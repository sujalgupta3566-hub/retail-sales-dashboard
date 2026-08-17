import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from components import render_hero, render_kpi_card
from utils import apply_plotly_theme

def show_feature_engineering_page(df_clean, df_feature, artifacts):
    render_hero(
        title="Feature Engineering Studio & Importances",
        subtitle="Unpack engineered temporal, financial, and categorical features, analyze correlation shifts before and after engineering, and examine predictive feature importances.",
        icon="⚙️"
    )
    
    st.subheader("💡 Feature Engineering Logic & Explanation")
    
    fe_explanations = [
        {"Feature": "Year, Month, Day, Weekday, Quarter, WeekOfYear", "Type": "Temporal", "Description": "Extracted from `Date` to capture seasonal trends, monthly spikes, and day-of-week purchasing patterns."},
        {"Feature": "IsWeekend", "Type": "Binary Flag", "Description": "Flag (`1` if Saturday/Sunday else `0`) identifying weekend shopping surges."},
        {"Feature": "Average_Item_Price", "Type": "Financial Ratio", "Description": "Calculated as `Sales / Quantity`. Represents effective price per unit after promotional discount."},
        {"Feature": "Discount_Amount", "Type": "Financial Metric", "Description": "Calculated as `UnitPrice * Quantity * Discount`. Quantifies total dollar discount granted."},
        {"Feature": "Profit_Margin", "Type": "Percentage Ratio", "Description": "Calculated as `(Profit / Sales) * 100`. Measures operational profitability per transaction."},
        {"Feature": "Age_Group", "Type": "Binned Categorical", "Description": "Segmented `CustomerAge` into 5 demographic cohorts (`18-25`, `26-35`, `36-45`, `46-55`, `55+`)."},
        {"Feature": "High_Discount", "Type": "Threshold Flag", "Description": "Binary flag (`1` if `Discount >= 15%` else `0`) indicating aggressive promotional discounting."}
    ]
    
    st.table(pd.DataFrame(fe_explanations))
    
    st.markdown("<br><hr style='border-color: rgba(99, 102, 241, 0.2);'><br>", unsafe_allow_html=True)
    
    st.subheader("🔥 Correlation Shift Analysis (Before vs After Feature Engineering)")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### Correlation Heatmap (Before Engineering)")
        num_before = df_clean.select_dtypes(include=['float64', 'int64'])
        fig_before = px.imshow(
            num_before.corr(),
            text_auto='.2f',
            color_continuous_scale='Blues',
            title="<b>Correlation Heatmap (Original Numerical Features)</b>"
        )
        fig_before = apply_plotly_theme(fig_before)
        st.plotly_chart(fig_before, use_container_width=True)
        
    with c2:
        st.markdown("#### Correlation Heatmap (After Feature Engineering)")
        num_after = df_feature.select_dtypes(include=['float64', 'int64', 'int32'])
        top_after_cols = ['Sales', 'UnitPrice', 'Quantity', 'Discount', 'Discount_Amount', 'Average_Item_Price', 'Profit', 'Profit_Margin']
        fig_after = px.imshow(
            num_after[top_after_cols].corr(),
            text_auto='.2f',
            color_continuous_scale='Purples',
            title="<b>Correlation Heatmap (Engineered Key Features)</b>"
        )
        fig_after = apply_plotly_theme(fig_after)
        st.plotly_chart(fig_after, use_container_width=True)

    st.markdown("<br><hr style='border-color: rgba(99, 102, 241, 0.2);'><br>", unsafe_allow_html=True)
    
    st.subheader("🎯 Top Predictive Features & Model Importance")
    
    model = artifacts['model']
    feature_names = artifacts['feature_names']
    
    if hasattr(model, 'coef_'):
        coefs = np.abs(model.coef_)
        fi_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': coefs
        }).sort_values(by='Importance', ascending=False).head(15)
        
        c1, c2 = st.columns([7, 5])
        
        with c1:
            fig_fi = px.bar(
                fi_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title="<b>Top 15 Feature Importances (|Model Coefficients|)</b>",
                color='Importance',
                color_continuous_scale='Purples'
            )
            fig_fi.update_layout(yaxis=dict(autorange="reversed"))
            fig_fi = apply_plotly_theme(fig_fi)
            st.plotly_chart(fig_fi, use_container_width=True)
            
        with c2:
            st.markdown("#### Key Predictive Insights")
            st.markdown("""
            - 🥇 **`Average_Item_Price` & `Quantity`**: Strongest direct linear determinants of gross Sales.
            - 🥈 **`Discount_Amount`**: High negative impact on net revenue margins when promotional rates exceed 15%.
            - 🥉 **`Category_Electronics` & `Category_Home`**: One-hot encoded high-ticket categories show strong positive weights.
            - 🏅 **`High_Discount`**: Crucial binary indicator for margin erosion.
            """)
