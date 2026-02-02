import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import math

# Title and description
st.set_page_config(page_title="Multi-System Horoscope Predictor", layout="wide")
st.title("🔮 Multi-System Horoscope Predictor")
st.markdown("""
Welcome to the ultimate horoscope experience! Enter your birth date and receive personalized predictions
based on multiple divination systems including Chinese Zodiac, Western Astrology, Numerology, and Moon Sign.
""")

# User input section
col1, col2 = st.columns(2)

# Create a list of dates from 100 years ago to today
current_year = datetime.now().year
start_year = current_year - 100
all_dates = [datetime(start_year + i, 1, 1) for i in range(101)]  # 101 years from start_year to current year

# Create a more user-friendly date selection
with col1:
    st.subheader("Birth Information")
    birth_year = st.selectbox("Birth Year", options=range(current_year, start_year - 1, -1), index=25)
    birth_month = st.selectbox("Birth Month", options=range(1, 13), format_func=lambda x: ['January', 'February', 'March', 'April', 'May', 'June', 
                                                                                          'July', 'August', 'September', 'October', 'November', 'December'][x-1])
    
    # Determine the number of days in the selected month
    if birth_month in [1, 3, 5, 7, 8, 10, 12]:
        max_day = 31
    elif birth_month in [4, 6, 9, 11]:
        max_day = 30
    else:  # February
        # Check if it's a leap year
        if (birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0):
            max_day = 29
        else:
            max_day = 28
    
    birth_day = st.selectbox("Birth Day", options=range(1, max_day + 1))

    # Create the birth date from selected components
    try:
        birth_date = datetime(birth_year, birth_month, birth_day).date()
    except ValueError:
        # Handle invalid dates like Feb 29 on non-leap years
        birth_date = datetime(birth_year, 2, 28).date()  # Default to Feb 28

with col2:
    st.markdown("### About Your Birth Date")
    st.write(f"**Selected Date:** {birth_date.strftime('%B %d, %Y')}")
    age = (datetime.now().date() - birth_date).days // 365
    st.write(f"**Approximate Age:** {age} years")

