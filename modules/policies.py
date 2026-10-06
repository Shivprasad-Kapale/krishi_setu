"""Plain-language Indian and Maharashtra farmer policy guidance."""

from __future__ import annotations

from typing import Any

import streamlit as st

from modules.translator_service import translate_text


POLICY_TOPICS: dict[str, list[dict[str, Any]]] = {
    "Government payments": [
        {
            "name": "PM-KISAN",
            "summary": (
                "Eligible landholding farmer families can receive ₹6,000 a year "
                "from the central government, paid in three instalments. Check "
                "your beneficiary status, e-KYC, bank account and land record details."
            ),
            "steps": (
                "Use the official PM-KISAN portal to check status or complete e-KYC. "
                "If a payment is held, read the reason shown there and ask your "
                "local agriculture or revenue office how to correct it."
            ),
            "remember": (
                "Eligibility exclusions apply. A land record or registration alone "
                "does not guarantee payment."
            ),
            "source": "https://pmkisan.gov.in/",
            "source_name": "PM-KISAN official portal",
        },
        {
            "name": "Namo Shetkari Mahasanman Nidhi (Maharashtra)",
            "summary": (
                "This is Maharashtra's farmer payment scheme linked to PM-KISAN "
                "eligibility. Instalments and checks follow the current state rules."
            ),
            "steps": (
                "Check the Namo Shetkari portal for your current beneficiary and "
                "instalment status. Keep PM-KISAN, Aadhaar, bank and land records "
                "consistent."
            ),
            "remember": (
                "Do not count an instalment as received until it appears in your "
                "official status or bank account. State rules and payment dates can change."
            ),
            "source": "https://nsmny.mahait.org/",
            "source_name": "Maharashtra Namo Shetkari portal",
        },
    ],
    "Crop insurance": [
        {
            "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "summary": (
                "Crop insurance can help protect against notified crop losses. "
                "The crops, villages, risks, application window and farmer premium "
                "depend on the current season notification."
            ),
            "steps": (
                "Before applying, check that your crop and village are notified "
                "for this season. Apply by the announced deadline through an "
                "authorised channel. For damage, report it promptly using the "
                "official instructions and keep the acknowledgement."
            ),
            "remember": (
                "Cover is not automatic for every crop or event. Deadlines and "
                "claim evidence requirements matter."
            ),
            "source": "https://pmfby.gov.in/",
            "source_name": "PMFBY official portal",
        },
    ],
    "Subsidies and equipment": [
        {
            "name": "MahaDBT Farmer Schemes",
            "summary": (
                "Maharashtra farmers can check current application rounds for "
                "eligible farm equipment, irrigation and other agriculture support."
            ),
            "steps": (
                "Open MahaDBT Farmer, sign in, complete your farmer profile and "
                "check which components are accepting applications. Read the "
                "required documents and selection steps before applying."
            ),
            "remember": (
                "Subsidy amount, eligibility, selection and available funds vary "
                "by component and application round. Do not buy equipment assuming "
                "a subsidy will be approved; first check the current rules."
            ),
            "source": "https://mahadbt.maharashtra.gov.in/Farmer/",
            "source_name": "MahaDBT Farmer portal",
        },
        {
            "name": "Maharashtra Agriculture Department",
            "summary": (
                "Use the state Agriculture Department for current notices, "
                "scheme circulars and district-level agriculture information."
            ),
            "steps": (
                "Check the latest notice and its date. If a notice is unclear, "
                "ask your Taluka Agriculture Officer or district agriculture office."
            ),
            "remember": (
                "Old scheme posters may show expired dates or previous-year amounts."
            ),
            "source": "https://krishi.maharashtra.gov.in/",
            "source_name": "Maharashtra Agriculture Department",
        },
    ],
    "Selling crops and MSP": [
        {
            "name": "Minimum Support Price (MSP)",
            "summary": (
                "MSP is a support price announced for selected crops. The current "
                "season's price and where procurement is available must be checked "
                "for your crop and location."
            ),
            "steps": (
                "Check the latest season announcement and local procurement "
                "registration instructions. Compare the MSP with your mandi price, "
                "quality requirements, transport and waiting costs."
            ),
            "remember": (
                "An announced MSP does not mean every crop will be bought at every "
                "market. Confirm the crop, dates, quality rules and buying centre."
            ),
            "source": "https://agriwelfare.gov.in/",
            "source_name": "Agriculture Ministry notices",
        },
        {
            "name": "e-NAM (National Agriculture Market)",
            "summary": (
                "e-NAM connects participating mandis and helps farmers and traders "
                "see market information and conduct trade where the facility is active."
            ),
            "steps": (
                "Check whether your mandi and commodity are active. Ask the mandi "
                "office about registration, assaying, lot preparation, charges and "
                "payment before sending produce."
            ),
            "remember": (
                "Online access does not remove local mandi rules, quality checks "
                "or transport costs."
            ),
            "source": "https://www.enam.gov.in/web/",
            "source_name": "e-NAM official portal",
        },
    ],
    "Loans and working capital": [
        {
            "name": "Kisan Credit Card (KCC)",
            "summary": (
                "KCC is a bank credit facility for eligible farm and allied "
                "activities. It can help pay seasonal costs such as seed, fertiliser "
                "and labour."
            ),
            "steps": (
                "Ask your bank or cooperative about KCC eligibility, the credit "
                "limit based on your farm plan, documents, interest and repayment "
                "dates. Repay on time to avoid extra charges and check whether any "
                "interest benefit applies to your account."
            ),
            "remember": (
                "It is a loan, not a grant. Rates, limits and benefits depend on "
                "current rules and your bank."
            ),
            "source": "https://www.myscheme.gov.in/schemes/kcc",
            "source_name": "myScheme Kisan Credit Card information",
        },
    ],
    "Import and export": [
        {
            "name": "Check the rule for your exact product",
            "summary": (
                "India's import and export rules can differ by crop, processed "
                "product, quality and date. A commodity may be free, restricted "
                "or prohibited, and rules can change quickly."
            ),
            "steps": (
                "Find the product's 8-digit ITC(HS) code and check the current "
                "DGFT import/export policy and latest notifications. For export, "
                "also check destination-country food-safety, plant-health, grading, "
                "testing, packaging and phytosanitary requirements. APEDA supports "
                "exports of scheduled agricultural and processed food products."
            ),
            "remember": (
                "Never rely on an old news article or last season's permission. "
                "Confirm the rule and paperwork with DGFT, customs, APEDA where "
                "applicable, and a qualified customs broker before buying or shipping."
            ),
            "source": "https://www.dgft.gov.in/CP/?opt=itchs-import-export",
            "source_name": "DGFT ITC(HS) import/export policy",
            "extra_source": "https://apeda.gov.in/",
            "extra_source_name": "APEDA",
        },
    ],
}

