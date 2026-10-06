"""
Farmer Community Module (शेतकरी समुदाय मंच) for KrishiSetu
Provides:
- Multi-lingual Farmer & Expert Feed with Likes, Nested Replies, Voice Notes, and Web Speech (Audio)
- Crop & Regional Specialized Groups (FPO Circles, Grape Growers, Machinery, Dairy, etc.)
- Hyperlocal Real-Time Agricultural & Pest Alerts with Severity Indicators
- Farmer Reputation, Karma Points, Activity Stats, and Achievement Badges
- Direct Posting with Image & Voice-to-Text simulation
"""

import json
import html
import os
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

COMMUNITY_DATA_FILE = "community_data.json"

COMMUNITY_COPY = {
    "en": {
        "ask_share": "Ask or share with farmers",
        "post_hint": "Describe what is happening on your farm. Clear details help others give useful advice.",
        "category": "Topic",
        "post_text": "Your question or tip",
        "post_placeholder": "For example: Yellow spots have appeared on my tomato leaves. What should I check?",
        "crop_symbol": "Crop symbol",
        "read_aloud_hint": "You can use the read-aloud button on your post after publishing.",
        "post_button": "Publish to community",
        "empty_post": "Write a message before publishing.",
        "published": "Your post is live.",
        "feed_title": "Recent farmer discussions",
        "search": "Search discussions",
        "search_placeholder": "Search crops, questions or farmers",
        "topic": "Topic",
        "all_topics": "All topics",
        "nearby": "Show posts from my area",
        "no_results": "No discussions match these filters. Try another topic or start a discussion.",
        "reply": "Write a reply",
        "reply_button": "Post reply",
        "reply_empty": "Write a reply before sending.",
        "reply_added": "Your reply was added."
    },
    "hi": {
        "ask_share": "किसानों से सवाल पूछें या जानकारी साझा करें",
        "post_hint": "खेत में क्या हो रहा है, साफ़-साफ़ लिखें। इससे दूसरे किसान बेहतर सलाह दे पाएँगे।",
        "category": "विषय",
        "post_text": "आपका सवाल या सुझाव",
        "post_placeholder": "उदाहरण: टमाटर की पत्तियों पर पीले धब्बे हैं। मुझे क्या देखना चाहिए?",
        "crop_symbol": "फसल का चिन्ह",
        "read_aloud_hint": "पोस्ट करने के बाद उसे सुनने के लिए पढ़कर सुनाएँ बटन का उपयोग करें।",
        "post_button": "समुदाय में पोस्ट करें",
        "empty_post": "पोस्ट करने से पहले संदेश लिखें।",
        "published": "आपकी पोस्ट प्रकाशित हो गई।",
        "feed_title": "किसानों की नई चर्चाएँ",
        "search": "चर्चा खोजें",
        "search_placeholder": "फसल, सवाल या किसान खोजें",
        "topic": "विषय",
        "all_topics": "सभी विषय",
        "nearby": "मेरे इलाके की पोस्ट दिखाएँ",
        "no_results": "इन फ़िल्टर में चर्चा नहीं मिली। दूसरा विषय चुनें या नई चर्चा शुरू करें।",
        "reply": "जवाब लिखें",
        "reply_button": "जवाब भेजें",
        "reply_empty": "भेजने से पहले जवाब लिखें।",
        "reply_added": "आपका जवाब जोड़ दिया गया।"
    },
    "mr": {
        "ask_share": "शेतकऱ्यांशी प्रश्न विचारा किंवा माहिती शेअर करा",
        "post_hint": "शेतात काय घडत आहे ते स्पष्ट लिहा. त्यामुळे इतर शेतकरी योग्य सल्ला देऊ शकतील.",
        "category": "विषय",
        "post_text": "तुमचा प्रश्न किंवा सल्ला",
        "post_placeholder": "उदा. टोमॅटोच्या पानांवर पिवळे डाग दिसत आहेत. काय तपासावे?",
        "crop_symbol": "पिकाचे चिन्ह",
        "read_aloud_hint": "पोस्ट केल्यानंतर ती ऐकण्यासाठी मोठ्याने ऐका बटण वापरा.",
        "post_button": "समुदायात पोस्ट करा",
        "empty_post": "पोस्ट करण्यापूर्वी संदेश लिहा.",
        "published": "तुमची पोस्ट प्रकाशित झाली.",
        "feed_title": "शेतकऱ्यांच्या अलीकडील चर्चा",
        "search": "चर्चा शोधा",
        "search_placeholder": "पीक, प्रश्न किंवा शेतकरी शोधा",
        "topic": "विषय",
        "all_topics": "सर्व विषय",
        "nearby": "माझ्या परिसरातील पोस्ट दाखवा",
        "no_results": "या फिल्टरमध्ये चर्चा सापडली नाही. दुसरा विषय निवडा किंवा नवी चर्चा सुरू करा.",
        "reply": "उत्तर लिहा",
        "reply_button": "उत्तर पाठवा",
        "reply_empty": "पाठवण्यापूर्वी उत्तर लिहा.",
        "reply_added": "तुमचे उत्तर जोडले गेले."
    }
}


def render_html(html_str):
    """
    Renders raw HTML safely in Streamlit without triggering Markdown indented code block parsing.
    Strips leading/trailing indentation from each line and joins without empty lines.
    """
    clean_lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    st.markdown("".join(clean_lines), unsafe_allow_html=True)

