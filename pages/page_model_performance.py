import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from components import render_hero, render_kpi_card
from utils import apply_plotly_theme

def show_model_performance_page(artifacts):
    render_hero(
        title="Machine Learning Model Evaluation Studio",
        subtitle="Detailed regression benchmarks, actual vs predicted analysis, residual diagnostics, and error distribution for Multiple Linear Regression & Regularized variants.",
        icon="🎯"
    )
    
    metrics_df = artifacts['metrics_df']
    best_model_name = metrics_df.iloc[0]['Model']
    
    st.subheader(f"🏆 Best Trained Model: {best_model_name}")
    
    # Model evaluation metrics cards
    best_row = metrics_df.iloc[0]
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_kpi_card("R² Score", f"{best_row['R2 Score']:.4f}", "Variance Explained", "🎯", "Top Fit")
    with c2:
        render_kpi_card("Adjusted R²", f"{best_row['Adjusted R2']:.4f}", "Penalized Feature Fit", "📐", "High Acc")
    with c3:
        render_kpi_card("MAE ($)", f"${best_row['MAE']:.2f}", "Mean Absolute Error", "📉", "Avg Error")
    with c4:
        render_kpi_card("MSE ($²)", f"{best_row['MSE']:,.2f}", "Mean Squared Error", "📊", "Variance")
    with c5:
        render_kpi_card("RMSE ($)", f"${best_row['RMSE']:.2f}", "Root Mean Sq Error", "🔍", "Standard Dev")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📊 Regression Models Benchmark Comparison Table")
    st.dataframe(metrics_df, use_container_width=True)
    
    st.markdown("<br><hr style='border-color: rgba(99, 102, 241, 0.2);'><br>", unsafe_allow_html=True)
    
    # Model Diagnostics Plots
    y_test = artifacts['y_test']
    y_pred = artifacts['y_pred']
    residuals = y_test - y_pred
    
    st.subheader("🔍 Model Diagnostic & Error Plots")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # Actual vs Predicted Scatter Plot
        fig_actual_pred = px.scatter(
            x=y_test,
            y=y_pred,
            labels={'x': 'Actual Sales ($)', 'y': 'Predicted Sales ($)'},
            title="<b>Actual vs Predicted Sales Scatter Plot</b>",
            color_discrete_sequence=['#6366F1']
        )
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        fig_actual_pred.add_trace(
            go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode='lines', line=dict(color='#EC4899', width=2, dash='dash'), name='Ideal 1:1 Fit')
        )
        fig_actual_pred = apply_plotly_theme(fig_actual_pred)
        st.plotly_chart(fig_actual_pred, use_container_width=True)
        
    with c2:
        # Residual Plot (Residuals vs Predicted)
        fig_res = px.scatter(
            x=y_pred,
            y=residuals,
            labels={'x': 'Predicted Sales ($)', 'y': 'Residuals ($)'},
            title="<b>Residual Scatter Plot (Residuals vs Predicted)</b>",
            color_discrete_sequence=['#8B5CF6']
        )
        fig_res.add_hline(y=0, line_dash="dash", line_color="#EC4899")
        fig_res = apply_plotly_theme(fig_res)
        st.plotly_chart(fig_res, use_container_width=True)
        
    c3, c4 = st.columns(2)
    
    with c3:
        # Distribution of Residuals
        fig_res_dist = px.histogram(
            x=residuals,
            nbins=30,
            title="<b>Distribution of Residuals (Normality Check)</b>",
            color_discrete_sequence=['#06B6D4'],
            marginal="box"
        )
        fig_res_dist = apply_plotly_theme(fig_res_dist)
        st.plotly_chart(fig_res_dist, use_container_width=True)
        
    with c4:
        # Prediction Error Plot
        error_df = pd.DataFrame({
            'Actual': y_test,
            'Predicted': y_pred,
            'Error': np.abs(residuals)
        }).sort_values(by='Actual').reset_index(drop=True)
        
        fig_err = px.line(
            error_df,
            y=['Actual', 'Predicted'],
            title="<b>Actual vs Predicted Curve (Sorted Test Sample)</b>",
            color_discrete_sequence=['#6366F1', '#EC4899']
        )
        fig_err = apply_plotly_theme(fig_err)
        st.plotly_chart(fig_err, use_container_width=True)