POLICY_UI_MR = {
    "Government payments": "सरकारी आर्थिक मदत",
    "Crop insurance": "पीक विमा",
    "Subsidies and equipment": "अनुदान आणि शेतीची साधने",
    "Selling crops and MSP": "पीक विक्री आणि हमीभाव",
    "Loans and working capital": "कर्ज आणि हंगामी खर्च",
    "Import and export": "आयात आणि निर्यात",
    "Policies for farmers": "शेतकऱ्यांसाठी योजना आणि धोरणे",
    "Simple guides to Indian and Maharashtra schemes, crop selling, farm loans, and import/export rules.": (
        "भारत आणि महाराष्ट्रातील शेतकरी योजना, पीक विक्री, शेती कर्ज आणि "
        "आयात-निर्यात नियम सोप्या भाषेत समजून घ्या."
    ),
    "Rules, amounts, deadlines and eligibility can change. Use the official government link for the latest details. Never pay an agent who promises a guaranteed scheme benefit.": (
        "योजनेचे नियम, रक्कम, शेवटची तारीख आणि पात्रता बदलू शकते. नवीन "
        "माहितीसाठी सरकारी संकेतस्थळ तपासा. लाभ नक्की मिळवून देतो असे सांगणाऱ्या "
        "एजंटला पैसे देऊ नका."
    ),
    "Choose what you want to know about": "तुम्हाला कोणत्या विषयाची माहिती हवी आहे?",
    "In simple words": "सोप्या भाषेत",
    "What to do": "तुम्ही काय करावे",
    "Simple crop cost and profit calculator": "पीक खर्च आणि नफ्याचा सोपा अंदाज",
    "Enter your own expected yield, sale price and costs. This is a planning estimate, not a guaranteed price or profit.": (
        "तुमच्या अपेक्षित उत्पादनाचे, विक्रीभावाचे आणि खर्चाचे आकडे भरा. हा "
        "फक्त नियोजनासाठीचा अंदाज आहे; भाव किंवा नफा निश्चित नाही."
    ),
    "Expected yield (quintals per acre)": "अपेक्षित उत्पादन (प्रति एकर क्विंटल)",
    "Expected sale price (₹ per quintal)": "अपेक्षित विक्रीभाव (प्रति क्विंटल रुपये)",
    "Area (acres)": "क्षेत्र (एकर)",
    "Estimated costs per acre": "प्रति एकर अंदाजे खर्च",
    "Seed and planting (₹)": "बियाणे आणि पेरणी (रुपये)",
    "Fertiliser and soil care (₹)": "खते आणि मातीची निगा (रुपये)",
    "Sprays and crop care (₹)": "फवारणी आणि पीक संरक्षण (रुपये)",
    "Labour (₹)": "मजुरी (रुपये)",
    "Water and energy (₹)": "पाणी आणि वीज/इंधन (रुपये)",
    "Harvest and machinery (₹)": "कापणी आणि यंत्रसामग्री (रुपये)",
    "Transport and market charges (₹)": "वाहतूक आणि बाजार खर्च (रुपये)",
    "Other costs (₹)": "इतर खर्च (रुपये)",
    "Calculate estimate": "अंदाज काढा",
    "Estimated total sales": "एकूण अंदाजे विक्री",
    "Estimated total cost": "एकूण अंदाजे खर्च",
    "Estimated profit / (loss)": "अंदाजे नफा / (तोटा)",
    "Sales = yield × sale price. Profit = sales − entered costs. This simple estimate may not include family labour, land rent, loan interest, storage or price changes unless you enter them.": (
        "विक्री = उत्पादन × विक्रीभाव. नफा = विक्री − भरलेला खर्च. कुटुंबाची "
        "मजुरी, जमिनीचे भाडे, कर्जाचे व्याज, साठवण किंवा भावातील बदल तुम्ही "
        "खर्चात भरले नसल्यास या अंदाजात धरलेले नाहीत."
    ),
}

