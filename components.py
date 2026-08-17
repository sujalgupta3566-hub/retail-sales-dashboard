import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* Google Fonts & Universal Emoji Support */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', -apple-system, sans-serif;
        color: #F8FAFC;
    }
    
    /* Main App Dark Gradient Background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(49, 36, 107, 0.7) 0%, rgba(15, 23, 42, 0.98) 55%, rgba(9, 13, 22, 1) 100%);
        background-attachment: fixed;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.6);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.4);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(168, 85, 247, 0.7);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(99, 102, 241, 0.25);
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
        font-size: 14px;
        color: #CBD5E1;
        padding: 10px 14px;
        border-radius: 10px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2px;
    }
    
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(139, 92, 246, 0.18);
        color: #E0E7FF;
        transform: translateX(4px);
    }
    
    /* Top Navigation Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(15, 23, 42, 0.75);
        padding: 8px 12px;
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.25);
        backdrop-filter: blur(16px);
        margin-bottom: 24px;
        flex-wrap: wrap;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre;
        border-radius: 12px;
        font-weight: 700;
        font-size: 13.5px;
        color: #94A3B8;
        padding: 0px 18px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #E0E7FF;
        background: rgba(99, 102, 241, 0.15);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.45) 0%, rgba(139, 92, 246, 0.45) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(168, 85, 247, 0.6) !important;
        box-shadow: 0 4px 18px rgba(99, 102, 241, 0.35);
    }
    
    /* Glassmorphism Metric Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 18px;
        padding: 24px 20px;
        box-shadow: 0 12px 35px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(16px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899, #06B6D4);
        opacity: 0.85;
    }
    
    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 22px 45px -12px rgba(139, 92, 246, 0.45);
        border-color: rgba(168, 85, 247, 0.65);
    }
    
    .kpi-icon {
        font-size: 30px;
        margin-bottom: 8px;
        display: inline-block;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif;
    }
    
    .kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 30%, #C7D2FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .kpi-subtitle {
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
    }
    
    .kpi-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        background: rgba(99, 102, 241, 0.2);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.4);
        margin-top: 8px;
    }

    /* Section Cards & Glass Panels */
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 18px;
        padding: 26px;
        margin-bottom: 24px;
        box-shadow: 0 10px 35px 0 rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(14px);
    }
    
    .hero-banner {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.3) 0%, rgba(147, 51, 234, 0.3) 50%, rgba(236, 72, 153, 0.2) 100%);
        border: 1px solid rgba(168, 85, 247, 0.45);
        border-radius: 22px;
        padding: 28px 32px;
        margin-bottom: 26px;
        backdrop-filter: blur(20px);
        box-shadow: 0 15px 45px -10px rgba(99, 102, 241, 0.35);
    }
    
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #E0E7FF 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .hero-subtitle {
        font-size: 15px;
        color: #CBD5E1;
        font-weight: 400;
        line-height: 1.6;
    }

    /* Business Insight Card */
    .insight-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.88) 100%);
        border-left: 4px solid #8B5CF6;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        transition: all 0.35s ease;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    }
    
    .insight-card:hover {
        transform: translateX(8px);
        border-left-color: #EC4899;
        box-shadow: 0 12px 35px rgba(168, 85, 247, 0.25);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.98) 100%);
    }

    /* Custom Footer */
    .custom-footer {
        margin-top: 60px;
        padding: 28px;
        text-align: center;
        border-top: 1px solid rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(9, 13, 22, 0.95) 100%);
        border-radius: 18px;
        backdrop-filter: blur(16px);
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .footer-text {
        font-size: 16px;
        font-weight: 800;
        background: linear-gradient(90deg, #818CF8, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    
    .footer-sub {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 600;
        letter-spacing: 0.4px;
    }
    
    /* Streamlit Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 14px 30px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 10px 30px -5px rgba(99, 102, 241, 0.6) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
        cursor: pointer;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 15px 40px -5px rgba(139, 92, 246, 0.8) !important;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    }
    
    /* Hide Streamlit Default Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def render_kpi_card(title, value, subtitle, icon="📊", badge=""):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
        {f'<div class="kpi-badge">{badge}</div>' if badge else ''}
    </div>
    """, unsafe_allow_html=True)

def render_hero(title, subtitle, icon="🚀"):
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title"><span>{icon}</span> <span>{title}</span></div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="custom-footer">
        <div class="footer-text">Created by Sujal Gupta</div>
        <div class="footer-sub">Aspiring Data Analyst &nbsp;|&nbsp; Python &nbsp;|&nbsp; SQL &nbsp;|&nbsp; Machine Learning</div>
    </div>
    """, unsafe_allow_html=True)
