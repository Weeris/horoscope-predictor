import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import math

# Title and description
st.set_page_config(page_title="โปรแกรมทำนายดวงชะตาหลายระบบ", layout="wide")
st.title("🔮 โปรแกรมทำนายดวงชะตาหลายระบบ")
st.markdown("""
ยินดีต้อนรับสู่ประสบการณ์การทำนายดวงชะตาที่สมบูรณ์แบบ! กรุณาใส่วันเกิดของคุณเพื่อรับคำทำนายส่วนบุคคล
โดยใช้ระบบการพยากรณ์หลายแบบรวมถึงราศีจีน โหราศาสตร์ตะวันตก ตัวเลขศาสตร์ และดวงจันทร์
""")

# User input section
col1, col2 = st.columns(2)

# Create a more user-friendly date selection
with col1:
    st.subheader("ข้อมูลวันเกิด")
    current_year = datetime.now().year
    start_year = current_year - 100
    birth_year = st.selectbox("ปีเกิด", options=range(current_year, start_year - 1, -1), index=25)
    birth_month = st.selectbox("เดือนเกิด", options=range(1, 13), format_func=lambda x: ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 
                                                                                          'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'][x-1])
    
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
    
    birth_day = st.selectbox("วันเกิด", options=range(1, max_day + 1))

    # Create the birth date from selected components
    try:
        birth_date = datetime(birth_year, birth_month, birth_day).date()
    except ValueError:
        # Handle invalid dates like Feb 29 on non-leap years
        birth_date = datetime(birth_year, 2, 28).date()  # Default to Feb 28

with col2:
    st.markdown("### เกี่ยวกับวันเกิดของคุณ")
    st.write(f"**วันที่เลือก:** {birth_date.strftime('%d %B พ.ศ. %Y')}")
    age = (datetime.now().date() - birth_date).days // 365
    st.write(f"**อายุโดยประมาณ:** {age} ปี")

# Calculate astrological information
def get_chinese_zodiac(year):
    animals = ["หนู", "วัว", "เสือ", "กระต่าย", "มังกร", "งู", 
               "ม้า", "แพะ", "ลิง", "ไก่", "สุนัข", "หมู"]
    elements = ["โลหะ", "น้ำ", "ไม้", "ไฟ", "ดิน"]  # Cycles every 2 years
    
    animal_index = (year - 4) % 12
    element_index = ((year - 4) // 2) % 5
    
    return animals[animal_index], elements[element_index]

def get_western_sign(month, day):
    signs = [
        (1, 20, "มังกร"), (2, 19, "กุมภ์"), (3, 21, "มีน"),
        (4, 20, "เมษ"), (5, 21, "พฤษภ"), (6, 21, "เมถุน"),
        (7, 23, "กรกฎ"), (8, 23, "สิงห์"), (9, 23, "กันย์"),
        (10, 23, "ตุลย์"), (11, 22, "พิจิก"), (12, 22, "ธนู"),
        (12, 31, "มังกร")
    ]
    
    for sign_month, sign_day, sign_name in signs:
        if month == sign_month and day <= sign_day:
            return sign_name
        elif month == 12 and day > 22:  # Capricorn spans year boundary
            return "มังกร"
    
    # Fallback
    return "มังกร"

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
        (1, 20, "ธนู"), (2, 19, "มังกร"), (3, 21, "กุมภ์"),
        (4, 20, "มีน"), (5, 21, "เมษ"), (6, 21, "พฤษภ"),
        (7, 23, "เมถุน"), (8, 23, "กรกฎ"), (9, 23, "สิงห์"),
        (10, 23, "กันย์"), (11, 22, "ตุลย์"), (12, 22, "พิจิก"),
        (12, 31, "ธนู")
    ]
    
    for sign_month, sign_day, sign_name in moon_signs:
        if month == sign_month and day <= sign_day:
            return sign_name
    
    return "ธนู"

def get_vedic_sign(day, month):
    # Vedic astrology signs
    vedic_signs = [
        (1, 14, "มีน"), (2, 13, "เมษ"), (3, 14, "พฤษภ"), 
        (4, 14, "เมถุน"), (5, 15, "กรกฎ"), (6, 15, "สิงห์"),
        (7, 16, "กันย์"), (8, 16, "ตุลย์"), (9, 16, "พิจิก"),
        (10, 16, "ธนู"), (11, 15, "มังกร"), (12, 15, "กุมภ์"),
        (12, 31, "มีน")
    ]
    
    for sign_month, sign_day, sign_name in vedic_signs:
        if month == sign_month and day <= sign_day:
            return sign_name
    
    return "มีน"

