"""
Krishi-Sarthi WhatsApp / SMS Voice Bot Simulator Module
Provides instant multilingual (Marathi & English) agronomic voice/text query responses.
"""

def get_krishisarthi_response(query, lang_code="mr"):
    """
    Simulates AI conversational advisory for common rural farming queries
    """
    query_lower = query.lower()
    
    responses = {
        "mr": {
            "default": "नमस्कार शेतकरी बंधू! तुमच्या पिकाच्या समस्येवर तज्ज्ञांचा सल्ला: वेळेवर पाणी द्या आणि योग्य खताचा वापर करा. अधिक माहितीसाठी तुमच्या जवळील कृषी अधिकाऱ्याशी संपर्क साधा.",
            "wheat": "🌾 **गहू पीक सल्ला:** पिकाला पिवळा रतुआ (Yellow Rust) झाल्यास प्रोपिकोनाजोल २५% ईसी (Propiconazole 25% EC) ची फवारणी करा. दाणे भरण्याच्या वेळेस (CRI stage) पहिले पाणी द्या.",
            "paddy": "🌾 **धान/तांदूळ सल्ला:** ब्लास्ट रोगाच्या नियंत्रणासाठी ट्रायसायक्लाझोल ७५% डब्ल्यूपी (Tricyclazole 75% WP) फवारा. शेतात पाणी साचू देऊ नका.",
            "tomato": "🍅 **टोमॅटो पीक सल्ला:** फळ पोखरणारी अळी किंवा करपा (Blight) रोखण्यासाठी मँकोझेब ७५% डब्ल्यूपी फवारा आणि नीम ऑइल वापरा.",
            "weather": "🌦️ **हवामान सल्ला:** पुढील ४८ तासांत पावसाची शक्यता आहे. त्यामुळे युरिया खताची फवारणी किंवा टॉप-ड्रेसिंग सध्या टाळा.",
            "price": "📈 **बाजारभाव सल्ला:** सद्यस्थितीत बाजार स्थिर आहे. तुमच्या पिकाची प्रत चांगली ठेवून हप्त्याहप्त्याने विक्री करा."
        },
        "en": {
            "default": "Hello Farmer! Krishi-Sarthi advisory: Ensure timely irrigation and balanced fertilizer application. Contact your local agricultural officer for specific district soil testing.",
            "wheat": "🌾 **Wheat Advisory:** If yellow rust is observed, spray Propiconazole 25% EC. Ensure 1st irrigation at CRI stage (21 days after sowing).",
            "paddy": "🌾 **Paddy Advisory:** For blast disease control, spray Tricyclazole 75% WP. Maintain adequate drainage during heavy rainfall.",
            "tomato": "🍅 **Tomato Advisory:** To prevent early blight and fruit borer, spray Mancozeb 75% WP and use Neem oil.",
            "weather": "🌦️ **Weather Advisory:** Rain expected in the next 48 hours. Please delay fertilizer top-dressing to prevent nutrient run-off.",
            "price": "📈 **Market Advisory:** Prices are stable. Consider phased selling to average out market volatility."
        }
    }
    
    lang_dict = responses.get(lang_code, responses["en"])
    
    if "wheat" in query_lower or "गेहू" in query_lower or "गहू" in query_lower:
        return lang_dict["wheat"]
    elif "paddy" in query_lower or "धान" in query_lower or "तांदूळ" in query_lower:
        return lang_dict["paddy"]
    elif "tomato" in query_lower or "टोमॅटो" in query_lower:
        return lang_dict["tomato"]
    elif "weather" in query_lower or "पाऊस" in query_lower or "हवामान" in query_lower:
        return lang_dict["weather"]
    elif "price" in query_lower or "भाव" in query_lower or "किमत" in query_lower:
        return lang_dict["price"]
    else:
        return lang_dict["default"]