POLICY_CARD_MR = {
    "PM-KISAN": {
        "summary": (
            "पात्र जमीनधारक शेतकरी कुटुंबाला केंद्र सरकारकडून वर्षाला ₹६,००० "
            "मिळू शकतात. ही रक्कम तीन हप्त्यांत दिली जाते. लाभार्थी स्थिती, "
            "ई-केवायसी, बँक खाते आणि जमीन नोंदी तपासा."
        ),
        "steps": (
            "अधिकृत PM-KISAN संकेतस्थळावर लाभार्थी स्थिती तपासा किंवा ई-केवायसी "
            "पूर्ण करा. हप्ता थांबला असल्यास संकेतस्थळावर दिलेले कारण वाचा आणि "
            "दुरुस्तीसाठी स्थानिक कृषी किंवा महसूल कार्यालयात विचारा."
        ),
        "remember": (
            "काही शेतकरी कुटुंबे नियमांनुसार अपात्र असू शकतात. जमीन नोंद किंवा "
            "नोंदणी असल्याने पैसे मिळतीलच याची खात्री नसते."
        ),
        "source_name": "PM-KISAN अधिकृत संकेतस्थळ",
    },
    "Namo Shetkari Mahasanman Nidhi (Maharashtra)": {
        "name": "नमो शेतकरी महासन्मान निधी (महाराष्ट्र)",
        "summary": (
            "ही महाराष्ट्र शासनाची शेतकरी मदत योजना PM-KISAN पात्रतेशी जोडलेली "
            "आहे. हप्ते आणि तपासणी सध्याच्या राज्य नियमांनुसार होतात."
        ),
        "steps": (
            "नमो शेतकरी संकेतस्थळावर लाभार्थी आणि हप्त्याची स्थिती तपासा. "
            "PM-KISAN, आधार, बँक खाते आणि जमीन नोंदीतील माहिती जुळते आहे का पाहा."
        ),
        "remember": (
            "अधिकृत स्थिती किंवा बँक खात्यात रक्कम जमा दिसल्यावरच हप्ता मिळाला "
            "असे समजा. राज्याचे नियम आणि पैसे येण्याच्या तारखा बदलू शकतात."
        ),
        "source_name": "महाराष्ट्र नमो शेतकरी अधिकृत संकेतस्थळ",
    },
    "Pradhan Mantri Fasal Bima Yojana (PMFBY)": {
        "name": "प्रधानमंत्री पीक विमा योजना (PMFBY)",
        "summary": (
            "अधिसूचित पिकांचे काही प्रकारच्या नुकसानीपासून संरक्षण करण्यासाठी "
            "पीक विमा मदत करू शकतो. कोणते पीक, गाव, धोका, अर्जाची मुदत आणि "
            "शेतकऱ्याचा विमा हप्ता हे चालू हंगामाच्या सूचनेवर ठरते."
        ),
        "steps": (
            "या हंगामासाठी तुमचे पीक आणि गाव अधिसूचित आहे का ते आधी तपासा. "
            "दिलेल्या मुदतीत अधिकृत मार्गाने अर्ज करा. नुकसान झाल्यास अधिकृत "
            "सूचनेनुसार लगेच कळवा आणि पोचपावती जपून ठेवा."
        ),
        "remember": (
            "प्रत्येक पीक किंवा प्रत्येक नुकसानीला विमा लागू होतोच असे नाही. "
            "अर्जाची मुदत आणि नुकसान पुरावा महत्त्वाचा असतो."
        ),
        "source_name": "PMFBY अधिकृत संकेतस्थळ",
    },
    "MahaDBT Farmer Schemes": {
        "name": "महाडीबीटी शेतकरी योजना",
        "summary": (
            "महाराष्ट्रातील शेतकरी शेतीची साधने, सिंचन आणि इतर मदतीसाठी "
            "चालू अर्ज फेरीत पात्र योजना तपासू शकतात."
        ),
        "steps": (
            "महाडीबीटी शेतकरी पोर्टलवर लॉगिन करा, शेतकरी माहिती पूर्ण करा आणि "
            "सध्या अर्ज सुरू असलेले घटक तपासा. अर्जापूर्वी लागणारी कागदपत्रे "
            "आणि निवडीची पद्धत वाचा."
        ),
        "remember": (
            "अनुदानाची रक्कम, पात्रता, निवड आणि उपलब्ध निधी घटक व अर्ज फेरीनुसार "
            "बदलतो. मंजुरी मिळण्याआधी अनुदान मिळेल असे गृहीत धरून साधने खरेदी करू नका."
        ),
        "source_name": "महाडीबीटी शेतकरी पोर्टल",
    },
    "Maharashtra Agriculture Department": {
        "name": "महाराष्ट्र कृषी विभाग",
        "summary": (
            "महाराष्ट्र कृषी विभागाच्या संकेतस्थळावर नवीन सूचना, योजना परिपत्रके "
            "आणि जिल्हानिहाय शेतीविषयक माहिती तपासा."
        ),
        "steps": (
            "नवीनतम सूचना आणि तिची तारीख तपासा. काही समजत नसल्यास तालुका "
            "कृषी अधिकारी किंवा जिल्हा कृषी कार्यालयात विचारा."
        ),
        "remember": (
            "जुन्या योजनेच्या जाहिरातीत मागील वर्षाची रक्कम किंवा संपलेली तारीख असू शकते."
        ),
        "source_name": "महाराष्ट्र कृषी विभाग",
    },
    "Minimum Support Price (MSP)": {
        "name": "किमान आधारभूत किंमत (MSP)",
        "summary": (
            "काही निवडक पिकांसाठी सरकार आधारभूत किंमत जाहीर करते. सध्याच्या "
            "हंगामातील किंमत आणि खरेदी कुठे होते हे तुमच्या पिकासाठी आणि "
            "ठिकाणासाठी तपासा."
        ),
        "steps": (
            "चालू हंगामाची अधिकृत घोषणा आणि स्थानिक खरेदी नोंदणीची माहिती तपासा. "
            "बाजारभावाशी तुलना करताना मालाची गुणवत्ता, वाहतूक आणि प्रतीक्षा खर्च "
            "देखील मोजा."
        ),
        "remember": (
            "MSP जाहीर झाली म्हणजे प्रत्येक बाजारात प्रत्येक पीक खरेदी होईलच असे नाही. "
            "पीक, तारीख, गुणवत्तेचे नियम आणि खरेदी केंद्र आधी तपासा."
        ),
        "source_name": "कृषी मंत्रालयाच्या अधिकृत सूचना",
    },
    "e-NAM (National Agriculture Market)": {
        "name": "ई-नाम (राष्ट्रीय कृषी बाजार)",
        "summary": (
            "ई-नाम जोडलेल्या बाजार समित्यांमध्ये शेतकरी आणि व्यापाऱ्यांना "
            "बाजार माहिती पाहता येते आणि सुविधा सुरू असल्यास व्यापार करता येतो."
        ),
        "steps": (
            "तुमची बाजार समिती आणि पीक ई-नामवर सुरू आहे का तपासा. माल पाठवण्यापूर्वी "
            "नोंदणी, गुणवत्ता तपासणी, मालाची तयारी, शुल्क आणि पैसे मिळण्याची "
            "पद्धत बाजार समितीत विचारा."
        ),
        "remember": (
            "ऑनलाइन सुविधा असली तरी स्थानिक बाजार नियम, गुणवत्ता तपासणी आणि "
            "वाहतूक खर्च लागू होऊ शकतात."
        ),
        "source_name": "ई-नाम अधिकृत संकेतस्थळ",
    },
    "Kisan Credit Card (KCC)": {
        "name": "किसान क्रेडिट कार्ड (KCC)",
        "summary": (
            "KCC हे पात्र शेती आणि शेतीपूरक कामांसाठी बँकेकडून मिळणारे कर्ज "
            "आहे. बियाणे, खते आणि मजुरीसारखे हंगामी खर्च भागवण्यासाठी ते उपयोगी पडू शकते."
        ),
        "steps": (
            "तुमच्या बँक किंवा सहकारी संस्थेकडे पात्रता, शेतीच्या आराखड्यानुसार "
            "कर्जमर्यादा, कागदपत्रे, व्याज आणि परतफेडीच्या तारखा विचारा. वेळेवर "
            "परतफेड करा आणि व्याज सवलत लागू आहे का तपासा."
        ),
        "remember": (
            "हे कर्ज आहे, अनुदान नाही. व्याज, मर्यादा आणि सवलती सध्याचे नियम "
            "आणि बँकेनुसार ठरतात."
        ),
        "source_name": "myScheme किसान क्रेडिट कार्ड माहिती",
    },
    "Check the rule for your exact product": {
        "name": "तुमच्या मालासाठीचा नियम तपासा",
        "summary": (
            "भारतातील आयात-निर्यात नियम पीक, प्रक्रिया केलेला माल, गुणवत्ता आणि "
            "तारखेनुसार वेगळे असू शकतात. एखाद्या मालाची आयात-निर्यात खुली, "
            "मर्यादित किंवा बंद असू शकते; नियम लवकर बदलू शकतात."
        ),
        "steps": (
            "मालाचा ८ अंकी ITC(HS) कोड शोधून DGFT च्या सध्याच्या आयात-निर्यात "
            "धोरणात आणि नवीन सूचनांमध्ये तपासा. निर्यातीसाठी खरेदीदार देशाचे "
            "अन्नसुरक्षा, वनस्पती आरोग्य, गुणवत्ता, तपासणी, पॅकिंग आणि "
            "वनस्पती-स्वच्छता नियमही तपासा. APEDA काही कृषी आणि प्रक्रिया केलेल्या "
            "अन्नपदार्थांच्या निर्यातीस मदत करते."
        ),
        "remember": (
            "जुनी बातमी किंवा मागील हंगामाची परवानगी यावर विसंबू नका. माल खरेदी "
            "किंवा पाठवण्यापूर्वी DGFT, सीमाशुल्क विभाग आणि लागू असल्यास APEDA "
            "यांच्याकडून सध्याचे नियम व कागदपत्रे निश्चित करा."
        ),
        "source_name": "DGFT आयात-निर्यात धोरण (ITC(HS))",
        "extra_source_name": "APEDA",
    },
}


