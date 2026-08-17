# 🛍️ Retail Sales Prediction & Business Intelligence Dashboard

[![Python Version](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.0+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An end-to-end **Business Intelligence & Machine Learning Dashboard** designed for executive data analytics, retail demand forecasting, pricing strategy optimization, and transaction-level sales prediction. Built with **Python**, **Streamlit**, **Plotly**, and **Scikit-Learn**.

---

## ✨ Features & Dashboard Pages

### 🎨 Premium Glassmorphism UI/UX
- **Dark Theme Palette**: Deep space background (`#090D16`), glowing indigo (`#6366F1`) & purple (`#8B5CF6`) accents, and glassmorphic container cards.
- **Animated KPI Metrics**: Interactive metric cards with hover-elevation animations, trend indicators, and high-contrast typography.
- **100% Plotly Charts**: Interactive plots with hover tooltips, custom dark colorways, and responsive layouts.

### 📱 8 Dedicated Dashboard Pages
1. **📊 Executive Overview**: High-level sales revenue, profit margin, volume metrics, store branch comparisons, and monthly revenue trends.
2. **📁 Dataset Explorer**: Interactive dataset viewer across raw, cleaned, and feature-engineered stages, dataset shape, column schema, missing values analysis, duplicates diagnostics, and summary statistics.
3. **📈 Exploratory Data Analysis (EDA)**: Interactive distribution histograms, boxplots for outlier analysis, lowess/OLS regression scatter plots, payment method pie charts, loyalty contribution bars, correlation heatmaps, and pair plot scatter matrices.
4. **⚙️ Feature Engineering Studio**: Breakdown of engineered features (`Year`, `Month`, `Weekday`, `IsWeekend`, `Average_Item_Price`, `Discount_Amount`, `Profit_Margin`, `Age_Group`, `High_Discount`), correlation shift analysis (Before vs After), and top 15 predictive feature importances.
5. **🎯 Model Evaluation Studio**: Benchmark comparison across Multiple Linear Regression, Ridge, Lasso, and ElasticNet models. Includes R² (0.9859), Adjusted R², MAE ($52.91), MSE, RMSE ($74.03) metrics, Actual vs Predicted scatter plots, Residual plots, Residual distribution normality checks, and error curves.
6. **🔮 Real-Time Sales Prediction Engine**: Interactive input controls (Quantity, Unit Price, Discount, Category, Store, Region, Payment Method, Loyalty) with instant model inference, transaction value waterfall, profit estimation, and baseline comparisons.
7. **💡 Strategic Business Insights**: 8 automated data-driven insights backed by visuals and actionable business recommendations (pricing elasticity, discount caps, store operational benchmarks, loyalty program expansion).
8. **👨‍💻 About Project**: Full tech stack documentation, project architecture, machine learning workflow, and developer profile card for **Sujal Gupta**.

---

## 🛠️ Tech Stack & Libraries

- **Language:** Python 3.11
- **Web Framework:** Streamlit
- **Data Manipulation & Stats:** Pandas, NumPy, SciPy
- **Data Visualization:** Plotly Express & Plotly Graph Objects (Notebook EDA: Matplotlib, Seaborn)
- **Machine Learning:** Scikit-Learn (LinearRegression, Ridge, Lasso, ElasticNet, StandardScaler, LabelEncoder)
- **Model Serialization:** Joblib
- **File I/O:** Openpyxl

---

## 📁 Repository Structure

```
reatail_sales/
├── app.py                      # Main Streamlit Application Router & Theme Setup
├── utils.py                    # Dataset Loaders, Streamlit Caching & ML Inference Helpers
├── components.py               # Custom CSS Design System, Glassmorphism Cards & Footer
├── generate_data.py            # Data Pipeline Script (Dataset Generation & Model Training)
├── Retail_Sales.ipynb          # Jupyter Notebook containing full EDA & ML modeling
├── Retail_Sales_Prediction_Model.joblib # Saved Pre-trained ML Model Binary
├── retail_sales_raw.csv        # Raw Transaction Dataset
├── retail_sales_clean.csv      # Cleaned Dataset
├── retail_sales_engineered.csv # Feature Engineered Dataset
├── README.md                   # Repository Documentation
└── pages/                      # Modular Page Views
    ├── page_overview.py        # Executive Summary & KPIs
    ├── page_dataset.py         # Dataset Explorer & Health Diagnostics
    ├── page_eda.py             # 100% Plotly Exploratory Data Analysis
    ├── page_feature_engineering.py # Feature Engineering & Correlation Shift
    ├── page_model_performance.py   # Regression Evaluation & Residual Plots
    ├── page_prediction.py      # Real-Time Interactive Prediction Engine
    ├── page_insights.py        # Executive Business Insights
    └── page_about.py           # Project Architecture & Developer Profile
```

---

## 🚀 Installation & Local Execution

### Prerequisites
- Python 3.9+ installed on your system.

### Step-by-Step Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/retail-sales-prediction-dashboard.git
   cd retail-sales-prediction-dashboard
   ```

2. **Create a Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate

   pip install pandas numpy scikit-learn plotly streamlit openpyxl joblib
   ```

3. **(Optional) Run Data Pipeline & Train Model:**
   ```bash
   python generate_data.py
   ```

4. **Launch the Streamlit Dashboard:**
   ```bash
   streamlit run app.py
   ```
   Open your browser and navigate to `http://localhost:8501`.

---

## 📊 Model Performance Summary

| Model | MAE ($) | MSE | RMSE ($) | MAPE | R² Score | Adjusted R² |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Lasso Regression (Best)** | **52.91** | **5480.62** | **74.03** | **0.2468** | **0.9859** | **0.9427** |
| Ridge Regression | 53.61 | 5610.87 | 74.91 | 0.2492 | 0.9855 | 0.9413 |
| Multiple Linear Regression | 54.06 | 5676.83 | 75.34 | 0.2529 | 0.9854 | 0.9406 |
| Elastic Net | 64.70 | 7725.24 | 87.89 | 0.2740 | 0.9801 | 0.9192 |

---

## 👨‍💻 Developer Profile

**Sujal Gupta**  
*Aspiring Data Analyst | Python | SQL | Machine Learning*  

- 📧 Email: sujalgupta.analytics@gmail.com  
- 💼 LinkedIn: [linkedin.com/in/sujal-gupta](https://linkedin.com)  
- 💻 GitHub: [github.com/sujal-gupta](https://github.com)  

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
