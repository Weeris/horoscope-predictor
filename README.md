# 🔮 Multi-System Horoscope Predictor

A comprehensive horoscope application combining multiple divination systems with a beautiful, modern interface.

## ✨ Features

### Multiple Divination Systems
- **Western Astrology** - Sun sign based on birth date
- **Chinese Zodiac** - Year of birth animal and element
- **Moon Sign** - Lunar position at birth
- **Vedic Astrology** - Indian sidereal zodiac
- **Numerology** - Life Path, Karma, Soul Urge numbers
- **Biorhythm** - Physical, Emotional, Intellectual cycles

### Prediction Types
- **Daily Horoscope** - Daily guidance and insights
- **Weekly Forecast** - Week-ahead overview
- **Monthly Outlook** - Month-long predictions

### Lucky Elements
- Lucky numbers based on birth data
- Auspicious colors
- Fortunate days

## 🚀 Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

## 🌐 Supported Languages

- 🇹🇭 **ไทย (Thai)**
- 🇺🇸 **English**
- 🇨🇳 **中文 (Chinese)**

## 📁 Project Structure

```
horoscope_predictor/
├── app.py                 # Main Streamlit application
├── core/
│   ├── __init__.py
│   ├── calculators.py     # Astrological calculations
│   └── predictors.py      # Prediction generation
├── utils/
│   ├── __init__.py
│   └── language.py       # Multi-language support
├── data/                  # Data files (future)
├── tests/                 # Unit tests (future)
└── requirements.txt       # Dependencies
```

## 🔧 Technical Details

- **Frontend**: Streamlit
- **Calculations**: Custom Python algorithms
- **Styling**: Custom CSS with animations
- **Languages**: Thai, English, Chinese

## 📝 Disclaimer

This application is for **entertainment purposes only**. Predictions are generated based on astrological traditions and should not be used as the sole basis for important life decisions.

## 📄 License

MIT License

---

Built with ❤️ using Streamlit
