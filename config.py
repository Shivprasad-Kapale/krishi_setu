"""
Configuration, Localization, and Constants for KrishiSetu Platform
"""

APP_NAME = "KrishiSetu | कृषि सेतु"
APP_TAGLINE = "Market-Linked Crop Planning, Rural Advisory & Agricultural Operations Platform"

# Indian States & Major Agricultural Districts
INDIAN_LOCATIONS = {
    "Maharashtra": {
        "districts": [
            "Ahmednagar", "Akola", "Amravati", "Aurangabad", 
            "Beed", "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", 
            "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", 
            "Mumbai City", "Mumbai Suburban", "Nagpur", "Nanded", "Nandurbar", 
            "Nashik", "Osmanabad", "Palghar", "Parbhani", "Pune", 
            "Raigad", "Ratnagiri", "Sangli", "Satara", "Sindhudurg", "Solapur", 
            "Thane", "Wardha", "Washim", "Yavatmal"
        ],
        "lat": 19.7515, "lon": 75.7139
    },
    "Punjab": {
        "districts": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Firozpur"],
        "lat": 31.1471, "lon": 75.3412
    },
    "Uttar Pradesh": {
        "districts": ["Varanasi", "Lucknow", "Agra", "Kanpur", "Prayagraj", "Meerut", "Gorakhpur"],
        "lat": 26.8467, "lon": 80.9462
    },
    "Madhya Pradesh": {
        "districts": ["Indore", "Bhopal", "Ujjain", "Jabalpur", "Gwalior", "Hoshangabad", "Sagar"],
        "lat": 22.9734, "lon": 78.6569
    },
    "Karnataka": {
        "districts": ["Belagavi", "Dharwad", "Mysuru", "Shivamogga", "Tumakuru", "Vijayapura"],
        "lat": 15.3173, "lon": 75.7139
    },
    "Gujarat": {
        "districts": ["Rajkot", "Surat", "Ahmedabad", "Junagadh", "Mehsana", "Vadodara", "Bhavnagar"],
        "lat": 22.2587, "lon": 71.1924
    },
    "Rajasthan": {
        "districts": ["Jaipur", "Kota", "Jodhpur", "Bikaner", "Sri Ganganagar", "Alwar"],
        "lat": 27.0238, "lon": 74.2179
    },
    "Haryana": {
        "districts": ["Karnal", "Hisar", "Ambala", "Rohtak", "Sirsa", "Kurukshetra"],
        "lat": 29.0588, "lon": 76.0856
    },
    "Andhra Pradesh": {
        "districts": ["Guntur", "Krishna", "Kurnool", "West Godavari", "Chittoor", "Anantapur"],
        "lat": 15.9129, "lon": 79.7400
    },
    "Tamil Nadu": {
        "districts": ["Thanjavur", "Coimbatore", "Madurai", "Salem", "Erode", "Tiruchirappalli"],
        "lat": 11.1271, "lon": 78.6569
    },
    "West Bengal": {
        "districts": ["Bardhaman", "Murshidabad", "Hooghly", "Nadia", "Bankura"],
        "lat": 22.9868, "lon": 87.8550
    },
    "Bihar": {
        "districts": ["Patna", "Muzaffarpur", "Gaya", "Bhagalpur", "Samastipur"],
        "lat": 25.0961, "lon": 85.3131
    }
}

SOIL_TYPES = [
    "Alluvial Soil (Gaalachi Mati)",
    "Black Soil / Regur (Kali Mati)",
    "Red & Yellow Soil (Tambadi Mati)",
    "Laterite Soil (Jambhari Mati)",
    "Sandy / Arid Soil (Valuchi Mati)",
    "Clay Loam (Chikan Domat Mati)"
]

