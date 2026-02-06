"""
Astrological Calculations Module
Handles all astrological sign and calculation computations
"""

from datetime import datetime
from typing import Tuple, Dict, List, Optional
import math


# ============== Zodiac Data ==============
WESTERN_ZODIAC = {
    (1, 20): ("Capricorn", "มู่คัส / กุมภะ"),
    (2, 19): ("Aquarius", "วัวป่า / กุมภะ"),
    (3, 20): ("Pisces", "มีนะ"),
    (4, 20): ("Aries", "เมษะ"),
    (5, 21): ("Taurus", "พฤษภะ"),
    (6, 21): ("Gemini", "มิถุนะ"),
    (7, 23): ("Cancer", "กรกฏะ"),
    (8, 23): ("Leo", "สิงหะ"),
    (9, 23): ("Virgo", "กันยะ"),
    (10, 23): ("Libra", "ตุลยะ"),
    (11, 22): ("Scorpion", "พิจิกะ"),
    (12, 22): ("Sagittarius", "ธนุ"),
    (12, 31): ("Capricorn", "มู่คัส / กุมภะ"),
}

CHINESE_ZODIAC_ANIMALS = {
    0: ("Rat", "หนู"),
    1: ("Ox", "วัว"),
    2: ("Tiger", "เสือ"),
    3: ("Rabbit", "กระต่าย"),
    4: ("Dragon", "มังกร"),
    5: ("Snake", "งู"),
    6: ("Horse", "ม้า"),
    7: ("Goat", "แพะ"),
    8: ("Monkey", "ลิง"),
    9: ("Rooster", "ไก่"),
    10: ("Dog", "สุนัข"),
    11: ("Pig", "หมู"),
}

CHINESE_ELEMENTS = {
    0: ("Metal", "ทอง"),
    1: ("Metal", "ทอง"),
    2: ("Water", "น้ำ"),
    3: ("Water", "น้ำ"),
    4: ("Wood", "ไม้"),
    5: ("Wood", "ไม้"),
    6: ("Fire", "ไฟ"),
    7: ("Fire", "ไฟ"),
    8: ("Earth", "ดิน"),
    9: ("Earth", "ดิน"),
    10: ("Metal", "ทอง"),
    11: ("Metal", "ทอง"),
}

MOON_SIGNS = [
    ("Aries", "เมษะ"),
    ("Taurus", "พฤษภะ"),
    ("Gemini", "มิถุนะ"),
    ("Cancer", "กรกฏะ"),
    ("Leo", "สิงหะ"),
    ("Virgo", "กันยะ"),
    ("Libra", "ตุลยะ"),
    ("Scorpio", "พิจิกะ"),
    ("Sagittarius", "ธนุ"),
    ("Capricorn", "มู่คัส"),
    ("Aquarius", "วัวป่า"),
    ("Pisces", "มีนะ"),
]

VEDIC_SIGNS = [
    ("Mesha", "เมษะ", "Aries"),
    ("Vrishabha", "พฤษภะ", "Taurus"),
    ("Mithuna", "มิถุนะ", "Gemini"),
    ("Karka", "กรกฏะ", "Cancer"),
    ("Simha", "สิงหะ", "Leo"),
    ("Kanya", "กันยะ", "Virgo"),
    ("Tula", "ตุลยะ", "Libra"),
    ("Vrishchika", "พิจิกะ", "Scorpio"),
    ("Dhanus", "ธนุ", "Sagittarius"),
    ("Makara", "มู่คัส", "Capricorn"),
    ("Kumbha", "วัวป่า", "Aquarius"),
    ("Meena", "มีนะ", "Pisces"),
]

