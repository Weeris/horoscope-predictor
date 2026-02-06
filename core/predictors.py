"""
Prediction Generation Module
Handles horoscope predictions based on astrological data
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import random
import hashlib


# ============== Prediction Templates ==============
PREDICTION_TEMPLATES = {
    "th": {
        "financial": [
            "โอกาสทางการเงินกำลังจะมาถึง ควรเตรียมพร้อมรับ",
            "การลงทุนในช่วงนี้อาจให้ผลตอบแทนที่คุ้มค่า",
            "ควรระมัดระวังในการใช้จ่าย หลีกเลี่ยงการฟุ่มเฟือย",
            "มีโอกาสได้รับเงินก้อนจากแหล่งที่ไม่คาดคิด",
            "การวางแผนการเงินอย่างรอบคอบจะนำไปสู่ความมั่งคั่ง",
            "รายได้เสริมอาจมาในช่วงสัปดาห์นี้",
            "ควรหลีกเลี่ยงการลงทุนที่มีความเสี่ยงสูงเกินไป",
        ],
        "career": [
            "มีโอกาสเลื่อนตำแหน่งหรือได้รับความรับผิดชอบมากขึ้น",
            "การทำงานเป็นทีมจะนำมาซึ่งความสำเร็จ",
            "ความพยายามของคุณจะได้รับการยอมรับ",
            "อาจมีโอกาสได้งานใหม่ที่น่าสนใจ",
            "ควรระวังความขัดแย้งกับเพื่อนร่วมงาน",
            "การพัฒนาทักษะใหม่จะเป็นประโยชน์ในอนาคต",
            "ความสำเร็จในหน้าที่การงานกำลังจะมาถึง",
        ],
        "love": [
            "ความสัมพันธ์จะมีความหวานและผูกพันมากขึ้น",
            "มีโอกาสได้เจอคู่แท้หรือคนพิเศษในช่วงนี้",
            "ควรให้ความสำคัญกับคู่รักหรือคนที่รัก",
            "ความรักมีแนวโน้มที่จะดีขึ้นอย่างชัดเจน",
            "อาจมีความขัดแย้งเล็กน้อยกับคนรัก ควรใช้ความอ่อนโยน",
            "การสื่อสารที่ดีจะเสริมความสัมพันธ์ให้แน่นแฟ้น",
            "โชคชะตาเปิดทางให้ความรักมาเยือน",
        ],
        "health": [
            "สุขภาพโดยรวมอยู่ในเกณฑ์ดี ควรรักษาต่อ",
            "ควรระวังเรื่องระบบย่อยอาหารและการนอน",
            "การออกกำลังกายสม่ำเสมอจะช่วยเสริมพลัง",
            "สุขภาพจิตควรได้รับการดูแลอย่างสม่ำเสมอ",
            "ควรพักผ่อนให้เพียงพอ หลีกเลี่ยงความเครียด",
            "มีโอกาสเจ็บป่วยเล็กน้อย ควรระวังสุขภาพ",
        ],
        "family": [
            "ความสัมพันธ์ในครอบครัวจะแน่นแฟ้นมากขึ้น",
            "อาจมีเรื่องให้ต้องดูแลคนในครอบครัว",
            "ได้รับข่าวดีจากครอบครัวหรือญาติ",
            "ควรแบ่งเวลาให้ครอบครัวมากขึ้น",
            "ความเข้าใจกันในครอบครัวจะนำมาซึ่งความสุข",
        ],
        "education": [
            "การเรียนรู้มีความคืบหน้าดี ควรรักษาต่อ",
            "มีโอกาสได้เรียนรู้สิ่งใหม่ที่น่าสนใจ",
            "ความตั้งใจในการเรียนจะนำมาซึ่งความสำเร็จ",
            "ได้รับการยอมรับจากครูอาจารย์",
            "อาจมีอุปสรรคเล็กน้อย แต่จะผ่านไปได้ด้วยดี",
        ],
    },
    "en": {
        "financial": [
            "Financial opportunities are coming your way - be prepared",
            "Investments may yield good returns in the near future",
            "Be cautious with expenses and avoid unnecessary spending",
            "You may receive a significant amount from an unexpected source",
            "Careful financial planning will lead to abundance",
            "Additional income streams may appear this week",
            "Avoid high-risk investments for now",
        ],
        "career": [
            "Opportunity for promotion or increased responsibilities awaits",
            "Teamwork will lead to professional success",
            "Your efforts will be recognized and appreciated",
            "New and exciting job opportunities may arise",
            "Be wary of conflicts with colleagues",
            "Developing new skills will benefit your career",
            "Professional success is within reach",
        ],
        "love": [
            "Relationships will become sweeter and more fulfilling",
            "You may meet someone special very soon",
            "Focus on your partner and nurture your connection",
            "Love prospects are looking increasingly positive",
            "Minor conflicts may arise - respond with kindness",
            "Good communication will strengthen your bonds",
            "Fate opens doors for love to enter your life",
        ],
        "health": [
            "Overall health is good - maintain your wellness routine",
            "Pay attention to digestive health and sleep patterns",
            "Regular exercise will boost your energy levels",
            "Mental wellness deserves your attention and care",
            "Get adequate rest and manage stress levels",
            "Minor health concerns may arise - stay vigilant",
        ],
        "family": [
            "Family relationships will grow stronger and closer",
            "Family matters may require your attention",
            "Good news from relatives or family members expected",
            "Quality time with family will bring joy",
            "Understanding within the family brings happiness",
        ],
        "education": [
            "Learning progress is good - keep up the momentum",
            "Opportunities to learn new and interesting things arise",
            "Your dedication to studies will bring success",
            "Recognition from teachers and mentors is coming",
            "Minor obstacles may appear but will be overcome",
        ],
    },
    "zh": {
        "financial": [
            "财务机会正在向你招手，请做好准备",
            "投资可能在近期带来良好回报",
            "注意支出控制，避免不必要的花费",
            "你可能会从意想不到的来源获得一笔资金",
            "仔细的财务规划将带来财富",
            "本周可能会有额外收入来源",
            "目前应避免高风险投资",
        ],
        "career": [
            "晋升或增加责任的机会正在等着你",
            "团队合作将带来职业上的成功",
            "你的努力将得到认可和欣赏",
            "可能有机会遇到令人兴奋的新工作",
            "注意与同事的冲突",
            "发展新技能将对你的职业生涯有益",
            "职业成功触手可及",
        ],
        "love": [
            "关系将变得更加甜蜜和充实",
            "你可能很快会遇到特别的人",
            "专注于你的伴侣，培养你们的联系",
            "爱情前景越来越光明",
            "可能出现小冲突，以善意回应",
            "良好的沟通将加强你们的联系",
            "命运为爱情打开大门",
        ],
        "health": [
            "整体健康状况良好-保持你的养生习惯",
            "注意消化系统和睡眠模式",
            "定期锻炼将提升你的能量水平",
            "心理健康值得你关注和照顾",
            "获得充足的休息，管理压力水平",
            "可能出现轻微的健康问题-保持警惕",
        ],
        "family": [
            "家庭关系将变得更加牢固和亲密",
            "家庭事务可能需要你关注",
            "期待来自亲戚或家庭成员的好消息",
            "与家人共度美好时光将带来快乐",
            "家庭内的理解带来幸福",
        ],
        "education": [
            "学习进展良好-保持势头",
            "有机会学习新的有趣事物",
            "你对学习的专注将带来成功",
            "老师和新人的认可即将到来",
            "可能出现小障碍，但将会克服",
        ],
    },
}


class PredictionGenerator:
    """Generates personalized horoscope predictions"""
    
    def __init__(self, lang: str = "th"):
        self.lang = lang
        self.templates = PREDICTION_TEMPLATES[lang]
    
    def _get_seed(self, birth_date: datetime, period: str) -> int:
        """Generate consistent seed based on birth date and period"""
        seed_str = f"{birth_date.strftime('%Y%m%d')}_{period}"
        return int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    
    def _get_predictions_for_category(
        self, 
        category: str, 
        birth_date: datetime, 
        period: str,
        num_predictions: int = 3
    ) -> List[str]:
        """Get predictions for a specific category"""
        random.seed(self._get_seed(birth_date, f"{category}_{period}"))
        
        available = self.templates.get(category, self.templates["financial"])
        return random.sample(available, min(num_predictions, len(available)))
    
    def generate_daily_prediction(
        self, 
        astrological_data: Dict,
        birth_date: datetime,
        period: str = "daily"
    ) -> Dict:
        """Generate complete daily prediction"""
        categories = ["financial", "career", "love", "health", "family", "education"]
        
        predictions = {}
        for category in categories:
            predictions[category] = self._get_predictions_for_category(
                category, birth_date, period
            )
        
        # Calculate confidence based on data completeness
        confidence = self._calculate_confidence(astrological_data)
        
        return {
            "predictions": predictions,
            "confidence": confidence,
            "period": period,
            "generated_at": datetime.now().isoformat(),
        }
    
    def _calculate_confidence(self, data: Dict) -> float:
        """Calculate prediction confidence based on available data"""
        # More complete data = higher confidence
        required_keys = [
            "chinese_zodiac", "western_zodiac", "moon_sign", 
            "vedic_zodiac", "numerology"
        ]
        
        present = sum(1 for key in required_keys if key in data)
        return round((present / len(required_keys)) * 100, 1)
    
    def generate_weekly_forecast(self, astrological_data: Dict, birth_date: datetime) -> Dict:
        """Generate weekly forecast"""
        daily_pred = self.generate_daily_prediction(astrological_data, birth_date, "weekly")
        
        # Add weekly-specific insights
        weekly_overview = {
            "th": "สัปดาห์นี้มีพลังแห่งการเปลี่ยนแปลง โชคชะตาเปิดทางให้สิ่งใหม่ๆ",
            "en": "This week brings transformative energy - new opportunities await",
            "zh": "本周带来转变的能量-新机会正在等待",
        }
        
        daily_pred["overview"] = weekly_overview[self.lang]
        daily_pred["period"] = "weekly"
        
        return daily_pred
    
    def generate_monthly_outlook(self, astrological_data: Dict, birth_date: datetime) -> Dict:
        """Generate monthly outlook"""
        daily_pred = self.generate_daily_prediction(astrological_data, birth_date, "monthly")
        
        monthly_overview = {
            "th": "เดือนนี้เหมาะสำหรับการเริ่มต้นสิ่งใหม่ วางแผนอนาคตอย่างรอบคอบ",
            "en": "This month is ideal for new beginnings - plan your future carefully",
            "zh": "这个月是开始新事物理想时机-仔细规划你的未来",
        }
        
        daily_pred["overview"] = monthly_overview[self.lang]
        daily_pred["period"] = "monthly"
        
        return daily_pred
    
    def get_lucky_elements(self, astrological_data: Dict) -> Dict:
        """Get lucky elements for the user"""
        data = astrological_data.get("numerology", {})
        life_path = data.get("life_path", 1)
        
        lucky_data = {
            "th": {
                "numbers": [str(life_path), str(life_path * 2)[:1], str(life_path + 7)[:1]],
                "colors": ["ฟ้า", "เขียว", "ทอง"],
                "days": ["พุธ", "พฤหัสบดี", "ศุกร์"],
            },
            "en": {
                "numbers": [str(life_path), str(life_path * 2)[:1], str(life_path + 7)[:1]],
                "colors": ["Blue", "Green", "Gold"],
                "days": ["Wednesday", "Thursday", "Friday"],
            },
            "zh": {
                "numbers": [str(life_path), str(life_path * 2)[:1], str(life_path + 7)[:1]],
                "colors": ["蓝色", "绿色", "金色"],
                "days": ["周三", "周四", "周五"],
            },
        }
        
        return lucky_data.get(self.lang, lucky_data["en"])
