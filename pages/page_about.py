import streamlit as st
from components import render_hero

def show_about_page():
    render_hero(
        title="About Retail Sales Prediction Project",
        subtitle="End-to-End Business Intelligence & Machine Learning solution built for GitHub portfolio & technical recruiter demonstrations.",
        icon="👨‍💻"
    )
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📌 Project Overview")
    st.markdown("""
    This project demonstrates an end-to-end data science and business intelligence pipeline focused on **Retail Sales Analytics and Predictive Modeling**.
    
    The workflow encompasses:
    1. **Data Cleaning & Preprocessing:** Imputation of missing values (median for numerical, mode for categorical), removal of duplicate records, and outlier capping using IQR bounds.
    2. **Exploratory Data Analysis (EDA):** Univariate, bivariate, and multivariate analysis of sales performance, regional demand, store productivity, pricing elasticity, and customer demographics using interactive Plotly charts.
    3. **Feature Engineering:** Extraction of temporal features (`Year`, `Month`, `Weekday`, `IsWeekend`), financial metrics (`Average_Item_Price`, `Discount_Amount`, `Profit_Margin`), and demographic binning (`Age_Group`).
    4. **Machine Learning Modeling:** Comparison of Multiple Linear Regression, Ridge, Lasso, and ElasticNet models with feature scaling and hyperparameter tuning.
    5. **Interactive Streamlit Web App:** recruiter-friendly UI featuring animated metric cards, glassmorphism containers, real-time prediction engine, and actionable business insights.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.subheader("🛠️ Tools & Technologies Used")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🐍</div>
            <div class="kpi-title">Core Language</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Python 3.11</div>
            <div class="kpi-subtitle">Data Wrangling & ML</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-title">Data Analysis</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Pandas & NumPy</div>
            <div class="kpi-subtitle">Transformation & Stats</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-title">Visualization</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Plotly Express</div>
            <div class="kpi-subtitle">Interactive 100% Charts</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🤖</div>
            <div class="kpi-title">Machine Learning</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Scikit-Learn</div>
            <div class="kpi-subtitle">Linear Models & Metrics</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🚀</div>
            <div class="kpi-title">Web Framework</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Streamlit</div>
            <div class="kpi-subtitle">Interactive Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🎨</div>
            <div class="kpi-title">Notebook EDA</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Matplotlib & Seaborn</div>
            <div class="kpi-subtitle">Initial Notebook Analysis</div>
        </div>
        """, unsafe_allow_html=True)
    with col7:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">💾</div>
            <div class="kpi-title">Model Persistence</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Joblib</div>
            <div class="kpi-subtitle">Binary Serialization</div>
        </div>
        """, unsafe_allow_html=True)
    with col8:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📂</div>
            <div class="kpi-title">Data Format</div>
            <div style="font-weight: 700; color: #A5B4FC; font-size: 16px;">Excel & CSV</div>
            <div class="kpi-subtitle">Openpyxl Parser</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(99, 102, 241, 0.2);'><br>", unsafe_allow_html=True)
    
    st.subheader("👨‍💻 Developer Profile")
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);">
        <div style="font-size: 24px; font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">Sujal Gupta</div>
        <div style="font-size: 16px; font-weight: 600; color: #A855F7; margin-bottom: 12px;">Aspiring Data Analyst &nbsp;|&nbsp; Python &nbsp;|&nbsp; SQL &nbsp;|&nbsp; Machine Learning</div>
        <p style="color: #CBD5E1; font-size: 14px; line-height: 1.6; margin-bottom: 16px;">
            Passionate data analyst skilled in building interactive business intelligence dashboards, predictive machine learning models, statistical data analysis, and SQL query optimization. Dedicated to turning raw operational data into clear, actionable business strategies.
        </p>
        <div style="display: flex; gap: 12px;">
            <span class="kpi-badge" style="font-size: 13px; padding: 6px 14px;">💻 GitHub Portfolio</span>
            <span class="kpi-badge" style="font-size: 13px; padding: 6px 14px;">🔗 LinkedIn Profile</span>
            <span class="kpi-badge" style="font-size: 13px; padding: 6px 14px;">✉️ Open to Opportunities</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
