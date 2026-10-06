"""
Farmer Easy Mode Module - Visual UI/UX Redesign for KrishiSetu
Designed for rural farmers: large touch targets, visual icons, color-cured urgency.
"""

import html
import streamlit as st
import pandas as pd
from config import INDIAN_LOCATIONS, SOIL_TYPES
from modules.crop_planner import calculate_crop_recommendations
from modules.crop_doctor import analyze_crop_leaf
from modules.weather_service import get_weather_forecast, generate_weather_advisory
from data.mandi_prices import get_mandi_price_history
from modules.chat_persistence import save_chat_message, load_chat_history
from modules.krishisarthi import get_krishisarthi_response
from modules.community import render_community_tab

# === Visual Icon Map for Farmer Actions ===
ACTION_ICONS = {
    "Crop Recommendations": "🌱",
    "AI Leaf Doctor": "🩺",
    "Weather Advisory": "☀️🌧️",
    "Mandi Prices": "💰",
    "Krishi-Sarthi Bot": "🤖",
    "Farmer Community": "👥"
}

ACTION_COPY = {
    "en": {
        "hello": "Welcome",
        "greeting": "A better day starts with a better plan.",
        "question": "What would you like help with?",
        "choose": "Choose a service to get started.",
        "farm_profile": "Personalize your crop advice",
        "farm_details": "Farm details",
        "farm_hint": "Used to make your crop suggestions more useful.",
        "soil": "Soil type",
        "land": "Farm size (acres)",
        "water": "Water source",
        "season": "Growing season",
        "open": "Open",
        "empty": "Choose one of the services above to see your advice here.",
        "descriptions": {
            "Crop Recommendations": "Find crops suited to your soil and season.",
            "AI Leaf Doctor": "Upload a leaf photo to check for common problems.",
            "Weather Advisory": "See local forecast and farm guidance.",
            "Mandi Prices": "Check recent prices for your crops.",
            "Krishi-Sarthi Bot": "Ask a farming question in your own words.",
            "Farmer Community": "Learn and share with nearby farmers."
        },
        "titles": {
            "Crop Recommendations": "Crop Planner",
            "AI Leaf Doctor": "AI Leaf Doctor",
            "Weather Advisory": "Weather",
            "Mandi Prices": "Mandi Prices",
            "Krishi-Sarthi Bot": "Krishi-Sarthi",
            "Farmer Community": "Farmer Community"
        }
    },
    "hi": {
        "hello": "नमस्कार",
        "greeting": "बेहतर खेती की शुरुआत सही योजना से होती है।",
        "question": "आज आपको किस काम में मदद चाहिए?",
        "choose": "शुरू करने के लिए कोई सेवा चुनें।",
        "farm_profile": "अपनी फसल सलाह को बेहतर बनाएँ",
        "farm_details": "खेत की जानकारी",
        "farm_hint": "इससे फसल की सलाह आपके खेत के अनुसार मिलेगी।",
        "soil": "मिट्टी का प्रकार",
        "land": "खेत का आकार (एकड़)",
        "water": "पानी का स्रोत",
        "season": "फसल का मौसम",
        "open": "खोलें",
        "empty": "सलाह देखने के लिए ऊपर से कोई सेवा चुनें।",
        "descriptions": {
            "Crop Recommendations": "मिट्टी और मौसम के अनुसार फसल चुनें।",
            "AI Leaf Doctor": "पत्ते की तस्वीर से आम समस्याएँ पहचानें।",
            "Weather Advisory": "स्थानीय मौसम और खेती की सलाह देखें।",
            "Mandi Prices": "अपनी फसलों के हाल के भाव देखें।",
            "Krishi-Sarthi Bot": "खेती से जुड़ा सवाल पूछें।",
            "Farmer Community": "दूसरे किसानों से सीखें और साझा करें।"
        },
        "titles": {
            "Crop Recommendations": "फसल सलाह",
            "AI Leaf Doctor": "पत्ती रोग जाँच",
            "Weather Advisory": "मौसम",
            "Mandi Prices": "मंडी भाव",
            "Krishi-Sarthi Bot": "कृषि-साथी",
            "Farmer Community": "किसान समुदाय"
        }
    },
    "mr": {
        "hello": "नमस्कार",
        "greeting": "चांगल्या शेतीची सुरुवात योग्य नियोजनाने.",
        "question": "आज तुम्हाला कशासाठी मदत हवी आहे?",
        "choose": "सुरू करण्यासाठी सेवा निवडा.",
        "farm_profile": "तुमच्या पिकांचा सल्ला वैयक्तिक करा",
        "farm_details": "शेताची माहिती",
        "farm_hint": "यामुळे पिकांची शिफारस तुमच्या शेतासाठी योग्य होईल.",
        "soil": "मातीचा प्रकार",
        "land": "शेताचे क्षेत्रफळ (एकर)",
        "water": "पाण्याचा स्रोत",
        "season": "हंगाम",
        "open": "उघडा",
        "empty": "सल्ला पाहण्यासाठी वरील सेवा निवडा.",
        "descriptions": {
            "Crop Recommendations": "माती आणि हंगामानुसार योग्य पीक निवडा.",
            "AI Leaf Doctor": "पानाचा फोटो देऊन सामान्य रोग तपासा.",
            "Weather Advisory": "स्थानिक हवामान आणि शेतीविषयक सल्ला पहा.",
            "Mandi Prices": "तुमच्या पिकांचे अलीकडील बाजारभाव पहा.",
            "Krishi-Sarthi Bot": "शेतीविषयक प्रश्न विचारा.",
            "Farmer Community": "इतर शेतकऱ्यांकडून शिका आणि माहिती शेअर करा."
        },
        "titles": {
            "Crop Recommendations": "पीक नियोजन",
            "AI Leaf Doctor": "पान रोग तपासणी",
            "Weather Advisory": "हवामान",
            "Mandi Prices": "बाजारभाव",
            "Krishi-Sarthi Bot": "कृषी-सारथी",
            "Farmer Community": "शेतकरी समुदाय"
        }
    }
}


