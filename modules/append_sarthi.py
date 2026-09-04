"""
    # -------------------------------------------------------------
    # TAB 7: Krishi-Sarthi WhatsApp / SMS Voice Bot Simulator
    # -------------------------------------------------------------
    with tabs[6]:
        st.markdown(f'<p class="main-header">💬 {t.get("nav_sarthi", "Krishi-Sarthi Bot")}</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Simulated WhatsApp & SMS voice/text assistant for low-bandwidth rural farmers.</p>', unsafe_allow_html=True)
        
        from modules.krishisarthi import get_krishisarthi_response
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 📱 Quick Voice / Text Prompts")
            st.markdown("Click any preset query to simulate a WhatsApp message from a farmer:")
            
            preset_queries = [
                "गेहू में पीला रतुआ लग रहा है क्या करूँ?",
                "धान में ब्लास्ट रोग का उपाय बताओ",
                "टोमॅटो पिकावर करपा रोगासाठी काय करावे?",
                "आज हवामान कसे राहील पाऊस पडेल का?",
                "गहू आणि सोयाबीनचे आजचे बाजारभाव काय आहेत?"
            ]
            
            selected_preset = None
            for pq in preset_queries:
                if st.button(f"💬 {pq}", key=f"btn_{pq}"):
                    selected_preset = pq
                    
        with col2:
            st.markdown("### 🤖 Krishi-Sarthi Chat Simulator")
            
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = [
                    {"role": "assistant", "content": "नमस्कार! मी कृषी-सारथी आहे. तुमच्या शेतीविषयी किंवा पिकाविषयी सांगा, मी मदत करेन. (Hello! I am Krishi-Sarthi. How can I assist your farm today?)"}
                ]
                
            if selected_preset:
                st.session_state["chat_history"].append({"role": "user", "content": selected_preset})
                reply = get_krishisarthi_response(selected_preset, lang_code)
                st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                
            user_input = st.text_input("Type your question in Marathi or English...", key="sarthi_input")
            if st.button("Send / पाठवा", key="send_sarthi"):
                if user_input:
                    st.session_state["chat_history"].append({"role": "user", "content": user_input})
                    reply = get_krishisarthi_response(user_input, lang_code)
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                    st.rerun()
                    
            # Display chat conversation
            for chat in st.session_state["chat_history"]:
                if chat["role"] == "user":
                    st.markdown(f"""
                    <div style="background-color: #e8f5e9; padding: 10px; border-radius: 10px; margin-bottom: 8px; text-align: right; color: #1b5e20;">
                        <b>शेतकरी (Farmer):</b> {chat['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: #f1f8e9; padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #2e7d32; color: #1b5e20;">
                        <b>🤖 कृषी-सारथी (Krishi-Sarthi):</b><br>{chat['content']}
                    </div>
                    """, unsafe_allow_html=True)
"""