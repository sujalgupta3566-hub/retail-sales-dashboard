import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_datasets():
    if not os.path.exists("retail_sales_raw.csv"):
        import generate_data
        df_raw = generate_data.generate_retail_dataset()
        df_clean, df_final, df_feature = generate_data.clean_and_feature_engineer(df_raw)
        df_raw.to_csv("retail_sales_raw.csv", index=False)
        df_clean.to_csv("retail_sales_clean.csv", index=False)
        df_feature.to_csv("retail_sales_engineered.csv", index=False)
    else:
        df_raw = pd.read_csv("retail_sales_raw.csv")
        df_clean = pd.read_csv("retail_sales_clean.csv")
        df_feature = pd.read_csv("retail_sales_engineered.csv")
        
    df_raw['Date'] = pd.to_datetime(df_raw['Date'])
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    df_feature['Date'] = pd.to_datetime(df_feature['Date'])
    
    return df_raw, df_clean, df_feature

@st.cache_resource
def load_ml_artifacts():
    if not os.path.exists("Retail_Sales_Prediction_Model.joblib"):
        import generate_data
        df_raw = generate_data.generate_retail_dataset()
        _, _, df_feature = generate_data.clean_and_feature_engineer(df_raw)
        metrics_df, artifacts = generate_data.train_and_save_models(df_feature)
    else:
        artifacts = joblib.load("Retail_Sales_Prediction_Model.joblib")
    return artifacts

def apply_plotly_theme(fig):
    fig.update_layout(
        paper_bgcolor='rgba(15, 23, 42, 0.0)',
        plot_bgcolor='rgba(15, 23, 42, 0.0)',
        font=dict(family="Inter, sans-serif", size=13, color="#E2E8F0"),
        title=dict(font=dict(size=18, color="#F8FAFC", family="Inter, sans-serif")),
        legend=dict(
            bgcolor='rgba(30, 41, 59, 0.5)',
            bordercolor='rgba(99, 102, 241, 0.2)',
            borderwidth=1,
            font=dict(color="#CBD5E1")
        ),
        xaxis=dict(
            gridcolor='rgba(51, 65, 85, 0.3)',
            zerolinecolor='rgba(99, 102, 241, 0.3)',
            tickfont=dict(color="#94A3B8"),
            title_font=dict(color="#CBD5E1")
        ),
        yaxis=dict(
            gridcolor='rgba(51, 65, 85, 0.3)',
            zerolinecolor='rgba(99, 102, 241, 0.3)',
            tickfont=dict(color="#94A3B8"),
            title_font=dict(color="#CBD5E1")
        ),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def predict_single_instance(artifacts, input_dict):
    """
    input_dict keys: Quantity, UnitPrice, Discount, Category, Store, Region, Payment, Loyalty, CustomerAge, Gender
    """
    model = artifacts['model']
    scaler = artifacts['scaler']
    feature_names = artifacts['feature_names']
    num_scale_cols = artifacts.get('num_scale_cols', ['CustomerAge', 'Quantity', 'UnitPrice', 'Discount', 'Discount_Amount', 'Year', 'Month', 'Day', 'Quarter', 'WeekOfYear', 'DayOfYear'])
    le_gender = artifacts['le_gender']
    le_loyalty = artifacts['le_loyalty']
    
    qty = float(input_dict['Quantity'])
    unit_price = float(input_dict['UnitPrice'])
    discount = float(input_dict['Discount'])
    cat = str(input_dict['Category'])
    store = str(input_dict['Store'])
    region = str(input_dict['Region'])
    payment = str(input_dict['Payment'])
    loyalty = str(input_dict['Loyalty'])
    age = float(input_dict.get('CustomerAge', 38.0))
    gender = str(input_dict.get('Gender', 'M'))
    
    date = pd.Timestamp.now()
    year = float(date.year)
    month = float(date.month)
    month_name = date.month_name()
    day = float(date.day)
    weekday = date.day_name()
    quarter = float(date.quarter)
    week_of_year = float(date.isocalendar().week)
    day_of_year = float(date.dayofyear)
    is_weekend = 1.0 if date.weekday() >= 5 else 0.0
    
    discount_amount = unit_price * qty * discount
    high_discount = 1.0 if discount >= 0.15 else 0.0
    
    if age <= 25:
        age_group = '18-25'
    elif age <= 35:
        age_group = '26-35'
    elif age <= 45:
        age_group = '36-45'
    elif age <= 55:
        age_group = '46-55'
    else:
        age_group = '55+'
        
    gender_val = float(le_gender.transform([gender])[0]) if gender in le_gender.classes_ else 0.0
    loyalty_val = float(le_loyalty.transform([loyalty])[0]) if loyalty in le_loyalty.classes_ else 0.0
    
    row_dict = {
        'CustomerAge': age,
        'Gender': gender_val,
        'Quantity': qty,
        'UnitPrice': unit_price,
        'Discount': discount,
        'Loyalty': loyalty_val,
        'Year': year,
        'Month': month,
        'Day': day,
        'Quarter': quarter,
        'WeekOfYear': week_of_year,
        'DayOfYear': day_of_year,
        'IsWeekend': is_weekend,
        'Discount_Amount': discount_amount,
        'High_Discount': high_discount
    }
    
    # One-hot dummy mappings
    onehot_flags = [
        f'Region_{region}',
        f'Store_{store}',
        f'Category_{cat}',
        f'Payment_{payment}',
        f'Month_Name_{month_name}',
        f'Weekday_{weekday}',
        f'Age_Group_{age_group}'
    ]
    for flag in onehot_flags:
        row_dict[flag] = 1.0
        
    # Build complete DataFrame matching model features
    full_row = {col: float(row_dict.get(col, 0.0)) for col in feature_names}
    df_row = pd.DataFrame([full_row], columns=feature_names)
    
    # Scale only the continuous numerical features
    cols_to_scale = [c for c in num_scale_cols if c in df_row.columns]
    df_row_scaled = df_row.copy()
    df_row_scaled[cols_to_scale] = scaler.transform(df_row[cols_to_scale])
    
    pred_sales = model.predict(df_row_scaled)[0]
    return max(0.0, float(pred_sales))
