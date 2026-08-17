import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from components import render_hero, render_kpi_card
from utils import apply_plotly_theme

def show_dataset_page(df_raw, df_clean, df_feature):
    render_hero(
        title="Dataset Explorer & Data Health Diagnostics",
        subtitle="Inspect raw & cleaned retail transaction data, dataset dimensions, schema, missing values, duplicates, and statistical distribution summaries.",
        icon="📁"
    )
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Dataset Preview", 
        "📐 Dataset Shape & Schema", 
        "❓ Missing Values Analysis", 
        "👯 Duplicate Records", 
        "📊 Summary Statistics"
    ])
    
    with tab1:
        st.subheader("Interactive Dataset Viewer")
        dataset_choice = st.radio(
            "Select Dataset Stage:",
            ["Raw Dataset (Before Cleaning)", "Cleaned Dataset (Post Imputation & Outlier Capping)", "Feature Engineered Dataset"],
            horizontal=True
        )
        
        if dataset_choice == "Raw Dataset (Before Cleaning)":
            active_df = df_raw
        elif dataset_choice == "Cleaned Dataset (Post Imputation & Outlier Capping)":
            active_df = df_clean
        else:
            active_df = df_feature
            
        st.write(f"Displaying **{len(active_df):,}** records and **{active_df.shape[1]}** features.")
        st.dataframe(active_df, use_container_width=True, height=450)
        
    with tab2:
        st.subheader("Dataset Shape & Data Types")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_kpi_card("Total Rows", f"{len(df_raw):,}", "Raw Sample Size", "🔢")
        with c2:
            render_kpi_card("Cleaned Rows", f"{len(df_clean):,}", "Post Duplicate Drop", "✅")
        with c3:
            render_kpi_card("Total Columns", f"{df_raw.shape[1]}", "Original Features", "🏛️")
        with c4:
            render_kpi_card("Engineered Features", f"{df_feature.shape[1]}", "Post Feature Creation", "⚡")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.subheader("Column Names & Data Types Breakdown")
        col_info = pd.DataFrame({
            "Column Name": df_raw.columns,
            "Data Type": df_raw.dtypes.astype(str),
            "Non-Null Count": df_raw.notnull().sum().values,
            "Null Count": df_raw.isnull().sum().values,
            "Unique Values": [df_raw[c].nunique() for c in df_raw.columns]
        })
        st.dataframe(col_info, use_container_width=True)
        
    with tab3:
        st.subheader("Missing Values Analysis")
        
        raw_missing = df_raw.isnull().sum()
        raw_missing_df = pd.DataFrame({
            "Column": raw_missing.index,
            "Missing Count": raw_missing.values,
            "Missing Percentage (%)": np.round((raw_missing.values / len(df_raw)) * 100, 2)
        }).sort_values(by="Missing Count", ascending=False)
        
        c1, c2 = st.columns([5, 7])
        
        with c1:
            st.markdown("#### Missing Value Summary Table")
            st.dataframe(raw_missing_df, use_container_width=True)
            st.info("💡 **Imputation Strategy Applied:** Numerical missing values (e.g. `CustomerAge`) were imputed using **Median Imputation** to prevent outlier distortion.")
            
        with c2:
            fig_missing = px.bar(
                raw_missing_df[raw_missing_df["Missing Count"] > 0],
                x="Column",
                y="Missing Count",
                text="Missing Percentage (%)",
                title="<b>Missing Values by Column (Raw Data)</b>",
                color_discrete_sequence=['#EC4899']
            )
            fig_missing.update_traces(textposition='outside')
            fig_missing = apply_plotly_theme(fig_missing)
            st.plotly_chart(fig_missing, use_container_width=True)
            
    with tab4:
        st.subheader("Duplicate Records Diagnostics")
        
        dups_count = df_raw.duplicated().sum()
        
        st.warning(f"⚠️ **Duplicate Rows Detected in Raw Data:** `{dups_count}` rows.")
        
        if dups_count > 0:
            st.markdown("#### Preview of Duplicate Rows")
            dups_df = df_raw[df_raw.duplicated(keep=False)]
            st.dataframe(dups_df, use_container_width=True)
            st.success("✅ **Action Taken:** Duplicate records were permanently dropped (`df.drop_duplicates()`) during the cleaning phase.")
        else:
            st.success("No duplicate records found.")
            
    with tab5:
        st.subheader("Summary Statistics")
        st.markdown("Five-number summary, mean, standard deviation, and metrics for numerical variables.")
        
        num_clean = df_clean.select_dtypes(include=['number'])
        stats_df = num_clean.describe().T.reset_index()
        stats_df.columns = ['Feature', 'Count', 'Mean', 'Std Dev', 'Min', '25% (Q1)', '50% (Median)', '75% (Q3)', 'Max']
        stats_df = stats_df.round(2)
        st.dataframe(stats_df, use_container_width=True)