# Localization Dictionary (English, Hindi, Marathi - No Emojis)
TRANSLATIONS = {
    "en": {
        "title": "KrishiSetu",
        "tagline": "Market-Linked Crop Planning & Agricultural Operations",
        "nav_planner": "Smart Crop Planner",
        "nav_mandi": "Mandi Price Forecast",
        "nav_doctor": "AI Crop Doctor",
        "nav_weather": "Weather & Farm Advisory",
        "nav_ops": "Operations & Task Tracker",
        "nav_market": "Direct Marketplace & Contracts",
        "nav_sarthi": "Krishi-Sarthi Bot",
        "state": "Select State",
        "district": "Select District",
        "soil_type": "Soil Type",
        "land_size": "Land Area (Acres)",
        "season": "Current / Upcoming Season",
        "water_source": "Irrigation Availability",
        "budget": "Investment Budget per Acre (₹)",
        "btn_plan": "Analyze & Recommend Crops",
        "best_roi": "Estimated Highest ROI Crop",
        "market_linkage": "Market Demand Trend",
        "mandi_best_month": "Recommended Best Selling Month",
        "disease_detect": "Upload or Capture Leaf Photo",
        "weather_risk": "7-Day Farm Risk Index",
        "buyer_board": "Contract Farming & Buyer Requests",
        "farmer_listing": "Post Your Prospective Harvest",
        
        # Personas
        "persona_farmer": "Farmer / Producer",
        "persona_fpo": "FPO / Cooperative",
        "persona_buyer": "Agribusiness / Retail Buyer",
        "persona_agronomist": "Agronomist / Extension Officer",
        "persona_researcher": "Researcher / Policy Maker",

        # Section specific translations
        "mandi_title": "Mandi Price Forecast & Analytics",
        "mandi_subtitle": "Historical mandi prices, seasonal trends, and 3-month AI price forecasts for optimal selling decisions.",
        "mandi_select_commodity": "Select Commodity for Price Analysis",
        "market_intelligence": "Market Intelligence",
        "optimal_selling_window": "Optimal Selling Window:",
        "market_outlook": "Market Outlook:",
        "storage_rec": "Storage Recommendation: Consider silo / warehouse storage if market price is within 5% of MSP during harvest peak.",
        
        "doctor_title": "AI Crop Doctor (Disease Diagnosis)",
        "doctor_subtitle": "Upload or take a photo of a diseased leaf to instantly diagnose pests/pathogens and get organic/chemical remedies.",
        "uploaded_sample": "Uploaded Leaf Sample",
        "analyzing": "Analyzing leaf pathology with AI...",
        "doctor_tip": "Tip: You can upload a photo of wheat rust, rice blast, tomato blight, or cotton bollworm damage for instant AI diagnosis.",
        
        "weather_title": "Weather & Farm Advisory",
        "weather_subtitle": "Hyper-local 7-day meteorological forecast and automated operational alerts for **{district}, {state}**.",
        "auto_advisories": "Automated Agronomic Weather Advisories",
        "meteorological_outlook": "7-Day Meteorological Outlook",
        
        "ops_title": "Operations & Task Tracker",
        "ops_subtitle": "Automated crop calendar and task checklist for irrigation, fertilizer application, weeding, and harvest.",
        "select_active_crop": "Select Active Crop for Operations",
        "standard_schedule": "Standard Schedule for",
        "completed": "Completed",
        "pest_management": "Common Pest & Disease Management Protocols",
        
        "market_title": "Direct Marketplace & Contracts",
        "market_subtitle": "Direct buyer-farmer pre-contracts, FPO bulk demand listings, and market linkage board.",
        "farmer_listings_header": "Farmer Harvest Listings",
        "buyer_board_header": "Buyer Demand & Contract Board",
        "publish_listing": "Publish Listing",
        "publish_demand": "Publish Buyer Demand"
    },
    "hi": {
        "title": "कृषि सेतु",
        "tagline": "बाजार-आधारित फसल योजना, ग्रामीण सलाह और कृषि परिचालन मंच",
        "nav_planner": "स्मार्ट फसल योजनाकार",
        "nav_mandi": "मंडी भाव पूर्वानुमान",
        "nav_doctor": "एआई फसल डॉक्टर",
        "nav_weather": "मौसम और कृषि सलाह",
        "nav_ops": "कृषि परिचालन और कार्य सूची",
        "nav_market": "सीधा बाजार और अनुबंध खेती",
        "nav_sarthi": "कृषि-सारथी बॉट",
        "state": "राज्य चुनें",
        "district": "जिला चुनें",
        "soil_type": "मिट्टी का प्रकार",
        "land_size": "जमीन का क्षेत्रफल (एकड़)",
        "season": "मौसम (खरीफ/रबी/जायद)",
        "water_source": "सिंचाई की उपलब्धता",
        "budget": "प्रति एकड़ निवेश बजट (₹)",
        "btn_plan": "फसल विश्लेषण और सिफारिश देखें",
        "best_roi": "अनुमानित सर्वाधिक लाभ वाली फसल",
        "market_linkage": "बाजार मांग का रुझान",
        "mandi_best_month": "फसल बेचने का सर्वोत्तम महीना",
        "disease_detect": "पत्ती की फोटो अपलोड करें या खींचें",
        "weather_risk": "7-दिवसीय कृषि जोखिम सूचकांक",
        "buyer_board": "अनुबंध खेती और खरीदार मांग",
        "farmer_listing": "अपनी आगामी फसल सूचीबद्ध करें",
        
        # Personas
        "persona_farmer": "किसान / उत्पादक",
        "persona_fpo": "एफपीओ / सहकारिता",
        "persona_buyer": "कृषि व्यवसाय / खरीदार",
        "persona_agronomist": "कृषि विज्ञानी / अधिकारी",
        "persona_researcher": "शोधकर्ता / नीति निर्माता",

        # Section specific translations
        "mandi_title": "मंडी भाव पूर्वानुमान और विश्लेषण",
        "mandi_subtitle": "ऐतिहासिक मंडी भाव, मौसमी रुझान और इष्टतम बिक्री निर्णयों के लिए 3 महीने का एआई पूर्वानुमान।",
        "mandi_select_commodity": "मूल्य विश्लेषण के लिए वस्तु चुनें",
        "market_intelligence": "बाजार बुद्धिमत्ता",
        "optimal_selling_window": "सर्वोत्तम बिक्री विंडो:",
        "market_outlook": "बाजार दृष्टिकोण:",
        "storage_rec": "भंडारण अनुशंसा: यदि कटाई के चरम पर बाजार मूल्य एमएसपी के 5% के भीतर है, तो साइलो/वेयरहाउस भंडारण पर विचार करें।",
        
        "doctor_title": "एआई फसल डॉक्टर (रोग निदान)",
        "doctor_subtitle": "कीटों/रोगाणुओं का तुरंत निदान करने और जैविक/रासायनिक उपचार प्राप्त करने के लिए रोगग्रस्त पत्ते की फोटो अपलोड करें।",
        "uploaded_sample": "अपलोड किया गया पत्ता नमूना",
        "analyzing": "एआई के साथ पादप रोग विज्ञान का विश्लेषण किया जा रहा है...",
        "doctor_tip": "सुझाव: त्वरित एआई निदान के लिए आप गेहूं, धान, टमाटर या कपास के नुकसान की तस्वीर अपलोड कर सकते हैं।",
        
        "weather_title": "मौसम और कृषि सलाह",
        "weather_subtitle": "**{district}, {state}** के लिए हाइपर-लोकल 7-दिवसीय मौसम पूर्वानुमान और स्वचालित परिचालन अलर्ट।",
        "auto_advisories": "स्वचालित कृषि मौसम सलाह",
        "meteorological_outlook": "7-दिवसीय मौसम संबंधी दृष्टिकोण",
        
        "ops_title": "कृषि परिचालन और कार्य ट्रैकर",
        "ops_subtitle": "सिंचाई, उर्वरक अनुप्रयोग, निराई और कटाई के लिए स्वचालित फसल कैलेंडर और कार्य चेकलिस्ट।",
        "select_active_crop": "संचालन के लिए सक्रिय फसल चुनें",
        "standard_schedule": "के लिए मानक अनुसूची",
        "completed": "पूर्ण हुआ",
        "pest_management": "सामान्य कीट और रोग प्रबंधन प्रोटोकॉल",
        
        "market_title": "प्रत्यक्ष बाजार और अनुबंध",
        "market_subtitle": "प्रत्यक्ष खरीदार-किसान पूर्व-अनुबंध, एफपीओ थोक मांग सूची और बाजार लिंकेज बोर्ड।",
        "farmer_listings_header": "किसान फसल लिस्टिंग",
        "buyer_board_header": "खरीदार मांग और अनुबंध बोर्ड",
        "publish_listing": "लिस्टिंग प्रकाशित करें",
        "publish_demand": "खरीदार मांग प्रकाशित करें"
    },
    "mr": {
        "title": "कृषिसेतू",
        "tagline": "बाजार-संलग्न पीक नियोजन, ग्रामीण सल्ला आणि शेती परिचालन मंच",
        "nav_planner": "स्मार्ट पीक नियोजक",
        "nav_mandi": "बाजारभाव अंदाज (मंडी)",
        "nav_doctor": "एआय पीक डॉक्टर",
        "nav_weather": "हवामान आणि कृषी सल्ला",
        "nav_ops": "शेती कार्य ट्रॅकर",
        "nav_market": "थेट बाजारपेठ आणि करार",
        "nav_sarthi": "कृषि-सारथी बॉट",
        "state": "राज्य निवडा",
        "district": "जिल्हा निवडा",
        "soil_type": "मातीचा प्रकार",
        "land_size": "जमिनीचे क्षेत्रफळ (एकर)",
        "season": "हंगाम (खरीप/रबी/उन्हाळी)",
        "water_source": "सिंचनाची उपलब्धता",
        "budget": "प्रति एकर गुंतवणूक बजेट (₹)",
        "btn_plan": "पीक विश्लेषण आणि शिफारस पहा",
        "best_roi": "सर्वाधिक नफा देणारे पीक",
        "market_linkage": "बाजार मागणीचा कल",
        "mandi_best_month": "पीक विकण्याचा सर्वोत्तम महिना",
        "disease_detect": "पानाचे चित्र अपलोड करा किंवा काढा",
        "weather_risk": "७-दिवसांचा कृषी जोखीम निर्देशांक",
        "buyer_board": "करार शेती आणि खरेदीदार मागण्या",
        "farmer_listing": "तुमचे आगामी पीक बाजारपेठेत नोंदवा",
        
        # Personas
        "persona_farmer": "शेतकरी / उत्पादक",
        "persona_fpo": "एफपीओ / सहकार संस्था",
        "persona_buyer": "कृषी व्यवसाय / खरेदीदार",
        "persona_agronomist": "कृषी तज्ज्ञ / अधिकारी",
        "persona_researcher": "संशोधक / धोरणकर्ता",

        # Section specific translations
        "mandi_title": "बाजारभाव अंदाज आणि विश्लेषण",
        "mandi_subtitle": "ऐतिहासिक बाजारभाव, हंगामी कल आणि नफा मिळवण्यासाठी ३ महिन्यांचे एआय अंदाज.",
        "mandi_select_commodity": "भाव विश्लेषणासाठी पीक निवडा",
        "market_intelligence": "बाजार बुद्धिमत्ता",
        "optimal_selling_window": "सर्वोत्तम विक्री कालावधी:",
        "market_outlook": "बाजार दृष्टिकोन:",
        "storage_rec": "साठवणूक सल्ला: जर बाजारभाव काढणीच्या हंगामातील किमान आधारभूत किंमतीच्या (MSP) ५% च्या आत असेल, तर कोल्ड स्टोरेज किंवा वेअरहाऊसमध्ये साठवणूक करण्याचा विचार करा.",
        
        "doctor_title": "एआय पीक डॉक्टर (रोग निदान)",
        "doctor_subtitle": "रोगांचे निदान करण्यासाठी आणि सेंद्रिय/रासायनिक उपचारांची माहिती मिळवण्यासाठी पानाचा फोटो अपलोड करा.",
        "uploaded_sample": "अपलोड केलेले पानाचे नमुने",
        "analyzing": "एआय द्वारे पानांच्या रोगाचे विश्लेषण करत आहे...",
        "doctor_tip": "टीप: तुम्ही गहू, तांदूळ, टोमॅटो किंवा कपाशीवरील रोगांच्या निदानासाठी पानाचा फोटो अपलोड करू शकता.",
        
        "weather_title": "हवामान आणि कृषी सल्ला",
        "weather_subtitle": "**{district}, {state}** साठी ७-दिवसांचा हवामानाचा अंदाज आणि शेतीसाठी तातडीचे इशारे.",
        "auto_advisories": "स्वयंचलित कृषी हवामान सल्ले",
        "meteorological_outlook": "७-दिवसांचा हवामान अंदाज",
        
        "ops_title": "शेती कार्य आणि शेड्युल ट्रॅकर",
        "ops_subtitle": "सिंचन, खते देणे, खुरपणी आणि काढणीसाठी स्वयंचलित पीक कॅलेंडर आणि कार्य सूची.",
        "select_active_crop": "सक्रिय पिकाची निवड करा",
        "standard_schedule": "येथे मानक वेळापत्रक:",
        "completed": "पूर्ण झाले",
        "pest_management": "कीटक आणि रोग व्यवस्थापन",
        
        "market_title": "थेट बाजारपेठ आणि करार शेती",
        "market_subtitle": "शेतकरी-खरेदीदार पूर्व-करार, एफपीओ (FPO) मोठ्या प्रमाणावर मागणी सूची आणि थेट बाजारपेठ.",
        "farmer_listings_header": "शेतकऱ्यांच्या पीक नोंदणी (Listings)",
        "buyer_board_header": "खरेदीदार मागणी आणि करार फलक",
        "publish_listing": "बाजारपेठेत नोंदवा",
        "publish_demand": "खरेदीदार मागणी प्रकाशित करा"
    }
}