def calculate_farm_profit(
    yield_quintals_per_acre: float,
    sale_price_per_quintal: float,
    costs_per_acre: dict[str, float],
    acres: float,
) -> dict[str, float]:
    """Calculate simple gross revenue and net profit from farmer-entered values."""
    values = [yield_quintals_per_acre, sale_price_per_quintal, acres, *costs_per_acre.values()]
    if any(value < 0 for value in values):
        raise ValueError("Enter zero or a positive value in each field.")
    if acres <= 0:
        raise ValueError("Farm area must be greater than zero.")

    cost_per_acre = sum(costs_per_acre.values())
    gross_per_acre = yield_quintals_per_acre * sale_price_per_quintal
    profit_per_acre = gross_per_acre - cost_per_acre
    return {
        "cost_per_acre": cost_per_acre,
        "gross_per_acre": gross_per_acre,
        "profit_per_acre": profit_per_acre,
        "total_cost": cost_per_acre * acres,
        "total_gross": gross_per_acre * acres,
        "total_profit": profit_per_acre * acres,
    }


def _t(text: str, language: str) -> str:
    if language == "mr":
        return POLICY_UI_MR.get(text, text)
    return translate_text(text, language)


def _policy_text(policy: dict[str, Any], field: str, language: str) -> str:
    if language == "mr":
        translated = POLICY_CARD_MR.get(policy["name"], {}).get(field)
        if translated:
            return translated
    return _t(policy[field], language)


