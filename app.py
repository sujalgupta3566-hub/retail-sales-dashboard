import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Retail Sales Prediction Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Utilities & Components
from utils import load_datasets, load_ml_artifacts
from components import inject_custom_css, render_footer
from pages.page_overview import show_overview_page
from pages.page_dataset import show_dataset_page
from pages.page_eda import show_eda_page
from pages.page_feature_engineering import show_feature_engineering_page
from pages.page_model_performance import show_model_performance_page
from pages.page_prediction import show_prediction_page
from pages.page_insights import show_business_insights_page
from pages.page_about import show_about_page

# Inject Custom CSS Theme
inject_custom_css()

# Load Cached Data & ML Artifacts
df_raw, df_clean, df_feature = load_datasets()
artifacts = load_ml_artifacts()

menu_options = [
    "Overview",
    "Dataset",
    "Exploratory Data Analysis",
    "Feature Engineering",
    "Model Performance",
    "Prediction",
    "Business Insights",
    "About Project"
]

icons = {
    "Overview": "📊",
    "Dataset": "📁",
    "Exploratory Data Analysis": "📈",
    "Feature Engineering": "⚙️",
    "Model Performance": "🎯",
    "Prediction": "🔮",
    "Business Insights": "💡",
    "About Project": "👨‍💻"
}

if 'nav_page' not in st.session_state:
    st.session_state['nav_page'] = "Overview"

# Callback sync functions
def sync_top_nav():
    st.session_state['nav_page'] = st.session_state['top_nav_widget']
    st.session_state['sidebar_widget'] = f"{icons[st.session_state['nav_page']]} {st.session_state['nav_page']}"

def sync_sidebar_nav():
    choice = st.session_state['sidebar_widget'].split(" ", 1)[1]
    st.session_state['nav_page'] = choice
    st.session_state['top_nav_widget'] = choice

# Initialize widget keys if not present
if 'top_nav_widget' not in st.session_state:
    st.session_state['top_nav_widget'] = st.session_state['nav_page']
if 'sidebar_widget' not in st.session_state:
    st.session_state['sidebar_widget'] = f"{icons[st.session_state['nav_page']]} {st.session_state['nav_page']}"

# Top Navigation Bar (Always Visible)
st.markdown("""
<div style="margin-bottom: 8px;">
    <span style="font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;">Navigation Menu</span>
</div>
""", unsafe_allow_html=True)

st.radio(
    label="Navigation Tabs",
    options=menu_options,
    format_func=lambda x: f"{icons[x]} {x}",
    horizontal=True,
    label_visibility="collapsed",
    key="top_nav_widget",
    on_change=sync_top_nav
)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 16px 0;">
        <div style="font-size: 34px; margin-bottom: 4px;">🛍️</div>
        <div style="font-size: 19px; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Retail Sales</div>
        <div style="font-size: 12px; font-weight: 600; color: #94A3B8; letter-spacing: 0.5px;">PREDICTION DASHBOARD</div>
    </div>
    <hr style="border-color: rgba(99, 102, 241, 0.25); margin-bottom: 16px;">
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: #64748B; letter-spacing: 1px;'>SIDEBAR MENU</p>", unsafe_allow_html=True)
    
    formatted_options = [f"{icons[opt]} {opt}" for opt in menu_options]
    
    st.radio(
        label="Select Page:",
        options=formatted_options,
        label_visibility="collapsed",
        key="sidebar_widget",
        on_change=sync_sidebar_nav
    )
    
    st.markdown("""
    <br>
    <div style="background: rgba(30, 41, 59, 0.6); padding: 12px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2); text-align: center;">
        <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">PORTFOLIO STATUS</div>
        <div style="font-size: 12px; color: #10B981; font-weight: 700; margin-top: 2px;">🟢 Production Ready</div>
        <div style="font-size: 10px; color: #64748B; margin-top: 2px;">Machine Learning & Analytics</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Render active page on-demand
active_page = st.session_state['nav_page']

if active_page == "Overview":
    show_overview_page(df_raw, df_clean, df_feature)
elif active_page == "Dataset":
    show_dataset_page(df_raw, df_clean, df_feature)
elif active_page == "Exploratory Data Analysis":
    show_eda_page(df_clean, df_feature)
elif active_page == "Feature Engineering":
    show_feature_engineering_page(df_clean, df_feature, artifacts)
elif active_page == "Model Performance":
    show_model_performance_page(artifacts)
elif active_page == "Prediction":
    show_prediction_page(artifacts)
elif active_page == "Business Insights":
    show_business_insights_page(df_clean)
elif active_page == "About Project":
    show_about_page()

# Render Footer
render_footer()
