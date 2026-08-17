import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

def generate_retail_dataset(n_samples=1000, seed=42):
    np.random.seed(seed)
    
    transaction_ids = np.arange(100000, 100000 + n_samples)
    dates = pd.date_range(start='2025-01-01', end='2025-12-31', periods=n_samples)
    stores = np.random.choice(['S1', 'S2', 'S3', 'S4'], size=n_samples, p=[0.28, 0.26, 0.24, 0.22])
    regions = np.random.choice(['North', 'South', 'East', 'West'], size=n_samples, p=[0.27, 0.25, 0.25, 0.23])
    
    # Customer Age with 5% missing values
    ages = np.random.randint(18, 71, size=n_samples).astype(float)
    missing_age_idx = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    ages[missing_age_idx] = np.nan
    
    genders = np.random.choice(['M', 'F'], size=n_samples, p=[0.52, 0.48])
    categories = np.random.choice(['Electronics', 'Clothing', 'Home', 'Grocery'], size=n_samples, p=[0.30, 0.28, 0.24, 0.18])
    products = [f"Product_{np.random.randint(1, 101)}" for _ in range(n_samples)]
    quantities = np.random.choice(np.arange(1, 11), size=n_samples, p=[0.12, 0.15, 0.15, 0.14, 0.12, 0.10, 0.08, 0.06, 0.04, 0.04])
    
    unit_prices = []
    for cat in categories:
        if cat == 'Electronics':
            price = np.random.uniform(150, 500)
        elif cat == 'Home':
            price = np.random.uniform(50, 350)
        elif cat == 'Clothing':
            price = np.random.uniform(20, 180)
        else: # Grocery
            price = np.random.uniform(5, 80)
        unit_prices.append(round(price, 2))
    unit_prices = np.array(unit_prices)
    
    discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=n_samples, p=[0.30, 0.25, 0.20, 0.15, 0.10])
    
    # Sales = Quantity * UnitPrice * (1 - Discount)
    sales = np.round(quantities * unit_prices * (1 - discounts), 2)
    
    # Profit Margin
    base_margin = np.array([0.22 if c=='Electronics' else 0.28 if c=='Clothing' else 0.25 if c=='Home' else 0.18 for c in categories])
    margin = base_margin - (discounts * 0.4) + np.random.normal(0, 0.02, size=n_samples)
    margin = np.clip(margin, 0.05, 0.45)
    profit = np.round(sales * margin, 2)
    
    payments = np.random.choice(['Card', 'UPI', 'Cash'], size=n_samples, p=[0.45, 0.38, 0.17])
    loyalty = np.random.choice(['Yes', 'No'], size=n_samples, p=[0.42, 0.58])
    
    df_raw = pd.DataFrame({
        'TransactionID': transaction_ids,
        'Date': dates,
        'Store': stores,
        'Region': regions,
        'CustomerAge': ages,
        'Gender': genders,
        'Category': categories,
        'Product': products,
        'Quantity': quantities,
        'UnitPrice': unit_prices,
        'Discount': discounts,
        'Sales': sales,
        'Profit': profit,
        'Payment': payments,
        'Loyalty': loyalty
    })
    
    # Add 20 duplicate rows to mimic original notebook
    duplicate_rows = df_raw.iloc[np.random.choice(n_samples, 20, replace=False)].copy()
    df_raw = pd.concat([df_raw, duplicate_rows], ignore_index=True)
    
    return df_raw

