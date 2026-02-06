"""
Language and Localization Utilities
"""

from typing import Dict, Any

# ============== Language Configuration ==============
LANGUAGES = {
    'th': {
        'code': 'th',
        'name': 'ไทย',
        'name_en': 'Thai',
        'flag': '🇹🇭',
    },
    'en': {
        'code': 'en',
        'name': 'English',
        'name_en': 'English',
        'flag': '🇺🇸',
    },
    'zh': {
        'code': 'zh',
        'name': '中文',
        'name_en': 'Chinese',
        'flag': '🇨🇳',
    },
}


# ============== UI Texts ==============
UI_TEXTS = {
    'th': {
        'title': '🔮 ทำนายดวงชะตา',
        'subtitle': 'ระบบทำนายดวงชะตาครบวงจรจากหลายศาสตร์',
        'birth_info': '📅 ข้อมูลวันเกิด',
        'select_date': 'เลือกวันเกิดของคุณ',
        'calculate': '🔮 ดูดวง',
        'astro_info': '✨ ข้อมูลดวงของคุณ',
        'predictions': '📿 คำทำนาย',
        'select_period': 'เลือกช่วงเวลา:',
        'daily': 'รายวัน',
        'weekly': 'รายสัปดาห์',
        'monthly': 'รายเดือน',
        'lucky': '🍀 เลขและสีมงคล',
        'disclaimer': '⚠️ การทำนายเหล่านี้มีไว้เพื่อความบันเทิงและเป็นแนวทางเท่านั้น',
        'western_zodiac': 'ราศีตะวันตก',
        'chinese_zodiac': 'ราศีจีน',
        'moon_sign': 'ราศีจันทร์',
        'vedic_zodiac': 'ราศีเวทิก',
        'numerology': 'ศาสตร์ตัวเลข',
        'life_path': 'เส้นทางชีวิต',
        'financial': '💰 การเงิน',
        'career': '💼 การงาน',
        'love': '❤️ ความรัก',
        'health': '🏥 สุขภาพ',
        'family': '👨‍👩‍👧 ครอบครัว',
        'education': '📚 การศึกษา',
    },
    'en': {
        'title': '🔮 Horoscope Predictor',
        'subtitle': 'Complete horoscope system from multiple traditions',
        'birth_info': '📅 Birth Information',
        'select_date': 'Select your birth date',
        'calculate': '🔮 Get Prediction',
        'astro_info': '✨ Your Astrological Profile',
        'predictions': '📿 Predictions',
        'select_period': 'Select time period:',
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'lucky': '🍀 Lucky Numbers & Colors',
        'disclaimer': '⚠️ These predictions are for entertainment and guidance only',
        'western_zodiac': 'Western Zodiac',
        'chinese_zodiac': 'Chinese Zodiac',
        'moon_sign': 'Moon Sign',
        'vedic_zodiac': 'Vedic Zodiac',
        'numerology': 'Numerology',
        'life_path': 'Life Path',
        'financial': '💰 Financial',
        'career': '💼 Career',
        'love': '❤️ Love',
        'health': '🏥 Health',
        'family': '👨‍👩‍👧 Family',
        'education': '📚 Education',
    },
    'zh': {
        'title': '🔮 星座预测',
        'subtitle': '来自多种传统的完整星座系统',
        'birth_info': '📅 出生信息',
        'select_date': '选择您的出生日期',
        'calculate': '🔮 获取预测',
        'astro_info': '✨ 您的星座信息',
        'predictions': '📿 预测',
        'select_period': '选择时间段：',
        'daily': '每日',
        'weekly': '每周',
        'monthly': '每月',
        'lucky': '🍀 幸运数字和颜色',
        'disclaimer': '⚠️ 这些预测仅供娱乐和指导',
        'western_zodiac': '西方星座',
        'chinese_zodiac': '生肖',
        'moon_sign': '月亮星座',
        'vedic_zodiac': '吠陀星座',
        'numerology': '命理学',
        'life_path': '生命路径',
        'financial': '💰 财务',
        'career': '💼 事业',
        'love': '❤️ 爱情',
        'health': '🏥 健康',
        'family': '👨‍👩‍👧 家庭',
        'education': '📚 教育',
    },
}


def get_text(key: str, lang: str = 'th') -> str:
    """Get translated text by key"""
    return UI_TEXTS.get(lang, UI_TEXTS['en']).get(key, UI_TEXTS['en'].get(key, key))


def get_supported_languages() -> Dict[str, Dict]:
    """Get list of supported languages"""
    return LANGUAGES
