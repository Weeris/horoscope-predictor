"""
🔮 Horoscope Predictor - Main Application
A comprehensive multi-system horoscope application with beautiful UI
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any

# Import our core modules
from core import AstrologicalCalculator, PredictionGenerator
from utils.language import UI_TEXTS, LANGUAGES, get_text


# ============== Page Configuration ==============
st.set_page_config(
    page_title="🔮 Horoscope Predictor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============== Custom CSS for Beautiful UI ==============
def load_custom_css():
    """Load custom CSS for styling"""
    st.markdown("""
    <style>
    /* Main gradient background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #2d2d44 0%, #1a1a2e 100%);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Prediction cards */
    .prediction-card {
        background: linear-gradient(145deg, #1e3a5f 0%, #16213e 100%);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border-left: 4px solid;
    }
    
    .prediction-financial { border-left-color: #00C853; }
    .prediction-career { border-left-color: #2196F3; }
    .prediction-love { border-left-color: #E91E63; }
    .prediction-health { border-left-color: #FF9800; }
    .prediction-family { border-left-color: #9C27B0; }
    .prediction-education { border-left-color: #00BCD4; }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Text colors */
    .stMarkdown, .stText {
        color: #e0e0e0 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Date input */
    .stDateInput > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 8px 16px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* Zodiac icons */
    .zodiac-icon {
        font-size: 48px;
        margin-bottom: 8px;
    }
    
    /* Lucky colors grid */
    .lucky-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }
    
    .lucky-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


# ============== Helper Functions ==============
def get_zodiac_icon(sign: str) -> str:
    """Get emoji icon for zodiac sign"""
    icons = {
        "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
        "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
        "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓",
        "Rat": "🐀", "Ox": "🐂", "Tiger": "🐅", "Rabbit": "🐇",
        "Dragon": "🐉", "Snake": "🐍", "Horse": "🐎", "Goat": "🐐",
        "Monkey": "🐒", "Rooster": "🐓", "Dog": "🐕", "Pig": "🐖",
    }
    return icons.get(sign, "✨")


# ============== Main Application ==============
def main():
    """Main application function"""
    load_custom_css()
    
    # Session state
    if 'language' not in st.session_state:
        st.session_state.language = 'th'
    if 'birth_date' not in st.session_state:
        st.session_state.birth_date = None
    if 'astrological_data' not in st.session_state:
        st.session_state.astrological_data = None
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None
    
    # Language selector
    cols = st.columns([1, 6, 1])
    with cols[0]:
        lang_options = {k: f"{v['flag']} {v['name']}" for k, v in LANGUAGES.items()}
        selected_lang = st.selectbox(
            "🌐",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: lang_options[x],
            index=['th', 'en', 'zh'].index(st.session_state.language),
            key='lang_selector'
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
    
    texts = UI_TEXTS[st.session_state.language]
    
    # ============== Hero Section ==============
    st.markdown(f"""
    <div class="fade-in" style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 48px; margin-bottom: 16px;">{texts['title']}</h1>
        <p style="font-size: 20px; opacity: 0.8;">{texts['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============== Birth Date Input Section ==============
    st.subheader(f"📅 {texts['select_date']}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Date input
        birth_date = st.date_input(
            "",
            value=datetime(1990, 1, 1),
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now(),
            key='birth_date_input'
        )
        
        # Calculate button
        if st.button(f"🔮 {texts['calculate']}", use_container_width=True):
            st.session_state.birth_date = birth_date
            st.session_state.astrological_data = AstrologicalCalculator.calculate_all(
                datetime.combine(birth_date, datetime.min.time())
            )
            st.session_state.prediction = None
            st.rerun()
    
    # ============== Results Section ==============
    if st.session_state.astrological_data:
        data = st.session_state.astrological_data
        birth_date = st.session_state.birth_date
        
        st.markdown("---")
        
        # ============== Astrological Profile ==============
        st.subheader(f"✨ {texts['astro_info']}")
        
        # Calculate age
        age = data.get("age", 0)
        birth_display = birth_date.strftime("%d %B %Y")
        
        st.info(f"📆 {birth_display} | 🗓️ {age} {texts['life_path'].lower()}")
        
        # Create metrics grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="zodiac-icon">{get_zodiac_icon(data['western_zodiac']['sign_en'])}</div>
                <div style="font-size: 14px;">{texts['western_zodiac']}</div>
                <div style="font-size: 18px; font-weight: bold;">{data['western_zodiac']['sign_th']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            cz = data['chinese_zodiac']
            st.markdown(f"""
            <div class="metric-card">
                <div class="zodiac-icon">{get_zodiac_icon(cz['animal_en'])}</div>
                <div style="font-size: 14px;">{texts['chinese_zodiac']}</div>
                <div style="font-size: 18px; font-weight: bold;">{cz['animal_th']}</div>
                <div style="font-size: 12px; opacity: 0.8;">{cz['element_th']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            ms = data['moon_sign']
            st.markdown(f"""
            <div class="metric-card">
                <div class="zodiac-icon">🌙</div>
                <div style="font-size: 14px;">{texts['moon_sign']}</div>
                <div style="font-size: 18px; font-weight: bold;">{ms['sign_th']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            vs = data['vedic_zodiac']
            st.markdown(f"""
            <div class="metric-card">
                <div class="zodiac-icon">🕉️</div>
                <div style="font-size: 14px;">{texts['vedic_zodiac']}</div>
                <div style="font-size: 18px; font-weight: bold;">{vs['sign_th']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ============== Numerology Section ==============
        st.subheader(f"🔢 {texts['numerology']}")
        
        num = data['numerology']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(texts['life_path'], num['life_path'])
            st.caption(num['life_path_traits'][1])
        
        with col2:
            st.metric("Karma Number", num['karma_number'])
        
        with col3:
            st.metric("Soul Urge", num['soul_urge'])
        
        with col4:
            st.metric("Penta Number", num['penta_number'])
        
        st.markdown("---")
        
        # ============== Biorhythm Section ==============
        st.subheader("🧬 Biorhythm")
        
        bio = data['biorhythm']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.progress(bio['physical'] / 100)
            st.caption(f"🧘 Physical: {bio['physical']}%")
        
        with col2:
            st.progress(bio['emotional'] / 100)
            st.caption(f"💚 Emotional: {bio['emotional']}%")
        
        with col3:
            st.progress(bio['intellectual'] / 100)
            st.caption(f"🧠 Intellectual: {bio['intellectual']}%")
        
        st.markdown("---")
        
        # ============== Predictions Section ==============
        st.subheader(f"📿 {texts['predictions']}")
        
        # Period selector
        period_cols = st.columns(3)
        with period_cols[0]:
            period = st.radio(
                texts['select_period'],
                options=['daily', 'weekly', 'monthly'],
                format_func=lambda x: {
                    'daily': f"📅 {texts['daily']}",
                    'weekly': f"📆 {texts['weekly']}",
                    'monthly': f"🗓️ {texts['monthly']}",
                }[x],
                horizontal=True
            )
        
        # Generate prediction
        if st.session_state.prediction is None or st.session_state.prediction.get('period') != period:
            predictor = PredictionGenerator(st.session_state.language)
            
            if period == 'daily':
                st.session_state.prediction = predictor.generate_daily_prediction(
                    data, datetime.combine(birth_date, datetime.min.time())
                )
            elif period == 'weekly':
                st.session_state.prediction = predictor.generate_weekly_forecast(
                    data, datetime.combine(birth_date, datetime.min.time())
                )
            else:
                st.session_state.prediction = predictor.generate_monthly_outlook(
                    data, datetime.combine(birth_date, datetime.min.time())
                )
        
        prediction = st.session_state.prediction
        
        # Overview
        if 'overview' in prediction:
            st.markdown(f"""
            <div class="card" style="text-align: center; font-size: 18px;">
                {prediction['overview']}
            </div>
            """, unsafe_allow_html=True)
        
        # Category predictions
        categories = [
            ('financial', texts['financial'], '💰'),
            ('career', texts['career'], '💼'),
            ('love', texts['love'], '❤️'),
            ('health', texts['health'], '🏥'),
            ('family', texts['family'], '👨‍👩‍👧'),
            ('education', texts['education'], '📚'),
        ]
        
        for cat_key, cat_name, cat_icon in categories:
            if cat_key in prediction['predictions']:
                st.markdown(f"""
                <div class="prediction-card prediction-{cat_key}">
                    <h4 style="margin: 0 0 12px 0;">{cat_icon} {cat_name}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for pred in prediction['predictions'][cat_key]:
                    st.markdown(f"• {pred}")
                
                st.markdown("")
        
        # ============== Lucky Elements ==============
        st.markdown("---")
        st.subheader(f"{texts['lucky']}")
        
        predictor = PredictionGenerator(st.session_state.language)
        lucky = predictor.get_lucky_elements(data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("🎯 **Numbers**")
            st.write(", ".join(lucky['numbers']))
        
        with col2:
            st.markdown("🎨 **Colors**")
            st.write(", ".join(lucky['colors']))
        
        with col3:
            st.markdown("📅 **Lucky Days**")
            st.write(", ".join(lucky['days']))
        
        # ============== Disclaimer ==============
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; opacity: 0.6; font-size: 12px;">
            {texts['disclaimer']}
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