def get_karma_number(day):
    # Karma number based on birth day
    karma_map = {
        1: "ผู้นำ", 2: "ผู้ประสาน", 3: "ผู้สร้างสรรค์", 4: "ผู้ก่อตั้ง", 
        5: "ผู้ผจญภัย", 6: "ผู้ดูแล", 7: "ผู้แสวงหา", 8: "ผู้บริหาร", 
        9: "ผู้เสียสละ", 11: "ผู้บุกเบิก", 22: "ผู้สร้างยิ่งใหญ่"
    }
    return karma_map.get(day, "ผู้เรียนรู้")

def get_penta_number(day):
    # Pentalogy number (derived from day)
    penta_map = {
        1: "อำนาจ", 2: "ความสมดุล", 3: "ความคิดสร้างสรรค์", 4: "เสถียรภาพ", 
        5: "เสรีภาพ", 6: "ความรับผิดชอบ", 7: "ความรู้", 8: "ความมั่งคั่ง", 
        9: "ความเมตตา"
    }
    return penta_map.get(day, "การเรียนรู้")

def get_destiny_number(month):
    # Destiny number based on birth month
    destiny_map = {
        1: "อิสระ", 2: "ความร่วมมือ", 3: "การแสดงออก", 4: "ความมั่นคง", 
        5: "การเปลี่ยนแปลง", 6: "ความรัก", 7: "ปัญญา", 8: "อำนาจ", 
        9: "มนุษยธรรม", 10: "ความสำเร็จ", 11: "ความเชื่อมโยง", 12: "การเสียสละ"
    }
    return destiny_map.get(month, "การเรียนรู้")

# Calculate user's astrological data
chinese_animal, chinese_element = get_chinese_zodiac(birth_date.year)
western_sign = get_western_sign(birth_date.month, birth_date.day)
life_path = get_life_path_number(birth_date)
moon_sign = get_moon_sign(birth_date.day, birth_date.month)
vedic_sign = get_vedic_sign(birth_date.day, birth_date.month)
karma_number = get_karma_number(birth_date.day)
penta_trait = get_penta_number(birth_date.day)
destiny_trait = get_destiny_number(birth_date.month)

# Display calculated information
st.divider()
st.subheader("โพรไฟล์ทางดาราศาสตร์ของคุณ")

col1, col2, col3 = st.columns(3)
col1.metric("ราศีจีน", f"{chinese_animal}\n({chinese_element})", 
           help="จากปีเกิดของคุณ")
col2.metric("ราศีตะวันตก", western_sign, 
           help="ราศีดวงอาทิตย์ตามวันเกิดของคุณ")
col3.metric("เส้นทางชีวิต", life_path, 
           help="ตัวเลขศาสตร์เส้นทางชีวิต")

col4, col5, col6 = st.columns(3)
col4.metric("ราศีจันทร์", moon_sign, 
           help="ราศีจันทร์โดยประมาณ")
col5.metric("ราศีเวทิก", vedic_sign, 
           help="ราศีเวทิกตามวันเกิด")
col6.metric("ตัวเลขธาตุ", penta_trait, 
           help="คุณลักษณะตามธาตุ")

st.divider()
col7, col8, col9 = st.columns(3)
col7.metric("ตัวเลขกรรม", karma_number, 
           help="ลักษณะกรรมตามวันเกิด")
col8.metric("ลักษณะโชคชะตา", destiny_trait, 
           help="ลักษณะโชคชะตาตามเดือนเกิด")
col9.metric("ความหลากหลาย", "9 ศาสตร์", 
           help="จำนวนศาสตร์ที่ใช้ในการทำนาย")

# Prediction content generation
def calculate_accuracy(agreements, total_systems=9):
    """Calculate accuracy percentage based on agreement among systems"""
    return round((agreements / total_systems) * 100, 1)

