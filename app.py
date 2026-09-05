"""
Main Streamlit Application for KrishiSetu Platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

from config import INDIAN_LOCATIONS, SOIL_TYPES, TRANSLATIONS
from modules.crop_planner import calculate_crop_recommendations
from data.mandi_prices import get_mandi_price_history, get_market_advisory
from modules.weather_service import get_weather_forecast, generate_weather_advisory
from modules.crop_doctor import analyze_crop_leaf
from modules.marketplace import load_data, add_farmer_listing, add_buyer_demand
from modules.auth import init_auth_db, register_user, authenticate_user
from modules.translator_service import translate_text
from modules.krishisarthi import get_krishisarthi_response
from modules.farmer_mode import render_farmer_simple_mode

# Initialize Auth DB
init_auth_db()

# Page Configuration
st.set_page_config(
    page_title="KrishiSetu | Market-Linked Crop Planning & Rural Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling & Typography (Agricultural Navbar & Palette)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+Devanagari:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-family: 'Inter', 'Noto Serif Devanagari', sans-serif;
        font-size: 2.4rem;
        color: #1B5E20;
        font-weight: 700;
        margin-bottom: 0rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-family: 'Inter', 'Noto Serif Devanagari', sans-serif;
        font-size: 1.15rem;
        color: #2E7D32;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    h1, h2, h3, .stButton>button {
        font-family: 'Inter', 'Noto Serif Devanagari', sans-serif !important;
        font-weight: 600 !important;
    }

    .stButton>button {
        font-size: 0.95rem !important;
        border-radius: 8px !important;
        background-color: #2E7D32 !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        border: none !important;
    }

    /* Metric cards adjustments to prevent text truncation */
    [data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #1B5E20 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: #388E3C !important;
        white-space: nowrap !important;
    }

    .metric-card {
        background-color: #F1F8E9;
        color: #1B5E20 !important;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-card b, .metric-card div, .metric-card i, .metric-card a {
        color: #1B5E20 !important;
    }
    .stAlert {
        border-radius: 8px;
    }

    /* Professional Agricultural Navbar Strip */
    .stTabs {
        background-color: #FFFFFF;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #DCEDC8;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 10px;
        background-color: transparent;
        padding: 4px;
        flex-wrap: nowrap;
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: nowrap !important;
        background-color: #FAFAFA;
        color: #333333;
        border-radius: 10px !important;
        padding: 0px 24px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        border: 1px solid #E0E0E0 !important;
        transition: all 0.2s ease-in-out;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E8F5E9 !important;
        color: #1B5E20 !important;
        border-color: #C8E6C9 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 6px rgba(46, 125, 50, 0.2) !important;
        border-color: #2E7D32 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State for Authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

# Sidebar Controls for Language only when logged in
st.sidebar.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=400&auto=format&fit=crop&q=60", use_container_width=True)
st.sidebar.title("KrishiSetu Controls")

lang_option = st.sidebar.selectbox("Language / भाषा", ["English", "हिंदी (Hindi)", "मराठी (Marathi)"])
if lang_option == "English":
    lang_code = "en"
elif "Hindi" in lang_option:
    lang_code = "hi"
else:
    lang_code = "mr"
t = TRANSLATIONS[lang_code]

# Sidebar Navigation / Mode Toggle right under Language
st.sidebar.markdown("---")
st.sidebar.subheader("Navigation & Modes")
app_mode = st.sidebar.radio("Select View / दृश्य निवडा", [
    "Advanced Dashboard",
    "Farmer Easy Mode (शेतकरी सोपा मोड)"
])
# Authentication Check / Center Modal
if st.session_state["user"] is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"<h1 style='text-align: center; color: #1b5e20;'>{t['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #388e3c;'>{t['tagline']}</p><br>", unsafe_allow_html=True)
        
        auth_mode = st.radio("Choose Action / पर्याय निवडा", ["Login / लॉगिन", "Register / नोंदणी करा"], horizontal=True)
        
        if auth_mode == "Login / लॉगिन":
            with st.form("center_login_form"):
                st.subheader("User Login")
                l_username = st.text_input("Username / ईमेल किंवा युजरनेम")
                l_password = st.text_input("Password / पासवर्ड", type="password")
                l_submit = st.form_submit_button("Login / प्रवेश करा", type="primary")
                
                if l_submit:
                    usr_obj = authenticate_user(l_username, l_password)
                    if usr_obj:
                        st.session_state["user"] = usr_obj
                        st.success(f"Welcome back, {usr_obj['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password. / चुकीचा युजरनेम किंवा पासवर्ड.")
        else:
            with st.form("center_register_form"):
                st.subheader("📝 New User Registration")
                r_fullname = st.text_input("Full Name / पूर्ण नाव")
                r_mobile = st.text_input("Mobile Number / मोबाईल नंबर")
                r_username = st.text_input("Username / युजरनेम")
                r_password = st.text_input("Password / पासवर्ड", type="password")
                
                r_persona = st.selectbox("Who you are? / तुमची भूमिका (Role)", [
                    t["persona_farmer"],
                    t["persona_fpo"],
                    t["persona_buyer"],
                    t["persona_agronomist"],
                    t["persona_researcher"]
                ])
                
                r_state = st.selectbox("State / राज्य", list(INDIAN_LOCATIONS.keys()))
                r_district = st.selectbox("District / जिल्हा", INDIAN_LOCATIONS[r_state]["districts"])
                
                r_submit = st.form_submit_button("Register Account / खाते तयार करा", type="primary")
                if r_submit:
                    if r_username and r_password and r_fullname and r_mobile:
                        success = register_user(r_username, r_password, r_fullname, r_mobile, r_persona, r_district, r_state)
                        if success:
                            st.success("Account created successfully! Please switch to Login tab above. / खाते यशस्वीरित्या तयार झाले! आता लॉगिन करा.")
                        else:
                            st.error("Username already exists. / हा युजरनेम आधीपासून अस्तित्वात आहे.")
                    else:
                        st.warning("Please fill all required fields. / कृपया सर्व आवश्यक माहिती भरा.")
                        
    st.stop() # Stop rendering until logged in
else:
    usr = st.session_state["user"]
    st.sidebar.markdown("---")
    st.sidebar.success(f"User: **{usr['full_name']}**\n\nMobile: {usr['mobile']}\n\nRole: *{usr['persona']}*\n\nLocation: {usr.get('district', 'Ahmednagar')}, {usr.get('state', 'Maharashtra')}")
    if st.sidebar.button("Logout / बाहेर पडा"):
        st.session_state["user"] = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Location & Farm Setup")
default_state = st.session_state["user"].get("state", "Maharashtra") if st.session_state.get("user") else "Maharashtra"
selected_state = st.sidebar.selectbox(t["state"], list(INDIAN_LOCATIONS.keys()), index=list(INDIAN_LOCATIONS.keys()).index(default_state) if default_state in INDIAN_LOCATIONS else 0)
district_list = INDIAN_LOCATIONS[selected_state]["districts"]
default_dist = st.session_state["user"].get("district", district_list[0]) if st.session_state.get("user") else district_list[0]
selected_district = st.sidebar.selectbox(t["district"], district_list, index=district_list.index(default_dist) if default_dist in district_list else 0)

# Mirror to session state for synchronization
st.session_state["selected_district"] = selected_district
st.session_state["selected_state"] = selected_state

selected_soil = st.sidebar.selectbox(t["soil_type"], SOIL_TYPES)
land_size = st.sidebar.number_input(t["land_size"], min_value=0.5, max_value=100.0, value=2.0, step=0.5)
season = st.sidebar.selectbox(t["season"], ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"])
water_source = st.sidebar.selectbox("Irrigation Source", ["Tube Well / Borewell", "Canal Irrigation", "Rainfed Only", "Drip / Sprinkler"])
budget = st.sidebar.slider(t["budget"], min_value=5000, max_value=50000, value=15000, step=1000)

st.sidebar.markdown("---")
st.sidebar.subheader("AI & Integrations")
gemini_api_key = st.sidebar.text_input("Gemini API Key (Optional)", type="password", help="Enter key for live leaf disease diagnosis or leave blank for offline AI demo.")
datagov_api_key = st.sidebar.text_input("Data.gov.in API Key (Optional)", type="password", help="Enter key for live Agmarknet APMC mandi prices from Open Government Data India.")

if app_mode == "Farmer Easy Mode (शेतकरी सोपा मोड)":
    render_farmer_simple_mode(t, selected_state, selected_district, lang_code, gemini_api_key, usr)
else:
    # Professional Floating Agricultural Navbar Strip
    st.markdown("""
    <style>
        .stTabs {
            background-color: #FFFFFF !important;
            padding: 16px !important;
            border-radius: 14px !important;
            border: 1px solid #C8E6C9 !important;
            box-shadow: 0 10px 15px -3px rgba(46, 125, 50, 0.08), 0 4px 6px -2px rgba(46, 125, 50, 0.04) !important;
            margin-bottom: 25px !important;
            margin-top: 5px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    tab_titles = [
        t["nav_planner"],
        t["nav_mandi"],
        t["nav_doctor"],
        t["nav_weather"],
        t["nav_ops"],
        t["nav_market"],
        t["nav_sarthi"]
    ]
    tabs = st.tabs(tab_titles)

    # -------------------------------------------------------------
    # TAB 1: Smart Crop Planner (Basic & Precision Modes)
    # -------------------------------------------------------------
    with tabs[0]:
        st.markdown(f'<p class="main-header">{translate_text(t["nav_planner"], lang_code)}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{translate_text("Advanced crop recommendation engine combining soil suitability, market demand and expected ROI for", lang_code)} **{selected_district}, {selected_state}**.</p>', unsafe_allow_html=True)

        # Basic Mode Inputs
        c_mode1, c_mode2 = st.columns(2)
        with c_mode1:
            previous_crop = st.selectbox(translate_text("Previous Grown Crop", lang_code), ["None", "Wheat", "Paddy", "Soybean", "Cotton", "Mustard", "Chana"])
            farming_goal = st.selectbox(translate_text("Farming Goal", lang_code), [translate_text("Maximize Profit", lang_code), translate_text("Low Risk & Stable Yield", lang_code), translate_text("Soil Health Restoration", lang_code)])
        with c_mode2:
            setup_prefix = "सक्रिय शेती सेटअप" if lang_code == 'mr' else ("सक्रिय कृषि सेटअप" if lang_code == 'hi' else "Active Farm Setup")
            acres_text = "एकर" if lang_code == 'mr' else ("एकड़" if lang_code == 'hi' else "Acres")
            st.info(f"{setup_prefix}: {selected_state} | {selected_district} | {selected_soil} | {land_size} {acres_text}")

        # Precision Mode Toggle via Button / State
        if "show_precision" not in st.session_state:
            st.session_state["show_precision"] = False
            
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            if st.button(translate_text("Advance Soil (Precision Mode)", lang_code)):
                st.session_state["show_precision"] = not st.session_state["show_precision"]
                
        npk_values = {"ph": 7.0, "nitrogen": 200, "phosphorus": 20, "potassium": 250}
        
        if st.session_state["show_precision"]:
            st.markdown("---")
            st.subheader(translate_text("Precision Soil Parameters Setup (Advanced Mode)", lang_code))
            precision_method = st.radio(translate_text("Choose Input Method:", lang_code), [translate_text("Enter NPK + pH manually", lang_code), translate_text("Upload Soil Test Report (PDF/JPG/PNG)", lang_code)])
            
            if "Upload" in precision_method:
                soil_report_file = st.file_uploader(translate_text("Upload Soil Test Report", lang_code), type=["pdf", "jpg", "jpeg", "png"])
                if soil_report_file:
                    with st.spinner(translate_text("Extracting soil report values with AI...", lang_code)):
                        from modules.precision_planner import parse_soil_report
                        extracted = parse_soil_report(soil_report_file, gemini_api_key)
                        st.success(translate_text("Soil parameters successfully extracted from report! Please verify below:", lang_code))
                        npk_values["ph"] = st.number_input(translate_text("Soil pH", lang_code), value=float(extracted.get("ph", 7.0)), step=0.1)
                        npk_values["nitrogen"] = st.number_input(translate_text("Available Nitrogen (kg/ha)", lang_code), value=int(extracted.get("nitrogen", 200)))
                        npk_values["phosphorus"] = st.number_input(translate_text("Available Phosphorus (kg/ha)", lang_code), value=int(extracted.get("phosphorus", 20)))
                        npk_values["potassium"] = st.number_input(translate_text("Available Potassium (kg/ha)", lang_code), value=int(extracted.get("potassium", 250)))
            else:
                col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                npk_values["ph"] = col_p1.number_input(translate_text("Soil pH", lang_code), min_value=4.0, max_value=10.0, value=7.0, step=0.1)
                npk_values["nitrogen"] = col_p2.number_input("Nitrogen (N)", min_value=50, max_value=500, value=200)
                npk_values["phosphorus"] = col_p3.number_input("Phosphorus (P)", min_value=5, max_value=100, value=20)
                npk_values["potassium"] = col_p4.number_input("Potassium (K)", min_value=50, max_value=600, value=250)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(translate_text(t["btn_plan"], lang_code), type="primary"):
            from modules.precision_planner import advanced_precision_recommendation
            recommendations = advanced_precision_recommendation(
                selected_state, selected_district, selected_soil, season, water_source, budget, farming_goal, previous_crop, npk_values
            )
            st.session_state["recommendations"] = recommendations

        if "recommendations" in st.session_state:
            recs = st.session_state["recommendations"]
            top_crop = recs[0]
            
            st.markdown(f"### {translate_text(t['best_roi'], lang_code)}: **{top_crop['name']}**")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(translate_text("Est. Total Investment", lang_code), f"₹{top_crop['total_cost']:,}")
            col2.metric(translate_text("Est. Gross Revenue", lang_code), f"₹{top_crop['estimated_revenue']:,}")
            col3.metric(translate_text("Est. Net Profit", lang_code), f"₹{top_crop['estimated_net_profit']:,}", f"{top_crop['roi_percentage']}% ROI", delta_color="normal")
            col4.metric(translate_text("Market Demand", lang_code), translate_text(top_crop['market_demand'], lang_code))
            
            st.markdown("---")
            
            st.subheader(translate_text("Top 5 Crops: Comparative Net Profit vs Investment (₹)", lang_code))
            top_5_recs = recs[:5]
            df_comp = pd.DataFrame({
                "Crop": [c["name"] for c in top_5_recs],
                "Net Profit (₹)": [c["estimated_net_profit"] for c in top_5_recs],
                "Investment (₹)": [c["total_cost"] for c in top_5_recs]
            })
            df_comp_melted = df_comp.melt(id_vars="Crop", value_vars=["Net Profit (₹)", "Investment (₹)"], var_name="Financial Metric", value_name="Amount (₹)")
            fig_comp = px.bar(df_comp_melted, x="Crop", y="Amount (₹)", color="Financial Metric", barmode="group", color_discrete_sequence=["#2E7D32", "#81C784"])
            fig_comp.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_comp, use_container_width=True)
            
            st.markdown("---")
            st.subheader(translate_text("Ranked Crop Suitability & Detailed Reasoning", lang_code))
            st.caption(translate_text("Note: Recommendations are agronomic estimates based on mathematical models and current market data, not guarantees.", lang_code))
            
            for idx, crop in enumerate(recs):
                match_badge = "🟢" if crop['score'] >= 75 else ("🟡" if crop['score'] >= 50 else "🟠")
                risk_color = translate_text("Low Risk", lang_code) if crop['risk_level'] == "Low" else (translate_text("Medium Risk", lang_code) if crop['risk_level'] == "Medium" else translate_text("High Risk", lang_code))
                
                expander_label = f"#{idx+1} {crop['name']} | {match_badge} {crop['score']}% {translate_text('Match', lang_code)} | ₹{crop['estimated_net_profit']:,} {translate_text('net', lang_code)} | {crop['duration_days']} {translate_text('Days', lang_code)} | {risk_color}"
                
                with st.expander(expander_label):
                    sc1, sc2, sc3, sc4 = st.columns(4)
                    sc1.metric(translate_text("Cultivation Cost", lang_code), f"₹{crop['total_cost']:,}")
                    sc2.metric(translate_text("Expected Yield", lang_code), f"{crop['expected_yield']} Qtl")
                    sc3.metric(translate_text("Gross Revenue", lang_code), f"₹{crop['estimated_revenue']:,}")
                    sc4.metric(translate_text("Crop Duration", lang_code), f"{crop['duration_days']} {translate_text('Days', lang_code)}")
                    
                    st.markdown("---")
                    st.markdown(f"**{translate_text('Agronomic Rationale & Suitability Analysis:', lang_code)}**")
                    for r in crop['reasons']:
                        translated_r = translate_text(r, lang_code)
                        if "✅" in r or "Optimal" in r or "favorable" in r or "Aligned" in r:
                            st.success(f"✔ {translated_r.replace('✅ ', '')}")
                        elif "⚠️" in r or "marginal" in r or "Warning" in r:
                            st.warning(f"⚠ {translated_r.replace('⚠️ ', '')}")
                        else:
                            st.info(f"ℹ {translated_r}")

    # -------------------------------------------------------------
    # TAB 2: Mandi Price Forecast & Analytics
    # -------------------------------------------------------------
    with tabs[1]:
        st.markdown(f'<p class="main-header">{t.get("mandi_title", "Mandi Price Forecast")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{t.get("mandi_subtitle", "Historical mandi prices and forecasts.")}</p>', unsafe_allow_html=True)

        selected_crop_mandi = st.selectbox(t.get("mandi_select_commodity", "Select Commodity"), [
            "wheat", "paddy", "soybean", "cotton", "mustard", "chana", "maize", "tomato"
        ], format_func=lambda x: x.capitalize())

        df_prices = get_mandi_price_history(selected_crop_mandi)
        advisory = get_market_advisory(selected_crop_mandi)

        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.line(
                df_prices, x="Month", y="Price (₹/Quintal)", color="Type",
                markers=True, title=f"12-Month Price Trend & 3-Month Forecast for {selected_crop_mandi.capitalize()}"
            )
            fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown(f"### {t.get('market_intelligence', 'Market Intelligence')}")
            st.info(f"**{t.get('optimal_selling_window', 'Optimal Selling Window:')}**\n\n{advisory['best_month']}")
            st.success(f"**{t.get('market_outlook', 'Market Outlook:')}**\n\n{advisory['outlook']}")
            st.warning(f"**{t.get('storage_rec', 'Storage Recommendation:')}**")

        st.markdown("---")
        st.subheader("Live Agmarknet APMC Mandi Wholesale Rates (data.gov.in)")
        from modules.data_gov_mandi import fetch_live_mandi_prices
        df_live, data_source = fetch_live_mandi_prices(api_key=datagov_api_key, state=selected_state, district=selected_district, commodity=selected_crop_mandi.capitalize())
        st.caption(f"Source: {data_source}")
        st.dataframe(df_live, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 3: AI Crop Doctor (Disease Diagnosis)
    # -------------------------------------------------------------
    with tabs[2]:
        st.markdown(f'<p class="main-header">{t.get("doctor_title", "AI Crop Doctor")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{t.get("doctor_subtitle", "Upload leaf...")}</p>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(t["disease_detect"], type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(uploaded_file, caption=t.get("uploaded_sample", "Uploaded Leaf Sample"), use_container_width=True)
            with col2:
                with st.spinner(t.get("analyzing", "Analyzing leaf pathology with AI...")):
                    diagnosis_result = analyze_crop_leaf(uploaded_file, gemini_api_key)
                    st.markdown(f"**Engine Used:** {diagnosis_result['source']}")
                    st.markdown("---")
                    st.markdown(diagnosis_result['diagnosis'])
        else:
            st.info(f"{t.get('doctor_tip', 'Tip: You can upload a photo of wheat rust, rice blast, tomato blight, or cotton damage for instant diagnosis.')}")

    # -------------------------------------------------------------
    # TAB 4: Weather & Farm Advisory
    # -------------------------------------------------------------
    with tabs[3]:
        st.markdown(f'<p class="main-header">{t.get("weather_title", "Weather & Farm Advisory")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{t.get("weather_subtitle", "Hyper-local...").format(district=selected_district, state=selected_state)}</p>', unsafe_allow_html=True)

        lat = INDIAN_LOCATIONS[selected_state]["lat"]
        lon = INDIAN_LOCATIONS[selected_state]["lon"]
        
        forecast = get_weather_forecast(lat, lon)
        advisories = generate_weather_advisory(forecast, lang_code)

        # Display Advisories
        st.subheader(t.get("auto_advisories", "Automated Agronomic Weather Advisories"))
        for adv in advisories:
            if adv["type"] == "warning":
                st.warning(f"**{adv['title']}**\n\n{adv['message']}")
            elif adv["type"] == "success":
                st.success(f"**{adv['title']}**\n\n{adv['message']}")
            else:
                st.info(f"**{adv['title']}**\n\n{adv['message']}")

        st.markdown("---")
        st.subheader(t.get("meteorological_outlook", "7-Day Meteorological Outlook"))
        df_weather = pd.DataFrame(forecast)
        st.dataframe(df_weather, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 5: Operations & Task Tracker
    # -------------------------------------------------------------
    with tabs[4]:
        st.markdown(f'<p class="main-header">{t.get("ops_title", "Operations & Task Tracker")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{t.get("ops_subtitle", "Automated crop calendar...")}</p>', unsafe_allow_html=True)

        selected_crop_ops = st.selectbox(t.get("select_active_crop", "Select Active Crop for Operations"), [
            "wheat", "paddy", "soybean", "cotton", "mustard", "chana", "maize", "tomato"
        ], format_func=lambda x: x.capitalize())

        from data.crops_database import CROP_DATABASE
        crop_obj = next((c for c in CROP_DATABASE if c["id"] == selected_crop_ops), CROP_DATABASE[0])

        st.markdown(f"### {t.get('standard_schedule', 'Standard Schedule for')} {crop_obj['name_en']}")
        
        tasks = crop_obj['fertilizer_schedule']
        for idx, t_item in enumerate(tasks):
            col1, col2, col3 = st.columns([1, 4, 1])
            col1.markdown(f"**{translate_text('Day', lang_code)} {t_item['day']}**")
            col2.markdown(translate_text(t_item['task'], lang_code))
            status = col3.checkbox(translate_text("Completed", lang_code), key=f"task_{selected_crop_ops}_{idx}")

        st.markdown("---")
        st.subheader(t.get("pest_management", "Common Pest & Disease Management Protocols"))
        for dis in crop_obj['common_diseases']:
            with st.expander(translate_text(dis['name'], lang_code)):
                st.markdown(f"**{translate_text('Symptoms:', lang_code)}** {translate_text(dis['symptom'], lang_code)}")
                st.markdown(f"**{translate_text('Recommended Remedy:', lang_code)}** {translate_text(dis['remedy'], lang_code)}")

    # -------------------------------------------------------------
    # TAB 6: Direct Marketplace & Contracts
    # -------------------------------------------------------------
    with tabs[5]:
        st.markdown(f'<p class="main-header">{t.get("market_title", "Direct Marketplace & Contracts")}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{t.get("market_subtitle", "Direct buyer-farmer...")}</p>', unsafe_allow_html=True)

        market_data = load_data()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(t.get("farmer_listings_header", "Farmer Harvest Listings"))
            for listing in market_data["listings"]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 10px;">
                    <b>{listing['crop']}</b> ({listing['quantity_quintals']} Quintals)<br>
                    Farmer: {listing['farmer_name']} | Location: {listing['district']}<br>
                    Expected Price: ₹{listing['expected_price']}/Qtl | Harvest: {listing['harvest_date']}<br>
                    Status: <i>{listing['status']}</i>
                </div>
                """, unsafe_allow_html=True)

        with st.expander(t["farmer_listing"]):
            with st.form(f"farmer_form_{selected_state}"):
                f_name = st.text_input("Farmer Name", value=st.session_state["user"]['full_name'] if st.session_state.get("user") else "")
                f_dist = st.text_input("District / State", value=f"{selected_district}, {selected_state}")
                f_crop = st.selectbox("Crop", ["Wheat", "Paddy", "Soybean", "Cotton", "Mustard", "Chana", "Maize", "Tomato"])
                f_qty = st.number_input("Quantity (Quintals)", min_value=10, value=100)
                f_price = st.number_input("Asking Price (₹/Quintal)", min_value=1000, value=2300)
                f_date = st.date_input("Expected Harvest Date", value=date.today())
                
                submitted_f = st.form_submit_button(t.get("publish_listing", "Publish Listing"))
                if submitted_f:
                    add_farmer_listing(f_name, f_dist, f_crop, f_qty, f_price, f_date)
                    st.success("Listing published successfully to marketplace!")
                    st.rerun()

        with col2:
            st.subheader(t.get("buyer_board_header", "Buyer Demand & Contract Board"))
            for demand in market_data["buyer_demands"]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 10px; border-left-color: #1565c0;">
                    <b>{demand['crop']}</b> (Required: {demand['required_quintals']} Quintals)<br>
                    Buyer: {demand['buyer_org']} | Delivery: {demand['delivery_location']}<br>
                    Offered Price: ₹{demand['offered_price']}/Qtl<br>
                    Contact: <a href="mailto:{demand['contact']}">{demand['contact']}</a>
                </div>
                """, unsafe_allow_html=True)

        with st.expander(t["buyer_board"]):
            with st.form(f"buyer_form_{selected_state}"):
                current_usr = st.session_state.get("user", {})
                b_org = st.text_input("Buyer / FPO Organization Name", value="" if "Farmer" in current_usr.get('persona', '') else current_usr.get('full_name', ''))
                b_crop = st.selectbox("Crop Required", ["Wheat", "Paddy", "Soybean", "Cotton", "Mustard", "Chana", "Maize", "Tomato"])
                b_qty = st.number_input("Required Quantity (Quintals)", min_value=50, value=500)
                b_price = st.number_input("Offered Price (₹/Quintal)", min_value=1000, value=2400)
                b_loc = st.text_input("Delivery Hub / Location")
                b_contact = st.text_input("Email / Phone Contact", value=current_usr.get('mobile', '') if "Farmer" not in current_usr.get('persona', '') else "")
                    
                submitted_b = st.form_submit_button(t.get("publish_demand", "Publish Buyer Demand"))
                if submitted_b:
                    add_buyer_demand(b_org, b_crop, b_qty, b_price, b_loc, b_contact)
                    st.success("Buyer demand published successfully!")
                    st.rerun()

    # -------------------------------------------------------------
    # TAB 7: Krishi-Sarthi WhatsApp / SMS Voice Bot Simulator
    # -------------------------------------------------------------
    with tabs[6]:
        st.markdown(f'<p class="main-header">{t.get("nav_sarthi", "Krishi-Sarthi Bot")}</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Simulated WhatsApp & SMS assistant with persistent SQLite chat history.</p>', unsafe_allow_html=True)
        
        from modules.chat_persistence import save_chat_message, load_chat_history
        
        user_id = usr['id']
        session_id = "default_session"
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### Quick Prompts")
            st.markdown("Click any preset query to simulate a WhatsApp message from a farmer:")
            
            preset_queries = [
                "गेहू में पीला रतुआ लग रहा है क्या करूँ?",
                "धान में ब्लास्ट रोग का उपाय बताओ",
                "टोमॅटो पिकावर करपा रोगासाठी काय करावे?",
                "आज हवामान कसे राहील पाऊस पडेल का?",
                "गहू और सोयाबीनचे आजचे बाजारभाव काय आहेत?"
            ]
            
            selected_preset = None
            for pq in preset_queries:
                if st.button(pq, key=f"btn_{pq}"):
                    selected_preset = pq
                    
        with col2:
            st.markdown("### Krishi-Sarthi Chat Simulator")
            
            # Load chat history from SQLite
            chat_history = load_chat_history(user_id, session_id)
            if not chat_history:
                welcome_msg = "नमस्कार! मी कृषी-सारथी आहे. तुमच्या शेतीविषयी सांगा, मी मदत करेन. (Hello! I am Krishi-Sarthi. How can I assist your farm today?)"
                save_chat_message(user_id, session_id, "assistant", welcome_msg)
                chat_history = load_chat_history(user_id, session_id)
                
            if selected_preset:
                save_chat_message(user_id, session_id, "user", selected_preset)
                reply = get_krishisarthi_response(selected_preset, lang_code)
                save_chat_message(user_id, session_id, "assistant", reply)
                st.rerun()
                
            user_input = st.text_input("Type your question in Marathi, Hindi, or English...", key="sarthi_input")
            if st.button("Send / पाठवा", key="send_sarthi"):
                if user_input:
                    save_chat_message(user_id, session_id, "user", user_input)
                    reply = get_krishisarthi_response(user_input, lang_code)
                    save_chat_message(user_id, session_id, "assistant", reply)
                    st.rerun()
                    
            # Display chat conversation
            for chat in load_chat_history(user_id, session_id):
                if chat["role"] == "user":
                    st.markdown(
                        f'<div style="background-color: #e8f5e9; padding: 10px; border-radius: 10px; margin-bottom: 8px; text-align: right; color: #1b5e20;"><b>Farmer:</b> {chat["content"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="background-color: #f1f8e9; padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #2e7d32; color: #1b5e20;"><b>Krishi-Sarthi:</b><br>{chat["content"]}</div>',
                        unsafe_allow_html=True
                    )
