"""
utils/styling.py
Custom CSS and styling for the Streamlit Career Intelligence App.
"""

import streamlit as st


def apply_custom_css():
    """Inject custom CSS into the Streamlit app."""
    st.markdown("""
    <style>
    /* ── Google Font ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ──────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Hide default Streamlit header/footer ────────────────── */
    #MainMenu  { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }

    /* ── Main container ──────────────────────────────────────── */
    .main .block-container {
        padding-top:    1.5rem;
        padding-bottom: 2rem;
        max-width:      1200px;
    }

    /* ── App title ───────────────────────────────────────────── */
    h1 {
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }

    /* ── Section headings ────────────────────────────────────── */
    h2 { color: #1F2937 !important; font-weight: 600 !important; }
    h3 { color: #374151 !important; font-weight: 600 !important; }
    h4 { color: #4B5563 !important; font-weight: 500 !important; }

    /* ── Cards / containers ──────────────────────────────────── */
    .stExpander {
        border:        1px solid #E5E7EB !important;
        border-radius: 10px !important;
        margin-bottom: 0.75rem !important;
    }

    /* ── Metric cards ────────────────────────────────────────── */
    [data-testid="metric-container"] {
        background:    #F9FAFB;
        border:        1px solid #E5E7EB;
        border-radius: 12px;
        padding:       1rem 1.25rem;
        box-shadow:    0 1px 3px rgba(0,0,0,0.06);
    }

    [data-testid="stMetricValue"] {
        font-size:   1.6rem !important;
        font-weight: 700    !important;
        color:       #4F46E5!important;
    }

    /* ── Primary button ──────────────────────────────────────── */
    .stButton > button[kind="primary"] {
        background:    linear-gradient(135deg, #4F46E5, #7C3AED) !important;
        color:         white !important;
        border:        none  !important;
        border-radius: 8px   !important;
        padding:       0.75rem 2rem !important;
        font-size:     1rem  !important;
        font-weight:   600   !important;
        box-shadow:    0 4px 15px rgba(79,70,229,0.4) !important;
        transition:    all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform:  translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79,70,229,0.5) !important;
    }

    /* ── Secondary button ────────────────────────────────────── */
    .stButton > button[kind="secondary"] {
        border:        2px solid #4F46E5 !important;
        color:         #4F46E5 !important;
        border-radius: 8px !important;
        font-weight:   600 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #EEF2FF !important;
    }

    /* ── Form inputs ─────────────────────────────────────────── */
    .stTextInput  > div > div > input,
    .stSelectbox  > div > div > div {
        border-radius: 8px   !important;
        border:        1.5px solid #D1D5DB !important;
        font-size:     0.95rem !important;
    }
    .stTextInput  > div > div > input:focus,
    .stSelectbox  > div > div > div:focus {
        border-color: #4F46E5 !important;
        box-shadow:   0 0 0 3px rgba(79,70,229,0.15) !important;
    }

    /* ── Tabs ────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap:           8px !important;
        border-bottom: 2px solid #E5E7EB !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0 !important;
        font-weight:   500 !important;
        color:         #6B7280 !important;
    }
    .stTabs [aria-selected="true"] {
        color:        #4F46E5 !important;
        border-color: #4F46E5 !important;
    }

    /* ── Success / warning / error boxes ─────────────────────── */
    .stSuccess {
        border-left:   4px solid #10B981 !important;
        border-radius: 0 8px 8px 0 !important;
    }
    .stWarning {
        border-left:   4px solid #F59E0B !important;
        border-radius: 0 8px 8px 0 !important;
    }
    .stError {
        border-left:   4px solid #EF4444 !important;
        border-radius: 0 8px 8px 0 !important;
    }

    /* ── Sidebar ─────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1B4B 0%, #312E81 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: #E5E7EB !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    /* ── Dataframe ────────────────────────────────────────────── */
    .stDataFrame {
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* ── Progress bar ────────────────────────────────────────── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    }

    /* ── Info box ────────────────────────────────────────────── */
    .stInfo {
        border-left:   4px solid #4F46E5 !important;
        border-radius: 0 8px 8px 0 !important;
    }

    /* ── Horizontal divider ──────────────────────────────────── */
    hr {
        border-color: #E5E7EB !important;
        margin: 1.5rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