def clean_and_feature_engineer(df_raw):
    df_clean = df_raw.copy()
    
    # Impute missing CustomerAge with median
    median_age = df_clean['CustomerAge'].median()
    df_clean['CustomerAge'] = df_clean['CustomerAge'].fillna(median_age)
    
    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    
    # IQR Outlier Capping
    num_cols = ['CustomerAge', 'Quantity', 'UnitPrice', 'Discount', 'Sales', 'Profit']
    df_capped = df_clean.copy()
    for col in num_cols:
        Q1 = df_capped[col].quantile(0.25)
        Q3 = df_capped[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df_capped[col] = np.where(df_capped[col] < lower, lower, df_capped[col])
        df_capped[col] = np.where(df_capped[col] > upper, upper, df_capped[col])
        
    df_final = df_capped.copy()
    
    # Feature Engineering
    df_feature = df_final.copy()
    df_feature['Date'] = pd.to_datetime(df_feature['Date'])
    df_feature['Year'] = df_feature['Date'].dt.year
    df_feature['Month'] = df_feature['Date'].dt.month
    df_feature['Month_Name'] = df_feature['Date'].dt.month_name()
    df_feature['Day'] = df_feature['Date'].dt.day
    df_feature['Weekday'] = df_feature['Date'].dt.day_name()
    df_feature['Quarter'] = df_feature['Date'].dt.quarter
    df_feature['WeekOfYear'] = df_feature['Date'].dt.isocalendar().week.astype(int)
    df_feature['DayOfYear'] = df_feature['Date'].dt.dayofyear
    df_feature['IsWeekend'] = np.where(df_feature['Date'].dt.weekday >= 5, 1, 0)
    
    df_feature['Average_Item_Price'] = df_feature['Sales'] / df_feature['Quantity']
    df_feature['Discount_Amount'] = df_feature['UnitPrice'] * df_feature['Quantity'] * df_feature['Discount']
    df_feature['Profit_Margin'] = (df_feature['Profit'] / df_feature['Sales']) * 100
    df_feature['Age_Group'] = pd.cut(df_feature['CustomerAge'], bins=[0, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    df_feature['High_Discount'] = np.where(df_feature['Discount'] >= 0.15, 1, 0)
    
    return df_clean, df_final, df_feature

def train_and_save_models(df_feature):
    df_encoded = df_feature.copy()
    
    # Label Encoding
    le_gender = LabelEncoder()
    le_loyalty = LabelEncoder()
    df_encoded['Gender'] = le_gender.fit_transform(df_encoded['Gender'])
    df_encoded['Loyalty'] = le_loyalty.fit_transform(df_encoded['Loyalty'])
    
    # Drop identifiers and target-leakage engineered features for modeling
    drop_cols = ['Date', 'TransactionID', 'Product', 'Sales', 'Profit', 'Average_Item_Price', 'Profit_Margin']
    X_base = df_encoded.drop(columns=[c for c in drop_cols if c in df_encoded.columns])
    
    # One-Hot Encoding
    onehot_cols = ['Region', 'Store', 'Category', 'Payment', 'Month_Name', 'Weekday', 'Age_Group']
    X = pd.get_dummies(X_base, columns=onehot_cols, drop_first=True, dtype=int)
    y = df_encoded['Sales']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # Scale only continuous numerical columns
    continuous_features = ['CustomerAge', 'Quantity', 'UnitPrice', 'Discount', 'Discount_Amount', 'Year', 'Month', 'Day', 'Quarter', 'WeekOfYear', 'DayOfYear']
    num_scale_cols = [c for c in continuous_features if c in X_train.columns]
    
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[num_scale_cols] = scaler.fit_transform(X_train[num_scale_cols])
    X_test_scaled[num_scale_cols] = scaler.transform(X_test[num_scale_cols])
    
    models = {
        "Multiple Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Lasso Regression": Lasso(alpha=0.1),
        "Elastic Net": ElasticNet(alpha=0.1, l1_ratio=0.5)
    }
    
    n = len(y_test)
    p = X_train_scaled.shape[1]
    
    results = []
    fitted_models = {}
    
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        fitted_models[name] = model
        y_pred = model.predict(X_test_scaled)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        adj_r2 = 1 - ((1 - r2) * (n - 1) / (n - p - 1))
        
        results.append({
            "Model": name,
            "MAE": round(mae, 2),
            "MSE": round(mse, 2),
            "RMSE": round(rmse, 2),
            "MAPE": round(mape, 4),
            "R2 Score": round(r2, 4),
            "Adjusted R2": round(adj_r2, 4)
        })
        
    metrics_df = pd.DataFrame(results).sort_values(by="R2 Score", ascending=False)
    best_model_name = metrics_df.iloc[0]["Model"]
    best_model = fitted_models[best_model_name]
    
    artifacts = {
        'model': best_model,
        'all_models': fitted_models,
        'scaler': scaler,
        'num_scale_cols': num_scale_cols,
        'feature_names': list(X.columns),
        'le_gender': le_gender,
        'le_loyalty': le_loyalty,
        'onehot_cols': onehot_cols,
        'metrics_df': metrics_df,
        'X_test': X_test_scaled,
        'y_test': y_test,
        'y_pred': best_model.predict(X_test_scaled)
    }
    
    joblib.dump(artifacts, "Retail_Sales_Prediction_Model.joblib")
    return metrics_df, artifacts

if __name__ == '__main__':
    print("Generating raw retail dataset...")
    df_raw = generate_retail_dataset(n_samples=1000)
    df_raw.to_excel("Retail Analysis.xlsx", index=False)
    df_raw.to_csv("retail_sales_raw.csv", index=False)
    
    print("Cleaning & Feature Engineering...")
    df_clean, df_final, df_feature = clean_and_feature_engineer(df_raw)
    df_clean.to_csv("retail_sales_clean.csv", index=False)
    df_feature.to_csv("retail_sales_engineered.csv", index=False)
    
    print("Training ML Models...")
    metrics_df, artifacts = train_and_save_models(df_feature)
    print("\nModel Comparison Table:")
    print(metrics_df.to_string(index=False))
    print("\nModel saved to Retail_Sales_Prediction_Model.joblib successfully!")