def generate_categorized_predictions(sign, animal, element, life_path_num, moon_sign, vedic_sign, karma_desc, penta_desc, destiny_desc):
    """Generate predictions categorized by life aspects"""
    
    # Categories with their associated systems
    categories = {
        "การเงิน": {
            "themes": [
                "โอกาสทางการเงินกำลังจะมาถึง",
                "การลงทุนอาจให้ผลตอบแทนที่ดี",
                "ควรระมัดระวังในการใช้จ่าย",
                "มีโอกาสได้รับเงินก้อนโต",
                "ต้องวางแผนการเงินอย่างรอบคอบ"
            ],
            "systems_agreement": 0,
            "total_systems": 9
        },
        "การงาน": {
            "themes": [
                "มีโอกาสเลื่อนตำแหน่งหรือได้งานใหม่",
                "การทำงานเป็นทีมจะประสบความสำเร็จ",
                "ต้องใช้ความพยายามมากขึ้น",
                "ได้รับการยอมรับจากเพื่อนร่วมงาน",
                "อาจมีการเปลี่ยนแปลงในที่ทำงาน"
            ],
            "systems_agreement": 0,
            "total_systems": 9
        },
        "ความรัก": {
            "themes": [
                "ความสัมพันธ์จะมีความหวานชื่น",
                "มีโอกาสได้เจอคู่แท้",
                "ต้องให้ความสำคัญกับคู่รักมากขึ้น",
                "ความรักมีเกณฑ์ดีขึ้นอย่างชัดเจน",
                "อาจมีความขัดแย้งเล็กน้อย"
            ],
            "systems_agreement": 0,
            "total_systems": 9
        },
        "สุขภาพ": {
            "themes": [
                "สุขภาพโดยรวมอยู่ในเกณฑ์ดี",
                "ต้องระวังเรื่องระบบย่อยอาหาร",
                "ควรออกกำลังกายสม่ำเสมอ",
                "สุขภาพจิตต้องได้รับการดูแล",
                "มีเกณฑ์เจ็บป่วยเล็กน้อย"
            ],
            "systems_agreement": 0,
            "total_systems": 9
        },
        "ครอบครัว": {
            "themes": [
                "ความสัมพันธ์ในครอบครัวแน่นแฟ้น",
                "อาจมีเรื่องให้ต้องดูแลครอบครัว",
                "ได้รับข่าวดีจากครอบครัว",
                "ต้องแบ่งเวลาให้ครอบครัวมากขึ้น",
                "อาจมีความขัดแย้งภายในครอบครัว"
            ],
            "systems_agreement": 0,
            "total_systems": 9
        },
        "การศึกษา": {
            "themes": [
                "การเรียนรู้มีความคืบหน้าดี",
                "มีโอกาสได้เรียนรู้สิ่งใหม่ ๆ",
                "ต้องตั้งใจในการเรียนมากขึ้น",
                "ได้รับการยอมรับจากครูอาจารย์",
                "อาจมีอุปสรรคในการเรียน"
            ],
            "systems_agreement": 0,
            "total_systems": 9
        }
    }
    
    # Simulate agreements from different systems
    for category in categories:
        # Random agreement between 4-8 out of 9 systems for variety
        categories[category]["systems_agreement"] = random.randint(4, 8)
        categories[category]["accuracy"] = calculate_accuracy(
            categories[category]["systems_agreement"], 
            categories[category]["total_systems"]
        )
        categories[category]["prediction"] = random.choice(categories[category]["themes"])
    
    return categories

# Generate predictions
predictions = generate_categorized_predictions(
    western_sign, chinese_animal, chinese_element, life_path, 
    moon_sign, vedic_sign, karma_number, penta_trait, destiny_trait
)

# Display predictions by category
st.divider()
st.subheader("🔮 คำทำนายจำแนกตามหมวดหมู่")

# Create columns for each category
cols = st.columns(len(predictions))
categories = list(predictions.keys())

for i, category in enumerate(categories):
    with cols[i]:
        accuracy = predictions[category]["accuracy"]
        pred_text = predictions[category]["prediction"]
        
        # Color code based on accuracy
        if accuracy >= 70:
            st.success(f"**{category}**\n\n{pred_text}\n\n.accuracy: {accuracy}%")
        elif accuracy >= 50:
            st.info(f"**{category}**\n\n{pred_text}\n\n.accuracy: {accuracy}%")
        else:
            st.warning(f"**{category}**\n\n{pred_text}\n\n.accuracy: {accuracy}%")

# Detailed breakdown
st.divider()
st.subheader("📊 รายละเอียดความแม่นยำ")

# Create a dataframe for accuracy display
accuracy_data = []
for category in categories:
    accuracy_data.append({
        "หมวดหมู่": category,
        "คำทำนาย": predictions[category]["prediction"],
        "ความแม่นยำ": f"{predictions[category]['accuracy']}%",
        "ระบบเห็นด้วย": f"{predictions[category]['systems_agreement']}/9"
    })

df = pd.DataFrame(accuracy_data)
st.table(df)

# Additional insights
st.divider()
st.subheader("💎 ข้อมูลเพิ่มเติมจากศาสตร์ต่าง ๆ")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**ราศีเวทิก:** {vedic_sign}")
    st.markdown(f"**ลักษณะกรรม:** {karma_number}")
    st.markdown(f"**ลักษณะโชคชะตา:** {destiny_trait}")

with col2:
    st.markdown(f"**ธาตุประจำตัว:** {penta_trait}")
    st.markdown(f"**จำนวนศาสตร์ที่ใช้:** 9 ศาสตร์")
    st.markdown("**ระบบที่ใช้:** จีน, ตะวันตก, ตัวเลขศาสตร์, ดวงจันทร์, เวทิก, กรรม, ธาตุ, โชคชะตา, ดาวเคราะห์")

# Footer
st.divider()
st.markdown("*โปรดจำไว้ว่า: การทำนายเหล่านี้มีไว้เพื่อความบันเทิง ใช้เป็นแนวทาง ไม่ใช่ความจริงสัมบูรณ์*")