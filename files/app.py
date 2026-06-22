# app.py
# Rice Climate Risk & Precision Farming Assistant — Web Version
# Run with: streamlit run app.py

import streamlit as st
from datetime import datetime
from climate_analyzer import full_climate_report
from harvest_optimizer import recommend_sowing_date, recommend_harvest_date, estimate_yield

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Rice Farming Assistant",
    page_icon="🌾",
    layout="centered"
)

# ─────────────────────────────────────────────
# LANGUAGE TEXT (English / Tamil)
# ─────────────────────────────────────────────
TEXT = {
    "English": {
        "title": "🌾 Rice Climate Risk & Farming Assistant",
        "subtitle": "Get AI-powered recommendations on when to sow and harvest your rice crop.",
        "rainfall": "Average Monthly Rainfall (mm)",
        "temperature": "Current Temperature (°C)",
        "humidity": "Humidity (%)",
        "soil": "Soil Type",
        "variety": "Rice Variety",
        "button": "🔍 Get Recommendation",
        "results_header": "📊 Your Results",
        "risk_level": "Overall Risk Level",
        "sow_date": "Recommended Sowing Date",
        "harvest_date": "Recommended Harvest Date",
        "yield_label": "Estimated Yield",
        "quality_label": "Yield Quality",
        "details_header": "🔍 Detailed Climate Analysis",
        "footer": "Built for farmers 🇮🇳 | Rule-based AI — no internet weather data required",
    },
    "தமிழ்": {
        "title": "🌾 நெல் வானிலை ஆபத்து மற்றும் விவசாய உதவியாளர்",
        "subtitle": "உங்கள் நெல் பயிரை எப்போது விதைக்க, அறுவடை செய்ய வேண்டும் என்பதற்கான AI பரிந்துரைகளைப் பெறுங்கள்.",
        "rainfall": "மாத சராசரி மழைப்பொழிவு (மிமீ)",
        "temperature": "தற்போதைய வெப்பநிலை (°C)",
        "humidity": "ஈரப்பதம் (%)",
        "soil": "மண் வகை",
        "variety": "நெல் வகை",
        "button": "🔍 பரிந்துரையைப் பெறுக",
        "results_header": "📊 உங்கள் முடிவுகள்",
        "risk_level": "ஒட்டுமொத்த ஆபத்து நிலை",
        "sow_date": "பரிந்துரைக்கப்பட்ட விதைப்பு தேதி",
        "harvest_date": "பரிந்துரைக்கப்பட்ட அறுவடை தேதி",
        "yield_label": "மதிப்பிடப்பட்ட விளைச்சல்",
        "quality_label": "விளைச்சல் தரம்",
        "details_header": "🔍 விரிவான வானிலை பகுப்பாய்வு",
        "footer": "விவசாயிகளுக்காக கட்டப்பட்டது 🇮🇳 | விதி-அடிப்படையிலான AI — இணைய வானிலை தரவு தேவையில்லை",
    }
}

SOIL_OPTIONS = {
    "English": ["Clay", "Loam", "Sandy Loam", "Sandy", "Silt"],
    "தமிழ்": ["களிமண்", "வண்டல் மண்", "மணல் வண்டல் மண்", "மணல்", "சிற்றளுள் மண்"]
}
SOIL_MAP = ["clay", "loam", "sandy_loam", "sandy", "silt"]  # backend values, same order

VARIETY_OPTIONS = {
    "English": ["Short (~105 days)", "Medium (~120 days)", "Long (~150 days)"],
    "தமிழ்": ["குறுகிய (~105 நாட்கள்)", "நடுத்தர (~120 நாட்கள்)", "நீண்ட (~150 நாட்கள்)"]
}
VARIETY_MAP = ["short", "medium", "long"]  # backend values, same order

RISK_COLORS = {
    "NO RISK": "🟢", "LOW RISK": "🟡", "MEDIUM RISK": "🟠", "HIGH RISK": "🔴"
}

# ─────────────────────────────────────────────
# LANGUAGE TOGGLE (sidebar)
# ─────────────────────────────────────────────
with st.sidebar:
    lang = st.radio("🌐 Language / மொழி", ["English", "தமிழ்"])

t = TEXT[lang]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title(t["title"])
st.write(t["subtitle"])
st.divider()

# ─────────────────────────────────────────────
# INPUT FORM
# ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    rainfall = st.slider(t["rainfall"], min_value=0, max_value=400, value=150)
    temperature = st.slider(t["temperature"], min_value=10, max_value=45, value=28)

with col2:
    humidity = st.slider(t["humidity"], min_value=20, max_value=100, value=75)
    soil_label = st.selectbox(t["soil"], SOIL_OPTIONS[lang])

variety_label = st.selectbox(t["variety"], VARIETY_OPTIONS[lang])

# Map selected labels back to backend values
soil_type = SOIL_MAP[SOIL_OPTIONS[lang].index(soil_label)]
variety = VARIETY_MAP[VARIETY_OPTIONS[lang].index(variety_label)]

st.write("")
calculate = st.button(t["button"], type="primary", use_container_width=True)

# ─────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────
if calculate:
    st.divider()
    st.header(t["results_header"])

    # Run the same AI logic from climate_analyzer.py and harvest_optimizer.py
    report = full_climate_report(rainfall, temperature, humidity, soil_type)
    current_month = datetime.now().month
    sow_date, sow_note, zone = recommend_sowing_date(rainfall, temperature, current_month)
    harvest_date, growth_days = recommend_harvest_date(sow_date, variety)
    yield_kg, quality, score = estimate_yield(rainfall, temperature, humidity, soil_type)

    risk_level = report["overall_risk"]["level"]
    risk_icon = RISK_COLORS.get(risk_level, "⚪")

    # Top metric row
    m1, m2, m3 = st.columns(3)
    m1.metric(t["risk_level"], f"{risk_icon} {risk_level}")
    m2.metric(t["sow_date"], sow_date)
    m3.metric(t["harvest_date"], harvest_date)

    st.write("")
    y1, y2 = st.columns(2)
    y1.metric(t["yield_label"], f"{yield_kg:,} kg/ha")
    y2.metric(t["quality_label"], quality)

    st.write("")
    st.info(report["overall_risk"]["message"])

    # Detailed breakdown
    with st.expander(t["details_header"]):
        st.write(f"🌧️ **Rainfall** [{report['rainfall']['status']}] — {report['rainfall']['message']}")
        st.write(f"🌡️ **Temperature** [{report['temperature']['status']}] — {report['temperature']['message']}")
        st.write(f"💧 **Humidity** [{report['humidity']['status']}] — {report['humidity']['message']}")
        st.write(f"🪨 **Soil** [{report['soil']['status']}] — {report['soil']['message']}")
        st.write(f"🌍 **Climate Zone:** {zone.title()}")
        st.write(f"📈 **Condition Score:** {score}/100")

st.divider()
st.caption(t["footer"])