# Calculate astrological information
def get_chinese_zodiac(year):
    animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", 
               "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
    elements = ["Metal", "Water", "Wood", "Fire", "Earth"]  # Cycles every 2 years
    
    animal_index = (year - 4) % 12
    element_index = ((year - 4) // 2) % 5
    
    return animals[animal_index], elements[element_index]

def get_western_sign(month, day):
    signs = [
        (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"),
        (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
        (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
        (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
        (12, 31, "Capricorn")
    ]
    
    for sign_month, sign_day, sign_name in signs:
        if month == sign_month and day <= sign_day:
            return sign_name
        elif month == 12 and day > 22:  # Capricorn spans year boundary
            return "Capricorn"
    
    # Fallback
    return "Capricorn"

def get_life_path_number(birth_date):
    # Calculate life path number from birth date
    total = sum(int(digit) for digit in str(birth_date.year) + 
                str(birth_date.month).zfill(2) + str(birth_date.day).zfill(2))
    
    # Reduce to single digit
    while total > 9 and total not in [11, 22, 33]:  # Master numbers
        total = sum(int(digit) for digit in str(total))
    
    return total

def get_moon_sign(day, month):
    # Simplified moon sign calculation (approximate)
    moon_signs = [
        (1, 20, "Sagittarius"), (2, 19, "Capricorn"), (3, 21, "Aquarius"),
        (4, 20, "Pisces"), (5, 21, "Aries"), (6, 21, "Taurus"),
        (7, 23, "Gemini"), (8, 23, "Cancer"), (9, 23, "Leo"),
        (10, 23, "Virgo"), (11, 22, "Libra"), (12, 22, "Scorpio"),
        (12, 31, "Sagittarius")
    ]
    
    for sign_month, sign_day, sign_name in moon_signs:
        if month == sign_month and day <= sign_day:
            return sign_name
    
    return "Sagittarius"

# Calculate user's astrological data
chinese_animal, chinese_element = get_chinese_zodiac(birth_date.year)
western_sign = get_western_sign(birth_date.month, birth_date.day)
life_path = get_life_path_number(birth_date)
moon_sign = get_moon_sign(birth_date.day, birth_date.month)

# Display calculated information
st.divider()
st.subheader("Your Astrological Profile")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Chinese Zodiac", f"{chinese_animal}\n({chinese_element})", 
           help="Based on your birth year")
col2.metric("Western Sign", western_sign, 
           help="Sun sign based on your birth date")
col3.metric("Life Path", life_path, 
           help="Numerology life path number")
col4.metric("Moon Sign", moon_sign, 
           help="Approximate moon sign")

# Prediction content generation
def generate_daily_prediction(sign, animal, element, life_path_num, moon_sign):
    # General daily themes
    themes = [
        "Love & Relationships", "Career & Finance", "Health & Wellness", 
        "Spiritual Growth", "Adventure & Exploration", "Family & Friends",
        "Creativity & Arts", "Learning & Knowledge", "Travel & Movement", "Rest & Relaxation"
    ]
    
    # Positive and challenging aspects
    positive_aspects = [
        "You'll feel particularly energetic today.",
        "A new opportunity may present itself.",
        "Your intuition is especially strong today.",
        "Financial matters look promising.",
        "Social connections bring joy.",
        "Creative inspiration flows easily.",
        "Physical energy is at its peak.",
        "Mental clarity enhances decision-making.",
        "Unexpected support comes from friends.",
        "Inner peace is easily attainable."
    ]
    
    challenging_aspects = [
        "Patience will be tested in certain situations.",
        "Avoid making hasty financial decisions.",
        "Emotional sensitivity might be heightened.",
        "Communication challenges may arise.",
        "Energy levels might fluctuate.",
        "Overthinking could cloud judgment.",
        "Social interactions require extra patience.",
        "Physical fatigue might set in earlier.",
        "External pressures feel overwhelming.",
        "Conflicting priorities demand attention."
    ]
    
    # Advice based on numerology
    numerology_advice = {
        1: "Take initiative and lead with confidence.",
        2: "Focus on partnerships and collaboration.",
        3: "Express yourself creatively and joyfully.",
        4: "Organize and build solid foundations.",
        5: "Embrace change and new experiences.",
        6: "Nurture relationships and family bonds.",
        7: "Seek solitude for reflection and wisdom.",
        8: "Focus on material success and abundance.",
        9: "Complete old cycles and prepare for renewal.",
        11: "Trust your spiritual intuition today.",
        22: "Large-scale projects may see breakthroughs.",
        33: "Healing and nurturing others brings fulfillment."
    }
    
    theme = random.choice(themes)
    positive = random.choice(positive_aspects)
    challenging = random.choice(challenging_aspects)
    advice = numerology_advice.get(life_path_num, "Pay attention to your inner wisdom.")
    
    return {
        "theme": theme,
        "positive": positive,
        "challenging": challenging,
        "advice": advice
    }

def generate_weekly_prediction(sign, animal, element, life_path_num, moon_sign):
    weekly_themes = [
        "Professional Development", "Relationship Building", "Self-Care Focus",
        "Financial Planning", "Creative Projects", "Learning New Skills",
        "Home & Family Matters", "Health & Fitness", "Spiritual Practice", "Social Activities"
    ]
    
    focus_areas = [
        "Career advancement opportunities may emerge mid-week.",
        "Relationships take center stage, especially with family.",
        "Personal health and wellness deserve attention.",
        "Financial planning and budgeting become crucial.",
        "Creative projects see significant progress.",
        "Learning something new brings satisfaction.",
        "Home improvements or family gatherings occur.",
        "Physical activity enhances mental well-being.",
        "Spiritual practices bring clarity and peace.",
        "Social connections strengthen through shared activities."
    ]
    
    challenges = [
        "Balancing work and personal life requires effort.",
        "Unexpected expenses might arise.",
        "Time management becomes challenging.",
        "Interpersonal conflicts need addressing.",
        "Energy levels fluctuate throughout the week.",
        "Decision-making feels more difficult.",
        "External obligations compete for your time.",
        "Health concerns might surface.",
        "Communication barriers appear with loved ones.",
        "Technology issues disrupt plans."
    ]
    
    theme = random.choice(weekly_themes)
    focus = random.choice(focus_areas)
    challenge = random.choice(challenges)
    
    return {
        "theme": theme,
        "focus": focus,
        "challenge": challenge
    }

def generate_monthly_prediction(sign, animal, element, life_path_num, moon_sign):
    monthly_themes = [
        "Major Life Changes", "Financial Growth", "Relationship Deepening",
        "Career Advancement", "Personal Transformation", "Health Improvements",
        "Travel Opportunities", "Educational Pursuits", "Creative Expression", "Spiritual Awakening"
    ]
    
    opportunities = [
        "A significant opportunity related to your career presents itself.",
        "Financial investments show positive returns.",
        "Relationships deepen and become more meaningful.",
        "Professional recognition comes your way.",
        "Personal growth reaches a new milestone.",
        "Health improvements become noticeable.",
        "Travel opportunities expand your perspective.",
        "Learning new skills proves valuable.",
        "Creative talents receive recognition.",
        "Spiritual understanding deepens significantly."
    ]
    
    cautions = [
        "Avoid impulsive decisions regarding finances.",
        "Be patient with relationship developments.",
        "Don't overcommit to multiple projects.",
        "Maintain balance between work and rest.",
        "Take time for self-care and reflection.",
        "Avoid unnecessary risks in investments.",
        "Prepare thoroughly for travel plans.",
        "Set realistic expectations for learning.",
        "Protect your creative energy from criticism.",
        "Don't force spiritual experiences."
    ]
    
    theme = random.choice(monthly_themes)
    opportunity = random.choice(opportunities)
    caution = random.choice(cautions)
    
    return {
        "theme": theme,
        "opportunity": opportunity,
        "caution": caution
    }

# Generate predictions
daily_pred = generate_daily_prediction(western_sign, chinese_animal, chinese_element, life_path, moon_sign)
weekly_pred = generate_weekly_prediction(western_sign, chinese_animal, chinese_element, life_path, moon_sign)
monthly_pred = generate_monthly_prediction(western_sign, chinese_animal, chinese_element, life_path, moon_sign)

# Display predictions
st.divider()
st.subheader("🔮 Daily Horoscope")
st.markdown(f"**Theme of the Day:** {daily_pred['theme']}")
st.success(f"✨ {daily_pred['positive']}")
st.warning(f"⚠️ {daily_pred['challenging']}")
st.info(f"💡 Numerology Insight: {daily_pred['advice']}")

st.divider()
st.subheader("📅 Weekly Forecast")
st.markdown(f"**Weekly Theme:** {weekly_pred['theme']}")
st.success(f"🎯 Focus Area: {weekly_pred['focus']}")
st.warning(f"⚠️ Potential Challenge: {weekly_pred['challenge']}")

st.divider()
st.subheader("🌙 Monthly Outlook")
st.markdown(f"**Monthly Theme:** {monthly_pred['theme']}")
st.success(f"🌟 Opportunity: {monthly_pred['opportunity']}")
st.warning(f"⚠️ Caution: {monthly_pred['caution']}")

# Personalized recommendations
st.divider()
st.subheader("💎 Personalized Recommendations")

# Based on combination of factors
recommendations = []

if life_path in [1, 8, 9]:
    recommendations.append("Today is perfect for leadership roles and taking charge of projects.")
elif life_path in [2, 6]:
    recommendations.append("Focus on relationships and collaborative efforts.")

if western_sign in ["Aries", "Leo", "Sagittarius"]:
    recommendations.append("Your fiery energy is best channeled into physical activities.")
elif western_sign in ["Cancer", "Scorpio", "Pisces"]:
    recommendations.append("Your intuitive abilities are heightened today.")

if chinese_animal in ["Dragon", "Tiger", "Horse"]:
    recommendations.append("Take bold steps toward your goals - your courage will be rewarded.")
elif chinese_animal in ["Rabbit", "Goat", "Pig"]:
    recommendations.append("Gentle approaches and artistic pursuits will serve you well.")

for rec in recommendations:
    st.markdown(f"- {rec}")

# Footer
st.divider()
st.markdown("*Remember: These predictions are for entertainment purposes. Use them as guidance, not absolute truth.*")