def get_initial_community_data():
    return {
        "posts": [
            {
                "id": 1,
                "author": "Ramesh Patil (रमेश पाटील)",
                "user_id": "seed_1",
                "village": "Nashik, Maharashtra",
                "category": "Grape / Horticulture",
                "time": "10 minutes ago",
                "is_expert": False,
                "avatar_initial": "र",
                "avatar_color": "linear-gradient(135deg, #8d6e63, #5d4037)",
                "text": {
                    "en": "My grape leaves are turning yellow with pale spots. Does anyone know the cause? Attaching photo.",
                    "hi": "मेरे अंगूर के पत्ते पीले पड़ रहे हैं और धब्बे दिख रहे हैं। क्या किसी को कारण पता है? फोटो संलग्न है।",
                    "mr": "माझ्या द्राक्षाची पाने पिवळी पडत आहेत आणि त्यावर फिकट डाग दिसत आहेत. कुणाला कारण माहीत आहे का? फोटो पाठवत आहे."
                },
                "image_emoji": "🍇",
                "image_bg": "linear-gradient(135deg, #fff3e0, #ffe0b2)",
                "voice_note": False,
                "likes": 14,
                "liked_by": [],
                "replies": [
                    {
                        "id": 101,
                        "author": "Sunil Jadhav (सुनील जाधव)",
                        "role": "Farmer",
                        "time": "8m ago",
                        "text": "मॅग्नेशियम सल्फेट (Magnesium Sulphate) 5 ग्रॅम/लिटर फवारून पहा — माझ्या द्राक्ष बागेत चांगला फरक पडला होता."
                    },
                    {
                        "id": 102,
                        "author": "Dr. Sunil Kulkarni",
                        "role": "Agronomist / Expert",
                        "time": "5m ago",
                        "text": "Check soil electrical conductivity and nitrogen wash out due to excessive rain. Apply foliar zinc and magnesium."
                    }
                ]
            },
            {
                "id": 2,
                "author": "Dr. Sunil Kulkarni (कृषी विज्ञान केंद्र)",
                "user_id": "seed_2",
                "village": "KVK Pune / Nashik Belt",
                "category": "Pest & Disease Advisory",
                "time": "1 hour ago",
                "is_expert": True,
                "avatar_initial": "K",
                "avatar_color": "linear-gradient(135deg, #1565c0, #0d47a1)",
                "text": {
                    "en": "⚠️ Alert: Tomato early blight and sucking pest incidence rising in Pune & Nashik. Spray Mancozeb 75% WP @ 2.5g/Litre. Repeat after 7-10 days if cloudy weather persists.",
                    "hi": "⚠️ चेतावनी: पुणे और नासिक जिले में टमाटर पर झुलसा रोग और रस चूसक कीट बढ़ रहे हैं। मैंकोजेब 75% WP @ 2.5 ग्राम/लीटर का छिड़काव करें।",
                    "mr": "⚠️ तातडीची सूचना: पुणे आणि नाशिक भागात टोमॅटो पिकावर करपा आणि रसशोषक किडींचा प्रादुर्भाव वाढत आहे. मॅन्कोझेब 75% WP — 2.5 ग्रॅम/लिटर फवारणी करा. ढगाळ हवामान असल्यास ७ दिवसांनी पुनरावृत्ती करा."
                },
                "image_emoji": "🍅",
                "image_bg": "linear-gradient(135deg, #ffebee, #ffcdd2)",
                "voice_note": False,
                "likes": 56,
                "liked_by": [],
                "replies": [
                    {
                        "id": 201,
                        "author": "Vikas Shinde",
                        "role": "Farmer",
                        "time": "30m ago",
                        "text": "धन्यवाद डॉक्टर साहेब, योग्य वेळी माहिती दिली!"
                    }
                ]
            },
            {
                "id": 3,
                "author": "Sunita Deshmukh (सुनीता देशमुख)",
                "user_id": "seed_3",
                "village": "Karad, Satara",
                "category": "Organic Farming (सेंद्रिय शेती)",
                "time": "3 hours ago",
                "is_expert": False,
                "avatar_initial": "सु",
                "avatar_color": "linear-gradient(135deg, #ad1457, #6a1b3d)",
                "text": {
                    "en": "I am sharing my zero-budget organic Dashaparni ark recipe for fall armyworm and aphids. Listen to my audio voice note.",
                    "hi": "मैं फॉल आर्मीवर्म और एफिड्स के लिए अपनी दशपर्णी अर्क की प्राकृतिक विधि साझा कर रही हूँ — वॉइस नोट सुनें।",
                    "mr": "मी लष्करी अळी व मावा किडीसाठी घरगुती दशपर्णी अर्क आणि निंबोळी अर्क बनवण्याची सोपी पद्धत सांगत आहे — ऑडिओ व्हॉइस नोट ऐका."
                },
                "image_emoji": "🌿",
                "image_bg": "linear-gradient(135deg, #e8f5e9, #c8e6c9)",
                "voice_note": True,
                "voice_duration": "0:28",
                "likes": 42,
                "liked_by": [],
                "replies": []
            },
            {
                "id": 4,
                "author": "Bajrang Jadhav (बजरंग जाधव)",
                "user_id": "seed_4",
                "village": "Latur APMC",
                "category": "Mandi Market Buzz",
                "time": "5 hours ago",
                "is_expert": False,
                "avatar_initial": "ब",
                "avatar_color": "linear-gradient(135deg, #ef6c00, #e65100)",
                "text": {
                    "en": "Soybean touched ₹4,850/quintal in Latur APMC today due to strong oil mill buying. Might test ₹4,920 tomorrow. Plan dispatches accordingly.",
                    "hi": "आज लातूर मंडी में सोयाबीन ₹4,850/क्विंटल बिका। तेल मिलों की मजबूत खरीद से कल ₹4,920 तक जा सकता है।",
                    "mr": "आज लातूर मार्केट यार्डात सोयाबीनचा भाव ₹4,850/क्विंटल झाला. तेलाच्या कारखान्यांकडून मागणी वाढल्याने उद्या ₹4,920 पर्यंत जाण्याची शक्यता आहे. काढणी झालेल्यांनी विक्रीचा विचार करा."
                },
                "image_emoji": "💰",
                "image_bg": "linear-gradient(135deg, #fff8e1, #ffecb3)",
                "voice_note": False,
                "likes": 78,
                "liked_by": [],
                "replies": [
                    {
                        "id": 401,
                        "author": "Anand Patil",
                        "role": "Trader / Farmer",
                        "time": "2h ago",
                        "text": "अकोला आणि वाशीम बाजारातही ₹50 ची सुधारणा आहे."
                    }
                ]
            }
        ],
        "groups": [
            {
                "id": "g1",
                "name": {"mr": "नाशिक जिल्हा शेतकरी", "hi": "नाशिक जिला किसान संघ", "en": "Nashik District Farmers"},
                "desc": {"mr": "नाशिक, दिंडोरी, निफाड परिसरातील भाजीपाला व कांदा उत्पादक", "hi": "नाशिक क्षेत्र के सब्जी और प्याज उत्पादक", "en": "Vegetable & Onion growers in Nashik region"},
                "category": "Regional",
                "icon": "📍",
                "bg": "#e8f5e9",
                "members": 1240,
                "joined_by": ["seed_1", "admin"]
            },
            {
                "id": "g2",
                "name": {"mr": "द्राक्ष उत्पादक गट (Maharashtra)", "hi": "अंगूर उत्पादक समूह", "en": "Grape Growers Circle"},
                "desc": {"mr": "निर्यातक्षम द्राक्ष बागायतदार आणि छाटणी तंत्रज्ञान", "hi": "निर्यात गुणवत्ता अंगूर और छंटाई तकनीक", "en": "Export quality table grapes, canopy & pest care"},
                "category": "Crop Specific",
                "icon": "🍇",
                "bg": "#f3e5f5",
                "members": 612,
                "joined_by": ["seed_1"]
            },
            {
                "id": "g3",
                "name": {"mr": "सेंद्रिय शेती व विषमुक्त अन्न मंडळ", "hi": "जैविक खेती मंडल", "en": "Organic Farming & Permaculture"},
                "desc": {"mr": "जीवामृत, घनजीवामृत आणि सेंद्रिय प्रमाणीकरण मार्गदर्शन", "hi": "जीवामृत और प्राकृतिक खेती सलाह", "en": "Zero budget natural farming, bio-fertilizers & certification"},
                "category": "Practices",
                "icon": "🌿",
                "bg": "#e0f2f1",
                "members": 890,
                "joined_by": ["seed_3"]
            },
            {
                "id": "g4",
                "name": {"mr": "ट्रॅक्टर व अवजारे भाडे नेटवर्क", "hi": "ट्रैक्टर एवं कृषि यंत्र किराया", "en": "Tractor & Farm Implements Sharing"},
                "desc": {"mr": "रोटाव्हेटर, हार्वेस्टर व नांगरणीसाठी शेतकरी-ते-शेतकरी भाडे सेवा", "hi": "रोटावेटर व हार्वेस्टर शेयरिंग नेटवर्क", "en": "Peer-to-peer rental for rotavators, drones & harvesters"},
                "category": "Machinery",
                "icon": "🚜",
                "bg": "#fff3e0",
                "members": 348,
                "joined_by": []
            },
            {
                "id": "g5",
                "name": {"mr": "दुग्ध व्यवसाय व गोपालन गट", "hi": "डेयरी एवं पशुपालन समूह", "en": "Dairy & Livestock Circle"},
                "desc": {"mr": "गायी-म्हशींचे आरोग्य, संतुलित पशुखाद्य व दूध दर चर्चा", "hi": "पशु आहार, दूध दर और टीकाकरण जानकारी", "en": "Cattle nutrition, silage preparation & milk yield"},
                "category": "Allied Agri",
                "icon": "🐄",
                "bg": "#fce4ec",
                "members": 475,
                "joined_by": []
            },
            {
                "id": "g6",
                "name": {"mr": "टोमॅटो व भाजीपाला उत्पादक संघ", "hi": "टमाटर व सब्जी उत्पादक मंच", "en": "Tomato & Vegetable Growers"},
                "desc": {"mr": "नर्सरी रोपे, मल्चिंग, ठिबक व थेट खरेदीदार समन्वय", "hi": "मल्चिंग, ड्रिप और बाजार भाव समन्वय", "en": "Protected cultivation, seedling care & mandi linkage"},
                "category": "Crop Specific",
                "icon": "🍅",
                "bg": "#ffebee",
                "members": 730,
                "joined_by": []
            }
        ],
        "alerts": [
            {
                "id": 1,
                "type": "red",
                "icon": "🐛",
                "title": {"mr": "करपा रोग प्रादुर्भाव (Blight Outbreak)", "hi": "झुलसा रोग प्रकोप", "en": "Blight & Pest Outbreak"},
                "desc": {
                    "mr": "तुमच्या तालुक्यापासून १० किमी अंतरावर टोमॅटो आणि मिरचीवर करपा रोगाची नोंद झाली आहे. पानांवर काळे ठिपके दिसताच तात्काळ बुरशीनाशक फवारणी करा.",
                    "hi": "आपके क्षेत्र से 10 किमी दूर टमाटर व मिर्च पर झुलसा देखा गया है। तुरंत सतर्क रहें।",
                    "en": "Tomato early blight reported within 10 km of current cluster. Inspect foliage immediately."
                },
                "time": "2 hours ago",
                "district": "Nashik",
                "urgency": "High"
            },
            {
                "id": 2,
                "type": "amber",
                "icon": "🌧️",
                "title": {"mr": "अवकाळी पावसाचा व वादळी वाऱ्याचा इशारा", "hi": "बारिश और आंधी की चेतावनी", "en": "Rain & Thunderstorm Warning"},
                "desc": {
                    "mr": "पुढील ४८ तासांत विजांच्या कडकडाटासह ३०-५० मिमी पावसाची शक्यता. शेतात पाणी साचू देऊ नका आणि खत देणे आजच टाळा.",
                    "hi": "अगले 48 घंटों में तेज बारिश संभव। जल निकासी की व्यवस्था करें।",
                    "en": "30-50mm rainfall forecast over next 48 hrs. Clear drainage channels and postpone spray operations."
                },
                "time": "4 hours ago",
                "district": "All Maharashtra",
                "urgency": "Medium"
            },
            {
                "id": 3,
                "type": "green",
                "icon": "💰",
                "title": {"mr": "बाजारभाव तेजी (Mandi Price Surge)", "hi": "मंडी भाव में उछाल", "en": "Commodity Price Surge Alert"},
                "desc": {
                    "mr": "सोयाबीन आणि हरभरा भावात गेल्या ४ दिवसांत ₹१५०-₹२०० प्रति क्विंटल वाढ झाली आहे. चांगला दर मिळण्याची सुवर्णसंधी.",
                    "hi": "सोयाबीन और चने के भाव में अच्छी तेजी देखी जा रही है।",
                    "en": "Soybean and Bengal gram mandi prices up by ₹150-200/quintal over past 4 days."
                },
                "time": "Yesterday",
                "district": "Latur / Akola",
                "urgency": "Info"
            },
            {
                "id": 4,
                "type": "blue",
                "icon": "📋",
                "title": {"mr": "सरकारी योजना अंतिम तारीख (Scheme Deadline)", "hi": "सरकारी योजना पंजीकरण", "en": "Govt Subsidy / Scheme Deadline"},
                "desc": {
                    "mr": "महाडीबीटी (MahaDBT) ठिबक सिंचन व पाईपलाईन अनुदानासाठी अर्ज करण्याची शेवटची मुदत २५ ऑक्टोबर आहे. आजच कागदपत्रे जोडा.",
                    "hi": "ड्रिप सिंचाई सब्सिडी पोर्टल पर आवेदन की अंतिम तिथि 25 अक्टूबर है।",
                    "en": "MahaDBT Drip & Pipeline subsidy registration window open until 25th October. Apply on portal."
                },
                "time": "2 days ago",
                "district": "Statewide",
                "urgency": "Notice"
            }
        ]
    }