def render_farmer_simple_mode(t, selected_state, selected_district, lang_code, gemini_api_key, usr):
    copy = ACTION_COPY.get(lang_code, ACTION_COPY["en"])
    is_marathi = lang_code == "mr"
    user_name = usr.get('full_name', 'शेतकरी')
    safe_user_name = html.escape(str(user_name))
    safe_district = html.escape(str(selected_district))
    safe_state = html.escape(str(selected_state))

    hero_text, hero_image = st.columns([1.7, 1], gap="large")
    with hero_text:
        st.markdown(f"""
        <div style="height:100%; min-height:190px; padding:28px 30px; border-radius:22px;
                    background:linear-gradient(125deg,#174b2b 0%,#24733d 68%,#40884b 100%);
                    box-shadow:0 14px 34px rgba(23,75,43,.18); color:#fff;">
            <div style="font-size:13px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
                        color:#d1f0d2;">KRISHISETU · FARMER DESK</div>
            <h1 style="color:#fff; font-size:clamp(1.8rem,3vw,2.5rem); line-height:1.18;
                       margin:14px 0 8px;">{copy['hello']}, {safe_user_name}!</h1>
            <p style="color:#eff8ee; font-size:1.05rem; margin:0 0 18px;">{copy['greeting']}</p>
            <span style="display:inline-block; padding:7px 12px; border-radius:99px;
                         background:rgba(255,255,255,.14); color:#fff; font-size:.9rem;">
                📍 {safe_district}, {safe_state}
            </span>
        </div>
        """, unsafe_allow_html=True)
    with hero_image:
        st.image(
            "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=900&auto=format&fit=crop&q=80",
            use_container_width=True
        )

    st.markdown(f"### {copy['question']}")
    st.caption(copy["choose"])

    actions = [
        ("Crop Recommendations", "#2e7d32"),
        ("AI Leaf Doctor", "#1565c0"),
        ("Weather Advisory", "#1e88e5"),
        ("Mandi Prices", "#f57c00"),
        ("Krishi-Sarthi Bot", "#008577"),
        ("Farmer Community", "#7954a1")
    ]

    cols = st.columns(3, gap="large")

    for i, (action_key, color) in enumerate(actions):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="min-height:136px; padding:18px; margin:8px 0 4px;
                        border:1px solid #e3eade; border-left:4px solid {color};
                        border-radius:16px; background:#fff;
                        box-shadow:0 5px 16px rgba(27,55,33,.06);">
                <div style="width:44px; height:44px; display:grid; place-items:center;
                            border-radius:13px; background:{color}18; font-size:1.55rem;">
                    {ACTION_ICONS[action_key]}
                </div>
                <h3 style="color:#173b25; margin:12px 0 4px; font-size:1.02rem; font-weight:750;">
                    {copy['titles'][action_key]}
                </h3>
                <p style="color:#667568; font-size:.87rem; margin:0; line-height:1.45;">
                    {copy['descriptions'][action_key]}
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"{copy['open']} {copy['titles'][action_key]}  →",
                key=f"action_{action_key}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state['farmer_selected_action'] = action_key
                st.session_state['farmer_action_timestamp'] = pd.Timestamp.now().timestamp()
                st.rerun()

    st.markdown("---")
    st.markdown(f"### 🌾 {copy['farm_profile']}")
    st.caption(copy["farm_hint"])

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        with st.expander(copy["farm_details"], expanded=True):
            soil_type = st.selectbox(copy["soil"], SOIL_TYPES, index=1, key="farmer_soil_type")
            land_size = st.number_input(
                copy["land"],
                min_value=0.5,
                max_value=100.0,
                value=2.0,
                step=0.5,
                key="farmer_land_size"
            )
            water_source = st.selectbox(
                copy["water"],
                ["Tube Well / Borewell", "Canal Irrigation", "Rainfed Only", "Drip / Sprinkler"],
                key="farmer_water_source"
            )
            season = st.selectbox(
                copy["season"],
                ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"],
                key="farmer_season"
            )

    with col2:
        # Show relevant results based on stored action
        selected_action = st.session_state.get('farmer_selected_action', None)

        if selected_action == "Crop Recommendations":
            st.markdown(f"### 🌱 {copy['titles'][selected_action]}")
            recs = calculate_crop_recommendations(
                selected_state,
                selected_district,
                soil_type,
                land_size,
                season,
                water_source,
                15000
            )

            c1, c2, c3 = st.columns(3)
            for idx, crop in enumerate(recs[:3]):
                with [c1, c2, c3][idx]:
                    net_profit = crop['estimated_net_profit']
                    profit_color = "#2e7d32" if net_profit > 15000 else "#f57c00" if net_profit > 5000 else "#e53935"
                    st.markdown(f"""
                    <div style="min-height:124px; background:#fff; border-radius:14px;
                                padding:16px; border:1px solid #e3eade;
                                border-top:4px solid {profit_color}; margin-bottom:12px;
                                box-shadow:0 4px 14px rgba(27,55,33,.06);">
                        <b style="color:#173b25; font-size:1rem;">{crop['name']}</b><br>
                        <span style="color:{profit_color}; font-weight:800; font-size:1.25rem;">
                            ₹{net_profit:,.0f}
                        </span><br>
                        <small style="color:#667568;">Est. profit · {crop['expected_yield']} Qtl yield</small>
                    </div>
                    """, unsafe_allow_html=True)

        elif selected_action == "AI Leaf Doctor":
            st.markdown(f"### {'पानाचे रोग निदान (फोटो अपलोड करा)' if is_marathi else 'Leaf Pathology Diagnosis (Upload Photo)'}")
            img_file = st.file_uploader("पानाचा फोटो निवडा (Select Leaf Photo)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
            if img_file:
                st.image(img_file, width=350, caption="📸 अपलोडेड फोटो")
                if st.button("🔍 रोग तपासा (Check Disease)", type="primary", use_container_width=True):
                    with st.spinner("तपासणी चालू आहे..."):
                        res = analyze_crop_leaf(img_file, gemini_api_key)
                        st.markdown(res['diagnosis'])

        elif selected_action == "Weather Advisory":
            st.markdown(f"### {selected_district} - {'आजचा हवामान अंदाज' if is_marathi else 'Weather Forecast'}")
            location = INDIAN_LOCATIONS[selected_state]
            forecast = get_weather_forecast(location["lat"], location["lon"])
            advisories = generate_weather_advisory(forecast, lang_code)
            for adv in advisories:
                adv_color = "#2e7d32" if adv.get('urgency') == 'Low' else "#f57c00" if adv.get('urgency') == 'Medium' else "#e53935"
                st.markdown(f"""
                <div style="background: #fff8e1; border-left: 4px solid {adv_color};
                            border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
                    <b style="color: {adv_color}; font-size: 1rem;">🔔 {adv['title']}</b><br>
                    <small style="color: #333;">{adv['message']}</small>
                </div>
                """, unsafe_allow_html=True)

            # Weather table
            if forecast:
                df_weather = pd.DataFrame(forecast)
                st.dataframe(df_weather, use_container_width=True, column_config={
                    "time": "वेळ",
                    "temperature": "तापमान (°C)",
                    "condition": "स्थिती",
                    "rainfall": "पावस (mm)"
                })

        elif selected_action == "Mandi Prices":
            st.markdown(f"### {'आजचे बाजारभाव (₹ प्रति क्विंटल)' if is_marathi else 'Today Mandi Market Prices (₹/Quintal)'}")
            # Show multiple crops, not just wheat
            crops = ["wheat", "soybean", "cotton", "tur", "gram"]
            for crop in crops[:3]:
                df_p = get_mandi_price_history(crop)
                if not df_p.empty:
                    st.caption(f"🌾 {crop.upper()}")
                    st.dataframe(df_tail(df_p, 3), use_container_width=True)
                    st.markdown("")

        elif selected_action == "Krishi-Sarthi Bot":
            render_krishisarthi_bot(t, lang_code, usr, gemini_api_key)

        elif selected_action == "Farmer Community":
            render_community_tab(lang_code, usr, selected_district, selected_state)

        else:
            st.info(copy["empty"])

def render_krishisarthi_bot(t, lang_code, usr, gemini_api_key):
    """Krishi-Sarthi bot section with improved farmer-friendly UI"""
    is_marathi = (lang_code == 'mr')
    user_id = usr.get('id', 1)
    session_id = "easy_mode_session"

    st.markdown(f"### {'कृषी-सारथी व्हॉट्सॲप बॉट (आवाज किंवा मजकूर)' if is_marathi else 'Krishi-Sarthi Voice / Text Assistant'}")

    chat_history = load_chat_history(user_id, session_id)
    if not chat_history:
        # Friendly greeting in user's language
        greetings = {
            "mr": "नमस्कार शेतकरी बंधू! मी कृषी-सारथी आहे. तुम्हाला काय सल्ला चाहीये?",
            "hi": "नमस्ते किसान भाई! मैं कृषी-सारथी हूँ। क्या मदद करूं?",
            "en": "Hello Farmer! I'm Krishi-Sarthi. How can I help you today?"
        }
        save_chat_message(user_id, session_id, "assistant", greetings.get(lang_code, greetings["en"]))
        chat_history = load_chat_history(user_id, session_id)

    # Enhanced touch-friendly action buttons
    action_col1, action_col2 = st.columns([1, 1], gap="large")

    with action_col1:
        if st.button("🎤 Voice Query", use_container_width=True, type="secondary"):
            # Simulated voice query based on common farmer questions
            voice_questions = [
                "गेहू में पीला रतुआ लग रहा है क्या करूँ?",
                "आज बारिश होनेवारी आहे का?",
                "आजचे बाजार भाव कोणते?",
                "तोमॅटोचा रोग का होऊ लागतो?"
            ]
            import random
            q = random.choice(voice_questions)
            save_chat_message(user_id, session_id, "user", q + " (Voice Audio Note 🎙️)")
            reply = get_krishisarthi_response(q, lang_code)
            save_chat_message(user_id, session_id, "assistant", reply)
            st.rerun()

    with action_col2:
        if st.button("💬 Text Question", use_container_width=True, type="secondary"):
            st.session_state['show_bot_input'] = True

    # Text input area - expanded for touch
    show_input = st.session_state.get('show_bot_input', False)
    user_q = ""
    if show_input:
        user_q = st.text_input("तुमचा प्रश्न लिहाा...", key="farmer_bot_text_input",
                               placeholder="उदा. माझ्या टोमॅटो पिकावर करपा आला आहे, कोणते औषध फवारावे?",
                               label_visibility="collapsed")

    if st.session_state.get('show_bot_input', False):
        if st.button("❌ बन्द करा", key="close_bot_input", help="Close input"):
            st.session_state['show_bot_input'] = False
            st.rerun()

    if user_q:
        save_chat_message(user_id, session_id, "user", user_q)
        with st.spinner("सल्ला मिळणे..."):
            reply = get_krishisarthi_response(user_q, lang_code)
        save_chat_message(user_id, session_id, "assistant", reply)
        st.session_state['show_bot_input'] = False
        st.rerun()

    # Display chat history with farmer-friendly cards
    st.markdown("---")
    st.markdown(f"### {'वार्ता इतिहास (Chat History)' if is_marathi else 'Conversation History'}")

    for chat in load_chat_history(user_id, session_id):
        if chat["role"] == "user":
            # Farmer message card - green theme
            st.markdown(f'''
            <div style="background: #e8f5e9; border-left: 4px solid #2e7d32;
                        border-radius: 14px; padding: 12px 16px; margin-bottom: 12px;
                        max-width: 80%; margin-left: 20px; color: #1b5e20;
                        font-size: 14px; line-height: 1.5;">
                <b style="font-size: 13px;">👨‍🌾 शेतकरी (Farmer):</b> {chat["content"]}
            </div>
            ''', unsafe_allow_html=True)
        else:
            # Assistant message card - blue/teal theme
            st.markdown(f'''
            <div style="background: #e3f2fd; border-left: 4px solid #1565c0;
                        border-radius: 14px; padding: 12px 16px; margin-bottom: 12px;
                        max-width: 80%; margin-right: 20px; color: #1b5e20;
                        font-size: 14px; line-height: 1.5;">
                <b style="font-size: 13px; color: #1565c0;">🤖 कृषी-सारथी (Krishi-Sarthi):</b><br>{chat["content"]}
            </div>
            ''', unsafe_allow_html=True)


def df_tail(df, n=3):
    """Helper to get last n rows"""
    return df.tail(n).reset_index(drop=True)