def _render_policy_card(policy: dict[str, Any], language: str) -> None:
    localized = POLICY_CARD_MR.get(policy["name"], {}) if language == "mr" else {}
    name = localized.get("name") or _t(policy["name"], language)
    with st.expander(name, expanded=False):
        st.markdown(
            f"**{_t('In simple words', language)}:** "
            f"{_policy_text(policy, 'summary', language)}"
        )
        st.markdown(
            f"**{_t('What to do', language)}:** "
            f"{_policy_text(policy, 'steps', language)}"
        )
        st.warning(_policy_text(policy, "remember", language))
        st.link_button(
            localized.get("source_name", _t(policy["source_name"], language)),
            policy["source"],
            use_container_width=False,
        )
        if policy.get("extra_source"):
            st.link_button(
                localized.get(
                    "extra_source_name",
                    _t(policy["extra_source_name"], language),
                ),
                policy["extra_source"],
                use_container_width=False,
            )


def _render_profit_calculator(language: str) -> None:
    st.markdown(f"### {_t('Simple crop cost and profit calculator', language)}")
    st.caption(
        _t(
            "Enter your own expected yield, sale price and costs. This is a planning "
            "estimate, not a guaranteed price or profit.",
            language,
        )
    )
    with st.form("policy_farm_profit_form"):
        yield_per_acre = st.number_input(
            _t("Expected yield (quintals per acre)", language),
            min_value=0.0,
            value=0.0,
            step=0.5,
        )
        sale_price = st.number_input(
            _t("Expected sale price (₹ per quintal)", language),
            min_value=0.0,
            value=0.0,
            step=100.0,
        )
        acres = st.number_input(
            _t("Area (acres)", language),
            min_value=0.1,
            value=1.0,
            step=0.5,
        )
        st.markdown(f"**{_t('Estimated costs per acre', language)}**")
        cost_columns = st.columns(3)
        cost_labels = [
            ("Seed and planting (₹)", "seed"),
            ("Fertiliser and soil care (₹)", "fertiliser"),
            ("Sprays and crop care (₹)", "crop_care"),
            ("Labour (₹)", "labour"),
            ("Water and energy (₹)", "water"),
            ("Harvest and machinery (₹)", "machinery"),
            ("Transport and market charges (₹)", "transport"),
            ("Other costs (₹)", "other"),
        ]
        costs = {}
        for index, (label, key) in enumerate(cost_labels):
            costs[key] = cost_columns[index % len(cost_columns)].number_input(
                _t(label, language),
                min_value=0.0,
                value=0.0,
                step=500.0,
                key=f"policy_cost_{key}",
            )
        submitted = st.form_submit_button(_t("Calculate estimate", language))

    if submitted:
        result = calculate_farm_profit(yield_per_acre, sale_price, costs, acres)
        metric_columns = st.columns(3)
        metric_columns[0].metric(
            _t("Estimated total sales", language),
            f"₹{result['total_gross']:,.0f}",
        )
        metric_columns[1].metric(
            _t("Estimated total cost", language),
            f"₹{result['total_cost']:,.0f}",
        )
        metric_columns[2].metric(
            _t("Estimated profit / (loss)", language),
            f"₹{result['total_profit']:,.0f}",
        )
        st.caption(
            _t(
                "Sales = yield × sale price. Profit = sales − entered costs. "
                "This simple estimate may not include family labour, land rent, "
                "loan interest, storage or price changes unless you enter them.",
                language,
            )
        )


def render_policies(language: str = "en") -> None:
    """Render simple policy explainers, official links, and a crop-profit tool."""
    st.subheader(_t("Policies for farmers", language))
    st.write(
        _t(
            "Simple guides to Indian and Maharashtra schemes, crop selling, "
            "farm loans, and import/export rules.",
            language,
        )
    )
    st.info(
        _t(
            "Rules, amounts, deadlines and eligibility can change. Use the official "
            "government link for the latest details. Never pay an agent who promises "
            "a guaranteed scheme benefit.",
            language,
        )
    )

    topic_names = list(POLICY_TOPICS)
    selected_topic = st.selectbox(
        _t("Choose what you want to know about", language),
        topic_names,
        format_func=lambda topic: _t(topic, language),
    )
    for policy in POLICY_TOPICS[selected_topic]:
        _render_policy_card(policy, language)

    st.divider()
    _render_profit_calculator(language)
