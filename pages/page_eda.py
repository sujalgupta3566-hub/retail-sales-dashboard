import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from components import render_hero
from utils import apply_plotly_theme

def show_eda_page(df_clean, df_feature):
    render_hero(
        title="Exploratory Data Analysis (EDA) Studio",
        subtitle="100% Plotly-powered interactive visualization studio to uncover sales patterns, distributions, correlations, customer behavior, and pricing dynamics.",
        icon="📈"
    )
    
    # Categorized Tabs for structured navigation
    tab_dist, tab_bivariate, tab_cat, tab_corr, tab_insights = st.tabs([
        "📊 Distributions & Outliers",
        "🎯 Feature Relationships & Bivariate",
        "🛍️ Categorical & Segmentation Analysis",
        "🔥 Correlation & Pair Matrix",
        "💡 Deep Dive Sales Drivers"
    ])
    
    with tab_dist:
        st.subheader("Distribution Analysis (Histograms & Boxplots)")
        
        num_col = st.selectbox(
            "Select Numerical Feature to Analyze:",
            ['Sales', 'Profit', 'UnitPrice', 'Quantity', 'Discount', 'CustomerAge']
        )
        
        c1, c2 = st.columns(2)
        
        with c1:
            fig_hist = px.histogram(
                df_clean,
                x=num_col,
                nbins=30,
                marginal="rug",
                title=f"<b>Distribution Histogram of {num_col}</b>",
                color_discrete_sequence=['#8B5CF6']
            )
            fig_hist = apply_plotly_theme(fig_hist)
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with c2:
            fig_box = px.box(
                df_clean,
                x=num_col,
                points="all",
                title=f"<b>Boxplot & Outliers for {num_col}</b>",
                color_discrete_sequence=['#EC4899']
            )
            fig_box = apply_plotly_theme(fig_box)
            st.plotly_chart(fig_box, use_container_width=True)
            
    with tab_bivariate:
        st.subheader("Scatter Plot Analysis & Regression Trends")
        
        col_pair = st.selectbox(
            "Select Bivariate Relationship:",
            [
                "Quantity vs Sales", 
                "UnitPrice vs Sales", 
                "Discount vs Profit", 
                "CustomerAge vs Sales"
            ]
        )
        
        if col_pair == "Quantity vs Sales":
            x_var, y_var = "Quantity", "Sales"
        elif col_pair == "UnitPrice vs Sales":
            x_var, y_var = "UnitPrice", "Sales"
        elif col_pair == "Discount vs Profit":
            x_var, y_var = "Discount", "Profit"
        else:
            x_var, y_var = "CustomerAge", "Sales"
            
        fig_scatter = px.scatter(
            df_clean,
            x=x_var,
            y=y_var,
            color="Category",
            size="Sales" if y_var != "Sales" else "Quantity",
            hover_data=["Store", "Region", "Payment"],
            trendline="ols",
            title=f"<b>Scatter Plot: {y_var} vs {x_var} (colored by Category)</b>",
            color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
        )
        fig_scatter = apply_plotly_theme(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with tab_cat:
        st.subheader("Categorical & Regional Distributions")
        
        c1, c2 = st.columns(2)
        
        with c1:
            # Category-wise Sales
            cat_sales = df_clean.groupby('Category')['Sales'].agg(['sum', 'mean']).reset_index()
            fig_cat_bar = px.bar(
                cat_sales,
                x='Category',
                y='sum',
                color='Category',
                text_auto='.2s',
                title="<b>Total Category Sales ($)</b>",
                color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
            )
            fig_cat_bar = apply_plotly_theme(fig_cat_bar)
            st.plotly_chart(fig_cat_bar, use_container_width=True)
            
        with c2:
            # Store-wise Sales
            store_sales = df_clean.groupby('Store')['Sales'].sum().reset_index()
            fig_store_bar = px.bar(
                store_sales,
                x='Store',
                y='Sales',
                color='Store',
                text_auto='.2s',
                title="<b>Total Store Revenue ($)</b>",
                color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
            )
            fig_store_bar = apply_plotly_theme(fig_store_bar)
            st.plotly_chart(fig_store_bar, use_container_width=True)
            
        c3, c4 = st.columns(2)
        
        with c3:
            # Payment Method Distribution
            pay_dist = df_clean['Payment'].value_counts().reset_index()
            pay_dist.columns = ['Payment Method', 'Count']
            fig_pay = px.pie(
                pay_dist,
                names='Payment Method',
                values='Count',
                hole=0.45,
                title="<b>Payment Method Distribution</b>",
                color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899']
            )
            fig_pay = apply_plotly_theme(fig_pay)
            st.plotly_chart(fig_pay, use_container_width=True)
            
        with c4:
            # Loyalty Customer Analysis
            loyalty_sales = df_clean.groupby(['Loyalty', 'Category'])['Sales'].sum().reset_index()
            fig_loyalty = px.bar(
                loyalty_sales,
                x='Loyalty',
                y='Sales',
                color='Category',
                barmode='group',
                title="<b>Loyalty Program Revenue Contribution ($)</b>",
                color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
            )
            fig_loyalty = apply_plotly_theme(fig_loyalty)
            st.plotly_chart(fig_loyalty, use_container_width=True)
            
    with tab_corr:
        st.subheader("Correlation Heatmap & Pair Plot Matrix")
        
        num_df = df_clean.select_dtypes(include=['float64', 'int64'])
        corr = num_df.corr()
        
        fig_heat = px.imshow(
            corr,
            text_auto='.2f',
            color_continuous_scale='Purples',
            title="<b>Numerical Feature Correlation Matrix</b>",
            aspect="auto"
        )
        fig_heat = apply_plotly_theme(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Multivariable Pair Plot / Matrix Scatter Plot")
        
        fig_pair = px.scatter_matrix(
            df_clean,
            dimensions=['Sales', 'Profit', 'UnitPrice', 'Quantity', 'Discount'],
            color="Category",
            title="<b>Pair Plot Matrix across Key Numerical Features</b>",
            color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
        )
        fig_pair = apply_plotly_theme(fig_pair)
        st.plotly_chart(fig_pair, use_container_width=True)

    with tab_insights:
        st.subheader("Deep-Dive Key Sales Driver Charts")
        
        c1, c2 = st.columns(2)
        
        with c1:
            # Discount vs Profit Analysis
            fig_disc_prof = px.box(
                df_clean,
                x='Discount',
                y='Profit',
                color='Category',
                title="<b>Impact of Discount Rates on Net Profit ($)</b>",
                color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
            )
            fig_disc_prof = apply_plotly_theme(fig_disc_prof)
            st.plotly_chart(fig_disc_prof, use_container_width=True)
            
        with c2:
            # Unit Price vs Sales
            fig_price_sales = px.scatter(
                df_clean,
                x='UnitPrice',
                y='Sales',
                color='Category',
                trendline="lowess",
                title="<b>Unit Price vs Total Sales ($)</b>",
                color_discrete_sequence=['#6366F1', '#8B5CF6', '#EC4899', '#06B6D4']
            )
            fig_price_sales = apply_plotly_theme(fig_price_sales)
            st.plotly_chart(fig_price_sales, use_container_width=True)