NUMEROLOGY_TRAITS = {
    1: ("Independence", "ความเป็นผู้นำ, สร้างสรรค์, กล้าหาญ"),
    2: ("Cooperation", "ความสมดุล, ร่วมมือได้ดี, อ่อนโยน"),
    3: ("Expression", "การสื่อสาร, ความสร้างสรรค์, มีเสน่ห์"),
    4: ("Foundation", "ความมั่นคง, ปฏิบัติได้จริง, ซื่อสัตย์"),
    5: ("Change", "ความเป็นอิสระ, ผจญภัย, ปรับตัวเก่ง"),
    6: ("Harmony", "ความรับผิดชอบ, รักครอบครัว, เมตตา"),
    7: ("Spirituality", "การวิเคราะห์, ลึกลับ, สงบ"),
    8: ("Power", "ความสำเร็จ, อำนาจ, ความมั่งคั่ง"),
    9: ("Humanitarianism", "เมตตากรุณา, ใจกว้าง, เสียสละ"),
}


class AstrologicalCalculator:
    """Main calculator for astrological computations"""
    
    @staticmethod
    def get_western_zodiac(month: int, day: int) -> Tuple[str, str]:
        """Get Western zodiac sign with Thai name"""
        for (m, d), signs in sorted(WESTERN_ZODIAC.items(), key=lambda x: (-x[0][0], -x[0][1])):
            if (month == m and day >= d) or (month > m):
                return signs
        return ("Capricorn", "มู่คัส / กุมภะ")
    
    @staticmethod
    def get_chinese_zodiac(year: int) -> Tuple[str, str, str, str]:
        """Get Chinese zodiac animal, element with Thai names"""
        cycle_year = (year - 4) % 12
        element_cycle = (year - 4) % 10
        
        animal = CHINESE_ZODIAC_ANIMALS[cycle_year]
        element = CHINESE_ELEMENTS[element_cycle]
        
        return (
            animal[0],  # English animal
            animal[1],  # Thai animal
            element[0],  # English element
            element[1],  # Thai element
        )
    
    @staticmethod
    def get_moon_sign(month: int, day: int) -> Tuple[str, str]:
        """Calculate Moon sign based on birth date"""
        # Approximate calculation: Moon changes signs every ~2.5 days
        day_of_year = (month - 1) * 30 + day
        sign_index = int(day_of_year / 2.5) % 12
        return MOON_SIGNS[sign_index]
    
    @staticmethod
    def get_vedic_sign(month: int, day: int) -> Tuple[str, str, str]:
        """Get Vedic (Indian) astrology sign"""
        # Vedic signs are offset from Western by approximately Aries = Mesha
        day_of_year = (month - 1) * 30 + day
        sign_index = int(day_of_year / 30.4) % 12
        return VEDIC_SIGNS[sign_index]
    
    @staticmethod
    def get_life_path_number(day: int, month: int, year: int) -> int:
        """Calculate Life Path Number using Pythagorean method"""
        def reduce_number(n: int) -> int:
            while n > 9 and n not in [11, 22]:
                s = 0
                while n > 0:
                    s += n % 10
                    n //= 10
                n = s
            return n
        
        day_sum = reduce_number(day)
        month_sum = reduce_number(month)
        year_sum = reduce_number(year)
        
        total = day_sum + month_sum + year_sum
        return reduce_number(total)
    
    @staticmethod
    def get_destiny_number(day: int, month: int, year: int) -> int:
        """Calculate Destiny (Expression) Number"""
        # Use Pythagorean numerology for name conversion
        pythagorean = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
            'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
            'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
        }
        return 0  # Placeholder - would need name input
    
    @staticmethod
    def get_karma_number(day: int) -> int:
        """Karma number based on birth day"""
        return day % 9 if day % 9 != 0 else 9
    
    @staticmethod
    def get_soul_urge_number(month: int, day: int) -> int:
        """Soul Urge (Heart's Desire) Number"""
        return AstrologicalCalculator.get_karma_number(month + day)
    
    @staticmethod
    def get_personality_number(day: int) -> int:
        """Personality Number based on birth day"""
        return day % 9 if day % 9 != 0 else 9
    
    @staticmethod
    def get_chinese_element(year: int) -> Tuple[str, str]:
        """Get Chinese Five Element for the year"""
        _, _, _, element = AstrologicalCalculator.get_chinese_zodiac(year)
        return element[0], element[1]
    
    @staticmethod
    def get_buddhist_era(year: int) -> int:
        """Get Buddhist Era year"""
        return year + 543
    
    @staticmethod
    def get_biorhythm(day: int, month: int, year: int) -> Dict[str, float]:
        """Calculate biorhythm cycles (0-100)"""
        birth_date = datetime(year, month, day)
        today = datetime.now()
        days = (today - birth_date).days
        
        # Physical: 23-day cycle
        physical = 50 + 50 * math.sin(2 * math.pi * days / 23)
        # Emotional: 28-day cycle
        emotional = 50 + 50 * math.sin(2 * math.pi * days / 28)
        # Intellectual: 33-day cycle
        intellectual = 50 + 50 * math.sin(2 * math.pi * days / 33)
        
        return {
            "physical": round(physical, 1),
            "emotional": round(emotional, 1),
            "intellectual": round(intellectual, 1),
        }
    
    @staticmethod
    def get_penta_number(day: int) -> str:
        """Get Pentagonal number (Chaldean system)"""
        pentagonal = (day * (3 * day - 1)) // 2
        while pentagonal > 9:
            s = 0
            while pentagonal > 0:
                s += pentagonal % 10
                pentagonal //= 10
            pentagonal = s
        return str(pentagonal)
    
    @staticmethod
    def get_lucky_direction(day: int) -> str:
        """Get lucky direction based on birth day"""
        directions = ["East", "South", "West", "North"]
        return directions[day % 4]
    
    @staticmethod
    def calculate_all(birth_date: datetime) -> Dict:
        """Calculate all astrological data for a birth date"""
        year = birth_date.year
        month = birth_date.month
        day = birth_date.day
        
        chinese_animal_en, chinese_animal_th, chinese_element_en, chinese_element_th = \
            AstrologicalCalculator.get_chinese_zodiac(year)
        
        western_sign_en, western_sign_th = AstrologicalCalculator.get_western_zodiac(month, day)
        
        moon_sign_en, moon_sign_th = AstrologicalCalculator.get_moon_sign(month, day)
        
        vedic_sign_en, vedic_sign_th, vedic_western = AstrologicalCalculator.get_vedic_sign(month, day)
        
        life_path = AstrologicalCalculator.get_life_path_number(day, month, year)
        
        karma = AstrologicalCalculator.get_karma_number(day)
        soul_urge = AstrologicalCalculator.get_soul_urge_number(month, day)
        personality = AstrologicalCalculator.get_personality_number(day)
        
        biorhythm = AstrologicalCalculator.get_biorhythm(day, month, year)
        
        buddhist_year = AstrologicalCalculator.get_buddhist_era(year)
        
        return {
            "birth_date": birth_date.strftime("%Y-%m-%d"),
            "age": (datetime.now() - birth_date).days // 365,
            "chinese_zodiac": {
                "animal_en": chinese_animal_en,
                "animal_th": chinese_animal_th,
                "element_en": chinese_element_en,
                "element_th": chinese_element_th,
            },
            "western_zodiac": {
                "sign_en": western_sign_en,
                "sign_th": western_sign_th,
            },
            "moon_sign": {
                "sign_en": moon_sign_en,
                "sign_th": moon_sign_th,
            },
            "vedic_zodiac": {
                "sign_en": vedic_sign_en,
                "sign_th": vedic_sign_th,
                "western_equivalent": vedic_western,
            },
            "numerology": {
                "life_path": life_path,
                "life_path_traits": NUMEROLOGY_TRAITS[life_path],
                "karma_number": karma,
                "soul_urge": soul_urge,
                "personality": personality,
                "penta_number": AstrologicalCalculator.get_penta_number(day),
            },
            "biorhythm": biorhythm,
            "buddhist_era": buddhist_year,
        }