def init_community_db():
    if not os.path.exists(COMMUNITY_DATA_FILE):
        data = get_initial_community_data()
        with open(COMMUNITY_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def load_community_data():
    init_community_db()
    try:
        with open(COMMUNITY_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        data = get_initial_community_data()
        save_community_data(data)
        return data

def save_community_data(data):
    with open(COMMUNITY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _filter_community_posts(posts, topic, query, nearby_only, district, state):
    topic_keywords = {
        "Pest & Disease": ("pest", "disease", "कीड", "रोग", "करपा"),
        "Grape": ("grape", "horticulture", "द्राक्ष", "फळबाग"),
        "Tomato": ("tomato", "vegetable", "टोमॅटो", "भाजी"),
        "Organic": ("organic", "सेंद्रिय", "जैविक"),
        "Mandi Market": ("mandi", "market", "price", "बाजार", "मंडी", "भाव"),
        "Machinery": ("machinery", "tractor", "rental", "अवजारे", "ट्रॅक्टर")
    }
    filtered_posts = posts
    if topic != "All topics":
        keywords = topic_keywords[topic]
        filtered_posts = [
            post for post in filtered_posts
            if any(
                keyword in (
                    str(post.get("category", "")) + " "
                    + " ".join(str(text) for text in post.get("text", {}).values())
                ).casefold()
                for keyword in keywords
            )
        ]

    if nearby_only:
        local_terms = (district.casefold(), state.casefold())
        filtered_posts = [
            post for post in filtered_posts
            if any(term in str(post.get("village", "")).casefold() for term in local_terms)
        ]

    query = query.strip().casefold()
    if query:
        filtered_posts = [
            post for post in filtered_posts
            if query in " ".join([
                str(post.get("author", "")),
                str(post.get("village", "")),
                str(post.get("category", "")),
                " ".join(str(text) for text in post.get("text", {}).values())
            ]).casefold()
        ]

    return filtered_posts


def add_new_post(author, user_id, village, category, text_content, image_emoji="🌱", is_expert=False, voice_note=False):
    data = load_community_data()
    post_id = int(datetime.now().timestamp() * 1000)
    initial = author.strip()[0] if author.strip() else "श"
    
    new_post = {
        "id": post_id,
        "author": author,
        "user_id": str(user_id),
        "village": village,
        "category": category,
        "time": "Just now / आत्ताच",
        "is_expert": is_expert,
        "avatar_initial": initial,
        "avatar_color": "linear-gradient(135deg, #2e7d32, #1b5e20)",
        "text": {
            "mr": text_content,
            "hi": text_content,
            "en": text_content
        },
        "image_emoji": image_emoji,
        "image_bg": "linear-gradient(135deg, #e8f5e9, #c8e6c9)",
        "voice_note": voice_note,
        "voice_duration": "0:20" if voice_note else "",
        "likes": 0,
        "liked_by": [],
        "replies": []
    }
    
    data["posts"].insert(0, new_post)
    save_community_data(data)
    return True

def toggle_like(post_id, user_key):
    data = load_community_data()
    for p in data["posts"]:
        if p["id"] == post_id:
            if "liked_by" not in p:
                p["liked_by"] = []
            if user_key in p["liked_by"]:
                p["liked_by"].remove(user_key)
                p["likes"] = max(0, p.get("likes", 1) - 1)
            else:
                p["liked_by"].append(user_key)
                p["likes"] = p.get("likes", 0) + 1
            save_community_data(data)
            return True
    return False

def add_reply_to_post(post_id, author_name, role_name, reply_text, user_id=None):
    data = load_community_data()
    for p in data["posts"]:
        if p["id"] == post_id:
            if "replies" not in p:
                p["replies"] = []
            reply_obj = {
                "id": int(datetime.now().timestamp() * 1000),
                "author": author_name,
                "user_id": str(user_id) if user_id is not None else "",
                "role": role_name,
                "time": "Just now",
                "text": reply_text
            }
            p["replies"].append(reply_obj)
            save_community_data(data)
            return True
    return False

def toggle_group(group_id, user_key):
    data = load_community_data()
    for g in data["groups"]:
        if g["id"] == group_id:
            if "joined_by" not in g:
                g["joined_by"] = []
            if user_key in g["joined_by"]:
                g["joined_by"].remove(user_key)
                g["members"] = max(0, g.get("members", 1) - 1)
            else:
                g["joined_by"].append(user_key)
                g["members"] = g.get("members", 0) + 1
            save_community_data(data)
            return True
    return False

def add_community_alert(alert_type, icon, title, desc, district, urgency):
    data = load_community_data()
    alert_obj = {
        "id": int(datetime.now().timestamp()),
        "type": alert_type,
        "icon": icon,
        "title": {"mr": title, "hi": title, "en": title},
        "desc": {"mr": desc, "hi": desc, "en": desc},
        "time": "Just now",
        "district": district,
        "urgency": urgency
    }
    data["alerts"].insert(0, alert_obj)
    save_community_data(data)
    return True

# -------------------------------------------------------------
# Speech Synthesizer Component helper (plays audio in browser)
# -------------------------------------------------------------
def render_audio_player_html(text_to_speak, lang_code):
    safe_text = json.dumps(text_to_speak)
    btn_label = "मोठ्याने ऐका (Read Aloud)" if lang_code == "mr" else "जोर से सुनें (Listen)" if lang_code == "hi" else "Read Aloud"
    target_lang = "mr-IN" if lang_code == "mr" else "hi-IN" if lang_code == "hi" else "en-IN"
    
    html_code = f"""
    <div style="margin: 4px 0;">
        <button onclick='
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance({safe_text});
            u.lang = "{target_lang}";
            u.rate = 0.92;
            window.speechSynthesis.speak(u);
        ' style="background: #2e7d32; color: white; border: none; border-radius: 20px; padding: 6px 14px; font-size: 13px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">
            🔊 <span>{btn_label}</span>
        </button>
        <button onclick='window.speechSynthesis.cancel();' style="background: #eceff1; color: #455a64; border: none; border-radius: 20px; padding: 6px 12px; font-size: 12px; cursor: pointer; margin-left: 6px;">
            ⏹ <span>थांबा (Stop)</span>
        </button>
    </div>
    """
    components.html(html_code, height=44)

# -------------------------------------------------------------
# Main UI Renderer for Community Tab
# -------------------------------------------------------------
def render_community_tab(lang_code, current_user, selected_district, selected_state):
    data = load_community_data()
    copy = COMMUNITY_COPY.get(lang_code, COMMUNITY_COPY["en"])
    user_key = str(current_user.get("id", current_user.get("username", "guest_user")))
    user_name = current_user.get("full_name", "शेतकरी मित्र")
    user_role = current_user.get("persona", "Farmer / Producer")
    is_expert_user = ("Agronomist" in user_role or "Researcher" in user_role or "Doctor" in user_name)

    total_posts = len(data["posts"])
    total_groups = len(data["groups"])
    user_joined_groups = [g for g in data["groups"] if user_key in g.get("joined_by", [])]
    user_posts_count = sum(1 for p in data["posts"] if p.get("user_id") == user_key)
    user_replies_count = sum(
        1 for post in data["posts"]
        for reply in post.get("replies", [])
        if reply.get("user_id") == user_key
    )
    user_likes_received = sum(
        post.get("likes", 0) for post in data["posts"]
        if post.get("user_id") == user_key
    )
    safe_user_name = html.escape(str(user_name))
    safe_user_role = html.escape(str(user_role))
    safe_district = html.escape(str(selected_district))
    safe_state = html.escape(str(selected_state))

    title_text = {
        "mr": "🌾 शेतकरी समुदाय मंच (Farmer Community)",
        "hi": "🌾 किसान समुदाय मंच (Farmer Community)",
        "en": "🌾 Farmer Community & Knowledge Sharing Network"
    }.get(lang_code, "🌾 Farmer Community & Knowledge Sharing Network")

    subtitle_text = {
        "mr": "शेतकरी बांधव, कृषी तज्ज्ञ व FPO सोबत प्रश्न विचारा, अनुभव शेअर करा आणि तातडीच्या सूचना मिळवा.",
        "hi": "किसान भाईयों, कृषि विशेषज्ञों और FPO के साथ जुड़े, समस्या साझा करें और तुरंत सलाह पाएं।",
        "en": "Connect with fellow farmers, verified agronomists, and FPOs. Ask questions, listen to audio notes, and receive pest alerts."
    }.get(lang_code, "Connect with farmers and share practical advice.")

    render_html(f"""
    <div style="background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%); 
                border: 1px solid #c8e6c9; 
                border-radius: 18px; 
                padding: 24px 26px; 
                margin-bottom: 22px; 
                box-shadow: 0 4px 15px rgba(46,125,50,0.12);
                position: relative;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <h2 style="color: #1b5e20; margin: 0; font-size: 1.85rem; font-weight: 700;">{html.escape(title_text)}</h2>
                <p style="color: #2e7d32; margin: 6px 0 0 0; font-size: 1rem;">{html.escape(subtitle_text)}</p>
                <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
                    <span style="background: #e8f5e9; color: #2e7d32; padding: 4px 10px; border-radius: 12px; font-size: 0.82rem; font-weight: 600;">📍 {safe_district}, {safe_state}</span>
                    <span style="background: #e8f5e9; color: #1b5e20; padding: 4px 10px; border-radius: 12px; font-size: 0.82rem; font-weight: 600;">👤 {safe_user_name}</span>
                </div>
            </div>
            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                <div style="background: #e8f5e9; padding: 8px 14px; border-radius: 10px; font-size: 0.78rem; color: #2e7d32;">
                    {total_posts} {"पोस्ट" if lang_code == "mr" else "पोस्ट" if lang_code == "hi" else "Posts"}
                </div>
                <div style="background: #e8f5e9; padding: 8px 14px; border-radius: 10px; font-size: 0.78rem; color: #2e7d32;">
                    {total_groups} {"गट" if lang_code == "mr" else "Groups" if lang_code == "hi" else "Groups"}
                </div>
                <div style="background: #e8f5e9; padding: 8px 14px; border-radius: 10px; font-size: 0.78rem; color: #2e7d32;">
                    {len(data['alerts'])} {"अलर्ट" if lang_code == "mr" else "Alerts" if lang_code == "hi" else "Alerts"}
                </div>
            </div>
        </div>
    </div>
    """)

    # 4 Sub-Tabs for Community: Feed, Groups, Alerts, Farmer Profile & Karma
    comm_tab1, comm_tab2, comm_tab3, comm_tab4 = st.tabs([
        "📢 समुदाय मंच (Community Feed)" if lang_code == "mr" else "📢 किसान मंच (Feed)" if lang_code == "hi" else "📢 Community Feed",
        "👥 शेतकरी गट (Farmer Groups)" if lang_code == "mr" else "👥 किसान समूह (Groups)" if lang_code == "hi" else "👥 Farmer Groups",
        "🔔 तातडीच्या सूचना (Alerts)" if lang_code == "mr" else "🔔 अलर्ट व सूचना (Alerts)" if lang_code == "hi" else "🔔 Urgent Alerts",
        "🏅 शेतकरी प्रोफाइल व बॅज (My Profile)" if lang_code == "mr" else "🏅 प्रोफ़ाइल व बैज (Profile)" if lang_code == "hi" else "🏅 Farmer Profile & Badges"
    ])

    # =========================================================
    # TAB 1: COMMUNITY FEED
    # =========================================================
    with comm_tab1:
        feed_col, post_col = st.columns([1.7, 1.1], gap="large")

        with post_col:
            render_html(f"""
                <div style="background: #ffffff; padding: 18px; border-radius: 14px; border: 1px solid #c8e6c9; box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-bottom: 20px;">
                <h4 style="color: #1b5e20; margin-top: 0; display: flex; align-items: center; gap: 8px;">
                    ✍️ {copy['ask_share']}
                </h4>
                <p style="font-size: 0.85rem; color: #555; margin-bottom: 12px;">
                    {copy['post_hint']}
                </p>
            </div>
            """)

            with st.form("new_community_post_form", clear_on_submit=True):
                p_category = st.selectbox(
                    "विषय / Category",
                    [
                        "Pest & Disease (कीड व रोग निदान)",
                        "Grape / Horticulture (फळबाग व द्राक्ष)",
                        "Tomato & Vegetables (भाजीपाला पिके)",
                        "Mandi Market Buzz (बाजारभाव व विक्री)",
                        "Organic Farming (सेंद्रिय शेती व खते)",
                        "Farm Machinery & Rentals (अवजारे व ट्रॅक्टर)",
                        "General Farming Discussion (सर्वसाधारण चर्चा)"
                    ]
                )

                p_text = st.text_area(
                    copy["post_text"],
                    placeholder=copy["post_placeholder"],
                    height=110
                )

                p_emoji = st.selectbox(
                    copy["crop_symbol"],
                    ["🍇 द्राक्ष (Grapes)", "🍅 टोमॅटो (Tomato)", "🌾 गहू / भात (Cereal)", "🌱 सेंद्रिय शेती (Organic)", "🚜 ट्रॅक्टर (Machinery)", "💰 बाजारभाव (Mandi)", "🐛 कीड / रोग (Pest)"]
                )

                st.caption(f"🔊 {copy['read_aloud_hint']}")

                p_submit = st.form_submit_button(
                    f"🚀 {copy['post_button']}",
                    type="primary",
                    use_container_width=True
                )

                if p_submit:
                    if p_text.strip():
                        emoji_map = {
                            "🍇 द्राक्ष (Grapes)": "🍇",
                            "🍅 टोमॅटो (Tomato)": "🍅",
                            "🌾 गहू / भात (Cereal)": "🌾",
                            "🌱 सेंद्रिय शेती (Organic)": "🌱",
                            "🚜 ट्रॅक्टर (Machinery)": "🚜",
                            "💰 बाजारभाव (Mandi)": "💰",
                            "🐛 कीड / रोग (Pest)": "🐛"
                        }
                        chosen_emoji = emoji_map.get(p_emoji, "🌱")
                        add_new_post(
                            author=user_name,
                            user_id=user_key,
                            village=f"{selected_district}, {selected_state}",
                            category=p_category.split("(")[0].strip(),
                            text_content=p_text.strip(),
                            image_emoji=chosen_emoji,
                            is_expert=is_expert_user
                        )
                        st.success(copy["published"])
                        st.rerun()
                    else:
                        st.warning(copy["empty_post"])

        with feed_col:
            st.markdown(f"### 🌾 {copy['feed_title']}")
            filter_col, search_col = st.columns([1, 1.5], gap="small")
            topic_labels = {
                "All topics": {"en": "All topics", "hi": "सभी विषय", "mr": "सर्व विषय"},
                "Pest & Disease": {"en": "Pests & disease", "hi": "कीट और रोग", "mr": "कीड व रोग"},
                "Grape": {"en": "Grapes & fruit", "hi": "अंगूर और फल", "mr": "द्राक्ष व फळे"},
                "Tomato": {"en": "Tomato & vegetables", "hi": "टमाटर और सब्ज़ियाँ", "mr": "टोमॅटो व भाजीपाला"},
                "Organic": {"en": "Organic farming", "hi": "जैविक खेती", "mr": "सेंद्रिय शेती"},
                "Mandi Market": {"en": "Market prices", "hi": "मंडी भाव", "mr": "बाजारभाव"},
                "Machinery": {"en": "Farm machinery", "hi": "कृषि उपकरण", "mr": "शेतीची अवजारे"}
            }
            with filter_col:
                selected_filter = st.selectbox(
                    copy["topic"],
                    list(topic_labels),
                    format_func=lambda topic: topic_labels[topic].get(lang_code, topic_labels[topic]["en"])
                )
            with search_col:
                search_query = st.text_input(
                    copy["search"],
                    placeholder=copy["search_placeholder"],
                    label_visibility="collapsed"
                )
            nearby_only = st.checkbox(copy["nearby"])

            filtered_posts = _filter_community_posts(
                data["posts"],
                selected_filter,
                search_query,
                nearby_only,
                selected_district,
                selected_state
            )

            if not filtered_posts:
                st.info(copy["no_results"])

            for post in filtered_posts:
                pid = post["id"]
                post_texts = post.get("text", {})
                if isinstance(post_texts, dict):
                    p_text_display = post_texts.get(
                        lang_code,
                        post_texts.get("mr", next(iter(post_texts.values()), ""))
                    )
                else:
                    p_text_display = str(post_texts)
                safe_post_text = html.escape(str(p_text_display))
                safe_post_author = html.escape(str(post.get("author", "Farmer")))
                safe_post_location = html.escape(str(post.get("village", selected_district)))
                safe_post_time = html.escape(str(post.get("time", "Recently")))
                safe_post_category = html.escape(str(post.get("category", "Farming")))
                safe_avatar_initial = html.escape(str(post.get("avatar_initial", "श")))
                is_liked = user_key in post.get("liked_by", [])
                likes_count = post.get("likes", 0)
                replies_list = post.get("replies", [])
                has_voice = post.get("voice_note", False)

                expert_badge = """<span style="background: #e3f2fd; color: #1565c0; font-size: 10.5px; padding: 2px 8px; border-radius: 12px; font-weight: 700; margin-left: 6px; border: 1px solid #bbdefb;">✔ प्रमाणित कृषी तज्ज्ञ (Verified Expert)</span>""" if post.get("is_expert") else ""

                card_html = f"""
                <div style="background: #ffffff; border-radius: 16px; padding: 18px 20px; margin-bottom: 12px; border: 1px solid #e0e8e1; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; gap: 12px; align-items: flex-start;">
                        <div style="width: 44px; height: 44px; border-radius: 50%; background: {post.get('avatar_color', '#2e7d32')}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; flex-shrink: 0; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
                            {safe_avatar_initial}
                        </div>
                        <div style="flex: 1;">
                            <div style="font-weight: 700; font-size: 15px; color: #1b2e1f; display: flex; align-items: center; flex-wrap: wrap;">
                                {safe_post_author} {expert_badge}
                            </div>
                            <div style="font-size: 12px; color: #7a8a7d; margin-top: 3px;">
                                📍 {safe_post_location} · 🕒 {safe_post_time} · <span style="background: #f1f8e9; color: #2e7d32; padding: 1px 7px; border-radius: 8px; font-weight: 600;">{safe_post_category}</span>
                            </div>
                        </div>
                    </div>
                    <div style="font-size: 14.5px; line-height: 1.6; color: #22331f; white-space: pre-wrap; margin: 14px 0 10px 0; background: #fafdfa; padding: 12px 14px; border-radius: 10px; border-left: 3px solid #66bb6a;">
                        {safe_post_text}
                    </div>
                </div>
                """
                render_html(card_html)

# Visual emoji banner or voice badge
                # Color category badge
                cat_badge_color = "#e8f5e9"  # default green-farm
                cat_emoji = post.get("image_emoji", "🌱")
                if "कीड" in post.get("category", "").lower() or "पest" in post.get("category", "").lower():
                    cat_badge_color = "#fff3e0"
                elif "बाजारभाव" in post.get("category", "").lower() or "मंडी" in post.get("category", "").lower():
                    cat_badge_color = "#fff8e1"
                elif "सेंद्रिय" in post.get("category", "").lower() or "organic" in post.get("category", "").lower():
                    cat_badge_color = "#e8f5e9"
                elif "ट्रॅक्टर" in post.get("category", "").lower() or "मशीन" in post.get("category", "").lower():
                    cat_badge_color = "#ffebee"

                if has_voice:
                    render_html(f"""
                    <div style="background: #e8f5e9; border: 1px solid #c8e6c9; border-radius: 14px; padding: 12px 16px; display: flex; align-items: center; gap: 14px; margin-top: -8px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
                        <span style="font-size: 22px; flex-shrink: 0;">🎙️</span>
                        <div style="flex: 1; min-width: 0;">
                            <b style="color: #1b5e20; font-size: 14px; font-weight: 600;">व्हॉइस नोट</b>
                            <div style="display: flex; gap: 3px; align-items: center; height: 18px; margin-top: 4px; margin-bottom: 4px;">
                                <span style="height: 12px; width: 3px; background: #43a047; border-radius: 2px;"></span>
                                <span style="height: 16px; width: 3px; background: #43a047; border-radius: 2px;"></span>
                                <span style="height: 10px; width: 3px; background: #43a047; border-radius: 2px;"></span>
                            </div>
                            <small style="color: #666; font-size: 11px;">{html.escape(str(post.get('voice_duration', '0:25')))}</small>
                        </div>
                    </div>
                    """)
                elif post.get("image_emoji"):
                    render_html(f"""
                    <div style="background: {cat_badge_color}; border: 2px solid #c8e6c9; border-radius: 14px; height: 90px; display: flex; align-items: center; justify-content: center; font-size: 48px; margin: -8px auto 12px auto; box-shadow: 0 2px 6px rgba(0,0,0,0.08);">
                        {html.escape(str(post.get('image_emoji', '🌱')))}
                    </div>
                    """)

                # Actions row: Like, Read Aloud, Reply
                # Use 3-column layout with proper spacing for mobile/touch
                act_col1, act_col2, act_col3 = st.columns([1, 1, 2.5], gap="medium")

                with act_col1:
                    like_label = f"❤️ {likes_count}" if is_liked else f"🤍 {likes_count}"
                    if st.button(like_label, key=f"like_{pid}", help="लाइक करा / Unlike"):
                        toggle_like(pid, user_key)
                        st.rerun()

                with act_col2:
                    render_audio_player_html(p_text_display, lang_code)

                with act_col3:
                    st.caption(f"💬 {len(replies_list)} {'उत्तरे' if lang_code == 'mr' else 'जवाब' if lang_code == 'hi' else 'Replies'}")

                # Replies Section
                if replies_list:
                    # Enhanced replies container with subtle highlight
                    render_html("""<div style="margin-left: 22px; border-left: 3px solid #e0e0e0; padding-left: 16px; margin-top: 8px; background: #fafdfa; border-radius: 8px; padding-bottom: 12px;"></div>""")
                    for r in replies_list:
                        role_str = html.escape(str(r.get('role', '')))
                        reply_author = html.escape(str(r.get('author', 'Farmer')))
                        reply_time = html.escape(str(r.get('time', 'recent')))
                        reply_text = html.escape(str(r.get('text', '')))
                        role_tag = f" <span style='font-size: 10px; color: #1565c0; background: #e3f2fd; padding: 1px 6px; border-radius: 6px; margin-left: 4px;'>{role_str}</span>" if role_str else ""
                        render_html(f"""
                        <div style="margin-left: 22px; background: #f8faf8; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13.5px; border: 1px solid #edf2ed; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                            <b style="color: #1b5e20; font-size: 14px;">{reply_author}</b>{role_tag} <span style="font-size: 11px; color: #888;">· {reply_time}</span><br>
                            <span style="color: #333; font-size: 13px; white-space: pre-wrap;">{reply_text}</span>
                        </div>
                        """)

                # Reply Input Box - enlarged for touch
                with st.expander(f"✍️ {copy['reply']} ({safe_post_author.split()[0]})"):
                    with st.form(f"reply_form_{pid}", clear_on_submit=True):
                        # Larger text area for touch comfort
                        reply_txt = st.text_input(
                            copy["reply"],
                            key=f"reply_input_{pid}",
                            label_visibility="collapsed"
                        )
                        submit_r = st.form_submit_button(
                            copy["reply_button"],
                            type="primary",
                            use_container_width=True
                        )
                        if submit_r and reply_txt.strip():
                            add_reply_to_post(pid, user_name, user_role, reply_txt.strip(), user_key)
                            st.success(copy["reply_added"])
                            st.rerun()
                        elif submit_r:
                            st.warning(copy["reply_empty"])

                st.markdown("<hr style='margin: 18px 0; border: 0; border-top: 1px dashed #e0e0e0;'>", unsafe_allow_html=True)

    # =========================================================
    # TAB 2: FARMER GROUPS (शेतकरी गट)
    # =========================================================
    with comm_tab2:
        render_html("""
        <div style="background: #ffffff; padding: 16px 20px; border-radius: 12px; border: 1px solid #c8e6c9; margin-bottom: 18px;">
            <h4 style="color: #1b5e20; margin-top: 0;">👥 पीक आणि प्रादेशिक शेतकरी गट (Specialized Farmer Communities)</h4>
            <p style="font-size: 0.9rem; color: #444; margin-bottom: 0;">
                तुमच्या आवडीच्या गटात सामील व्हा, एकत्र अवजारे भाड्याने घ्या, किंवा तज्ज्ञांच्या सल्ल्याने पीक उत्पादन वाढवा.
            </p>
        </div>
        """)

        g_cols = st.columns(2)
        for idx, grp in enumerate(data["groups"]):
            gid = grp["id"]
            g_name = grp["name"].get(lang_code, grp["name"]["mr"])
            g_desc = grp["desc"].get(lang_code, grp["desc"]["mr"])
            is_joined = user_key in grp.get("joined_by", [])
            members_cnt = grp.get("members", 100)

            with g_cols[idx % 2]:
                render_html(f"""
                <div style="background: #ffffff; border-radius: 14px; padding: 16px; margin-bottom: 14px; border: 1px solid #dcedc8; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; gap: 14px; align-items: center;">
                    <div style="width: 50px; height: 50px; border-radius: 14px; background: {grp.get('bg', '#e8f5e9')}; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0;">
                        {grp.get('icon', '🌾')}
                    </div>
                    <div style="flex: 1; min-width: 0;">
                        <div style="font-weight: 700; font-size: 15px; color: #1b2e1f;">{g_name}</div>
                        <div style="font-size: 12px; color: #666; margin-top: 2px;">{g_desc}</div>
                        <div style="font-size: 11.5px; color: #2e7d32; font-weight: 600; margin-top: 4px;">👥 {members_cnt} सदस्य (Members) · {grp.get('category', 'Farming')}</div>
                    </div>
                </div>
                """)

                btn_label = "सामील ✓ (Joined)" if is_joined else "सामील व्हा (Join Group)"
                btn_type = "secondary" if is_joined else "primary"
                if st.button(btn_label, key=f"grp_btn_{gid}", type=btn_type, use_container_width=True):
                    toggle_group(gid, user_key)
                    st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================
    # TAB 3: URGENT ALERTS (तातडीच्या सूचना)
    # =========================================================
    with comm_tab3:
        render_html("""
        <div style="background: #ffffff; padding: 16px 20px; border-radius: 12px; border: 1px solid #c8e6c9; margin-bottom: 18px;">
            <h4 style="color: #1b5e20; margin-top: 0;">🔔 हायपरलोकल कृषी आणि कीड-रोग सूचना (Hyperlocal Alerts)</h4>
            <p style="font-size: 0.9rem; color: #444; margin-bottom: 0;">
                तुमच्या परिसरातील हवामान, बाजारभाव तेजी, सरकारी योजनांची मुदत व किडींचा प्रादुर्भाव याविषयी तातडीचे अलर्ट्स.
            </p>
        </div>
        """)

        # Allow Agronomists or FPO admins to post urgent alert
        if is_expert_user or "FPO" in user_role:
            with st.expander("🚨 नवीन कृषी अलर्ट जारी करा (Post Verified Agronomic Alert)"):
                with st.form("new_alert_form", clear_on_submit=True):
                    al_title = st.text_input("अलर्ट शीर्षक (Alert Title):", placeholder="उदा. करपा रोगाचा प्रादुर्भाव / अतिवृष्टी इशारा")
                    al_desc = st.text_area("तपशील आणि तातडीने करावयाची उपाययोजना (Details & Advisory):")
                    al_type = st.selectbox("गंभीरता (Severity)", ["red (अति तातडीचे / High Risk)", "amber (सावधानता / Moderate)", "blue (सरकारी योजना / Notice)", "green (बाजारभाव तेजी / Price Surge)"])
                    al_submit = st.form_submit_button("अलर्ट प्रसिद्ध करा (Broadcast Alert)", type="primary")

                    if al_submit and al_title.strip():
                        color_code = al_type.split()[0]
                        icon_choice = "🐛" if color_code == "red" else "🌧️" if color_code == "amber" else "💰" if color_code == "green" else "📋"
                        add_community_alert(color_code, icon_choice, al_title.strip(), al_desc.strip(), selected_district, "High")
                        st.success("अलर्ट सर्व शेतकऱ्यांपर्यंत पोहोचवला गेला आहे!")
                        st.rerun()

        for a in data["alerts"]:
            alert_title_text = str(a["title"].get(lang_code, a["title"]["mr"]))
            alert_desc_text = str(a["desc"].get(lang_code, a["desc"]["mr"]))
            a_title = html.escape(alert_title_text)
            a_desc = html.escape(alert_desc_text)
            alert_district = html.escape(str(a.get("district", selected_district)))
            alert_time = html.escape(str(a.get("time", "recent")))
            # Color coding based on urgency type with farmer-friendly labels
            if a["type"] == "red":
                border_col = "#c62828"
                bg_col = "#ffebee"
                urgency_label = "🔴 HIGH"
                urgency_text_color = "white"
            elif a["type"] == "amber":
                border_col = "#f9a825"
                bg_col = "#fff8e1"
                urgency_label = "🟡 MEDIUM"
                urgency_text_color = "#1b5e20"
            elif a["type"] == "blue":
                border_col = "#1565c0"
                bg_col = "#e3f2fd"
                urgency_label = "🟦 INFO"
                urgency_text_color = "white"
            else:  # green
                border_col = "#2e7d32"
                bg_col = "#e8f5e9"
                urgency_label = "🟢 SAFE"
                urgency_text_color = "white"

            render_html(f"""
            <div style="background: {bg_col}; border-left: 6px solid {border_col}; 
                        border-radius: 14px; padding: 18px 20px; margin-bottom: 16px; 
                        box-shadow: 0 2px 6px rgba(0,0,0,0.04); 
                        position: relative;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                    <div style="font-size: 28px; flex-shrink: 0; line-height: 1; color: {urgency_text_color};">
                        {a.get('icon', '🔔')} {urgency_label}
                    </div>
                    <div style="margin-top: 2px; font-size: 11.5px; color: #666; background: rgba(0,0,0,0.06); padding: 2px 8px; border-radius: 6px;">
                        🕒 {alert_time}
                    </div>
                </div>
                <h4 style="margin: 6px 0 10px 0; font-size: 15px; color: #1b2e1f; font-weight: 700;">{a_title}</h4>
                <p style="margin: 8px 0 0 0; font-size: 13.5px; line-height: 1.5; color: #2d3f30;">{a_desc}</p>
                <div style="margin-top: 8px; font-size: 11px; color: #555;">
                    📍 कार्यक्षेत्र: <b>{alert_district}</b>
                </div>
            </div>
            """)

            # Audio button for alert
            render_audio_player_html(f"{alert_title_text}. {alert_desc_text}", lang_code)
            st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================
    # TAB 4: FARMER PROFILE & GAMIFICATION BADGES
    # =========================================================
    with comm_tab4:
        prof_col1, prof_col2 = st.columns([1.2, 1.8], gap="large")

        with prof_col1:
            render_html(f"""
            <div style="background: linear-gradient(135deg, #2e7d32, #1b5e20); border-radius: 18px; padding: 24px; color: white; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="width: 76px; height: 76px; border-radius: 50%; background: rgba(255,255,255,0.2); border: 3px solid rgba(255,255,255,0.6); margin: 0 auto 12px; display: flex; align-items: center; justify-content: center; font-size: 36px;">
                    👨‍🌾
                </div>
                <h3 style="color: white; margin: 0; font-size: 18px;">{safe_user_name}</h3>
                <p style="font-size: 13px; opacity: 0.9; margin: 4px 0 14px 0;">📍 {safe_district}, {safe_state} · {safe_user_role}</p>
                
                <div style="display: flex; gap: 8px;">
                    <div style="flex: 1; background: rgba(255,255,255,0.18); border-radius: 10px; padding: 10px 4px;">
                        <b style="font-size: 19px; display: block;">{user_posts_count}</b>
                        <span style="font-size: 11px; opacity: 0.9;">📝 Posts</span>
                    </div>
                    <div style="flex: 1; background: rgba(255,255,255,0.18); border-radius: 10px; padding: 10px 4px;">
                        <b style="font-size: 19px; display: block;">{user_replies_count}</b>
                        <span style="font-size: 11px; opacity: 0.9;">💬 Replies</span>
                    </div>
                    <div style="flex: 1; background: rgba(255,255,255,0.18); border-radius: 10px; padding: 10px 4px;">
                        <b style="font-size: 19px; display: block;">{user_likes_received}</b>
                        <span style="font-size: 11px; opacity: 0.9;">❤️ Thanks</span>
                    </div>
                </div>
            </div>
            """)

            st.markdown("<br>", unsafe_allow_html=True)

            badges = []
            if user_posts_count:
                badges.append("🌱 First post")
            if user_replies_count:
                badges.append("💬 Helpful contributor")
            if user_joined_groups:
                badges.append("👥 Group member")
            badge_html = "".join(
                f'<span style="background:#e8f5e9;color:#2e7d32;font-size:12px;font-weight:700;'
                f'padding:6px 12px;border-radius:20px;border:1px solid #c8e6c9;">{badge}</span>'
                for badge in badges
            )
            render_html(f"""
            <div style="background:#fff;border-radius:16px;padding:18px;border:1px solid #dcedc8;
                        box-shadow:0 2px 8px rgba(0,0,0,.04);">
                <h4 style="color:#1b5e20;margin-top:0;font-size:14px;">🏅 Community milestones</h4>
                <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;">
                    {badge_html or '<span style="color:#667568;font-size:13px;">Share a post or join a group to earn your first milestone.</span>'}
                </div>
            </div>
            """)

        with prof_col2:
            render_html("""
            <div style="background: #ffffff; border-radius: 16px; padding: 20px; border: 1px solid #dcedc8; box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-bottom: 18px;">
                <h4 style="color: #1b5e20; margin-top: 0; font-size: 15px;">
                    👥 माझे सक्रिय शेतकरी गट (My Joined Groups)
                </h4>
            </div>
            """)

            if user_joined_groups:
                for jg in user_joined_groups:
                    jg_name = jg["name"].get(lang_code, jg["name"]["mr"])
                    render_html(f"""
                    <div style="display: flex; align-items: center; gap: 10px; padding: 8px 12px; margin-bottom: 6px; background: #ffffff; border-radius: 8px; border: 1px solid #f0f4f0; font-size: 13.5px;">
                        <span style="font-size: 20px;">{jg.get('icon', '🌾')}</span>
                        <b>{jg_name}</b>
                        <span style="margin-left: auto; color: #2e7d32; font-weight: 600; font-size: 12px;">✓ सदस्य ({jg.get('members', 0)})</span>
                    </div>
                    """)
            else:
                st.info("तुम्ही अजून कोणत्याही गटात सामील झालेला नाही. 'शेतकरी गट' टॅबमधून सामील व्हा!")

            st.markdown("#### 📊 Your community activity")
            stat_one, stat_two, stat_three = st.columns(3)
            stat_one.metric("Posts", user_posts_count)
            stat_two.metric("Replies", user_replies_count)
            stat_three.metric("Likes received", user_likes_received)
