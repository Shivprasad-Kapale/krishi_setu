"""
Farmer Easy Mode Module with Unified State Synchronization and Dynamic Routing
"""

import streamlit as st
import pandas as pd
from modules.crop_planner import calculate_crop_recommendations
from modules.crop_doctor import analyze_crop_leaf
from modules.weather_service import get_weather_forecast, generate_weather_advisory
from data.mandi_prices import get_mandi_price_history
from modules.chat_persistence import save_chat_message, load_chat_history
from modules.krishisarthi import get_krishisarthi_response

def render_farmer_simple_mode(t, selected_state, selected_district, lang_code, gemini_api_key, usr):
    is_marathi = (lang_code == 'mr')
    
    st.markdown(f"""
    <div style="background-color: #f1f8e9; padding: 20px; border-radius: 12px; border-left: 6px solid #2e7d32; margin-bottom: 20px;">
        <h2 style="color: #1b5e20; margin-top: 0; font-family: 'Poppins', sans-serif;">{ 'शेतकरी सोपा मोड (Farmer Easy Mode)' if is_marathi else 'Farmer Easy Mode' }</h2>
        <p style="color: #2e7d32; font-size: 1.1rem; font-family: 'Poppins', sans-serif;">स्थान (Location): {selected_district}, {selected_state} | शेतकरी (Farmer): {usr.get('full_name', 'شेतकरी')} ({usr.get('mobile', '')})</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(f"### {'1. तुम्हाला काय करायचे आहे?' if is_marathi else '1. What do you want to do?'}")
        action = st.radio("Select Action:", [
            "Crop Recommendations" if not is_marathi else "पिक शिफारस (Crop Planner)",
            "AI Leaf Doctor" if not is_marathi else "रोग निदान (AI Leaf Doctor)",
            "Weather Advisory" if not is_marathi else "हवामान सल्ला (Weather)",
            "Mandi Prices" if not is_marathi else "बाजारभाव (Mandi Prices)",
            "Krishi-Sarthi Bot" if not is_marathi else "कृषी-सारथी बॉट (Chat Bot)"
        ], label_visibility="collapsed")
        
    with col2:
        st.markdown(f"### {'2. जमिनीची सोपी माहिती' if is_marathi else '2. Simple Farm Info'}")
        soil_type = st.selectbox("मातीचा प्रकार (Soil Type):", [
            "काळी माती (Black Soil / Kali Mati)", 
            "गाळाची माती (Alluvial Soil / Gaalachi)", 
            "तांबडी माती (Red Soil / Tambadi)", 
            "दोनमट माती (Clay Loam / Domat)"
        ])
        
        land_size = st.number_input("जमिनीचे क्षेत्रफळ (एकरमध्ये - Acres):", min_value=0.5, max_value=50.0, value=2.0, step=0.5)
        water_source = st.selectbox("पाण्याची उपलब्धता (Water):", ["विहीर / बोरवेल (Borewell)", "कॅनाल / कालवा (Canal)", "केवळ पाऊस (Rainfed)", "ठिबक सिंचन (Drip)"])
        
    st.markdown("---")
    
    if "Crop Planner" in action or "पिक शिफारस" in action:
        st.markdown(f"### {'तुमच्या शेतासाठी सर्वोत्तम पिके (आणि अंदाजे नफा)' if is_marathi else 'Top Recommended Crops & Profit Estimate'}")
        recs = calculate_crop_recommendations(selected_state, selected_district, "Black Soil / Regur (काली मिट्टी)", land_size, "Kharif (Monsoon)", "Tube Well / Borewell", 15000)
        
        c1, c2, c3 = st.columns(3)
        for idx, crop in enumerate(recs[:3]):
            with [c1, c2, c3][idx]:
                net_profit = crop['estimated_net_profit']
                basta = int(net_profit / 2500) # Simple rural unit conversion
                st.markdown(f"""
                <div class="metric-card">
                    <b>{crop['name']}</b><br>
                    अंदाजे शुद्ध नफा: ₹{net_profit:,}<br>
                    (अंदाजे {basta} कट्टे/बास्ता उत्पादन)<br>
                    उत्तम मागणी: {crop['market_demand']}
                </div>
                """, unsafe_allow_html=True)
                
    elif "Leaf Doctor" in action or "रोग निदान" in action:
        st.markdown(f"### {'पानाचे रोग निदान (फोटो अपलोड करा)' if is_marathi else 'Leaf Pathology Diagnosis (Upload Photo)'}")
        img_file = st.file_uploader("पानाचा फोटो निवडा (Select Leaf Photo)", type=["jpg", "jpeg", "png"])
        if img_file:
            st.image(img_file, width=300)
            if st.button("रोग तपासा (Check Disease)", type="primary"):
                with st.spinner("तपासणी चालू आहे..."):
                    res = analyze_crop_leaf(img_file, gemini_api_key)
                    st.markdown(res['diagnosis'])
                    
    elif "Weather" in action or "हवामान सल्ला" in action:
        st.markdown(f"### {selected_district} - {'आजचा हवामान अंदाज' if is_marathi else 'Weather Forecast'}")
        forecast = get_weather_forecast(19.75, 75.71)
        advisories = generate_weather_advisory(forecast)
        for adv in advisories:
            st.warning(f"**{adv['title']}**\n\n{adv['message']}")
            
        st.dataframe(pd.DataFrame(forecast), use_container_width=True)
        
    elif "Mandi Prices" in action or "बाजारभाव" in action:
        st.markdown(f"### {'आजचे बाजारभाव (₹ प्रति क्विंटल)' if is_marathi else 'Today Mandi Market Prices (₹/Quintal)'}")
        df_p = get_mandi_price_history("wheat")
        st.dataframe(df_p, use_container_width=True)
        
    elif "Sarthi" in action or "कृषी-सारथी" in action:
        st.markdown(f"### {'कृषी-सारथी व्हॉट्सॲप बॉट (आवाज किंवा मजकूर)' if is_marathi else 'Krishi-Sarthi Voice / Text Assistant'}")
        
        user_id = usr.get('id', 1)
        session_id = "easy_mode_session"
        
        chat_history = load_chat_history(user_id, session_id)
        if not chat_history:
            save_chat_message(user_id, session_id, "assistant", "नमस्कार शेतकरी बंधू! मी कृषी-सारथी आहे. पिकाबद्दल काय विचारायचे आहे?")
            chat_history = load_chat_history(user_id, session_id)
            
        # Voice simulation button
        if st.button("🎤 बोलून प्रश्न विचारण्यासाठी क्लिक करा (Simulate Voice Query)"):
            voice_sim_q = "गेहू में पीला रतुआ लग रहा है क्या करूँ?"
            save_chat_message(user_id, session_id, "user", voice_sim_q + " (Voice Audio Note 🎙️)")
            reply = get_krishisarthi_response(voice_sim_q, lang_code)
            save_chat_message(user_id, session_id, "assistant", reply)
            st.rerun()
            
        user_q = st.text_input("किंवा येथे प्रश्न लिहा (Type your question here)...")
        if st.button("पाठवा (Send)", type="primary"):
            if user_q:
                save_chat_message(user_id, session_id, "user", user_q)
                reply = get_krishisarthi_response(user_q, lang_code)
                save_chat_message(user_id, session_id, "assistant", reply)
                st.rerun()
                
        for chat in load_chat_history(user_id, session_id):
            if chat["role"] == "user":
                st.markdown(f'<div style="background-color: #e8f5e9; padding: 10px; border-radius: 10px; margin-bottom: 8px; text-align: right; color: #1b5e20;"><b>शेतकरी (Farmer):</b> {chat["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color: #f1f8e9; padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #2e7d32; color: #1b5e20;"><b>🤖 कृषी-सारथी (Krishi-Sarthi):</b><br>{chat["content"]}</div>', unsafe_allow_html=True)

