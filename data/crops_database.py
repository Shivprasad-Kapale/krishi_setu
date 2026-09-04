"""
Comprehensive Crop Database with agronomic requirements, soil compatibility,
water usage, cost of cultivation, yield per acre, and historical price volatility.
"""

CROP_DATABASE = [
    {
        "id": "wheat",
        "name_en": "Wheat (गेहूं)",
        "name_hi": "गेहूं",
        "season": "Rabi",
        "suitable_soils": ["Alluvial Soil (जलोढ़ मिट्टी)", "Clay Loam (दोमट मिट्टी)"],
        "min_water_mm": 450,
        "max_water_mm": 650,
        "duration_days": 120,
        "cost_per_acre": 14000,
        "avg_yield_quintals_per_acre": 18,
        "msp_or_base_price": 2275, # per quintal
        "market_demand_trend": "High & Stable",
        "risk_level": "Low",
        "fertilizer_schedule": [
            {"day": 0, "task": "Basal NPK application (120:60:40 kg/ha)"},
            {"day": 21, "task": "1st Irrigation (CRI stage) + Urea top dressing"},
            {"day": 45, "task": "2nd Irrigation (Tillering stage) + Weed control"},
            {"day": 75, "task": "3rd Irrigation (Flowering stage)"},
            {"day": 105, "task": "Stop irrigation before harvest"}
        ],
        "common_diseases": [
            {"name": "Yellow Rust (पीला रतुआ)", "symptom": "Yellow stripes on leaves", "remedy": "Propiconazole 25% EC spray"},
            {"name": "Loose Smut", "symptom": "Black ear heads", "remedy": "Seed treatment with Vitavax"}
        ]
    },
    {
        "id": "paddy",
        "name_en": "Paddy / Rice (धान)",
        "name_hi": "धान / चावल",
        "season": "Kharif",
        "suitable_soils": ["Alluvial Soil (जलोढ़ मिट्टी)", "Clay Loam (दोमट मिट्टी)", "Black Soil / Regur (काली मिट्टी)"],
        "min_water_mm": 1100,
        "max_water_mm": 1500,
        "duration_days": 135,
        "cost_per_acre": 18500,
        "avg_yield_quintals_per_acre": 22,
        "msp_or_base_price": 2300,
        "market_demand_trend": "Very High",
        "risk_level": "Medium",
        "fertilizer_schedule": [
            {"day": 0, "task": "Puddling and basal NPK application"},
            {"day": 20, "task": "1st Urea application after weeding"},
            {"day": 45, "task": "2nd Urea top dressing at tillering"},
            {"day": 70, "task": "Panicle initiation irrigation & potash spray"}
        ],
        "common_diseases": [
            {"name": "Blast (ब्लास्ट रोग)", "symptom": "Spindle-shaped spots on leaves with gray centers", "remedy": "Tricyclazole 75% WP spray"},
            {"name": "Bacterial Leaf Blight", "symptom": "Yellowish-white water-soaked stripes", "remedy": "Copper oxychloride + Streptocycline"}
        ]
    },
    {
        "id": "soybean",
        "name_en": "Soybean (सोयाबीन)",
        "name_hi": "सोयाबीन",
        "season": "Kharif",
        "suitable_soils": ["Black Soil / Regur (काली मिट्टी)", "Clay Loam (दोमट मिट्टी)"],
        "min_water_mm": 500,
        "max_water_mm": 700,
        "duration_days": 100,
        "cost_per_acre": 11000,
        "avg_yield_quintals_per_acre": 10,
        "msp_or_base_price": 4600,
        "market_demand_trend": "High Export Demand",
        "risk_level": "Medium",
        "fertilizer_schedule": [
            {"day": 0, "task": "Rhizobium inoculation & basal SSP + MOP"},
            {"day": 30, "task": "Interculturing and manual weeding"},
            {"day": 45, "task": "Yellow mosaic virus vector check"}
        ],
        "common_diseases": [
            {"name": "Collar Rot", "symptom": "White fungal growth near soil line", "remedy": "Trichoderma seed treatment"},
            {"name": "Stem Fly", "symptom": "Wilting and dried plants", "remedy": "Thiamethoxam seed dressing"}
        ]
    },
    {
        "id": "cotton",
        "name_en": "Cotton (कपास)",
        "name_hi": "कपास",
        "season": "Kharif",
        "suitable_soils": ["Black Soil / Regur (काली मिट्टी)", "Alluvial Soil (जलोढ़ मिट्टी)"],
        "min_water_mm": 700,
        "max_water_mm": 1200,
        "duration_days": 160,
        "cost_per_acre": 22000,
        "avg_yield_quintals_per_acre": 9,
        "msp_or_base_price": 6620,
        "market_demand_trend": "High Industrial Demand",
        "risk_level": "High",
        "fertilizer_schedule": [
            {"day": 0, "task": "Deep plowing and baseline organic manure"},
            {"day": 30, "task": "Nitrogen split dose + Earthing up"},
            {"day": 60, "task": "Boll formation micro-nutrient spray (MgSO4)"}
        ],
        "common_diseases": [
            {"name": "Pink Bollworm (गुलाबी सुंडी)", "symptom": "Damaged bolls and stained lint", "remedy": "Pheromone traps and Quinalphos"},
            {"name": "Leaf Curl Virus", "symptom": "Upward curling of leaves", "remedy": "Imidacloprid for whitefly control"}
        ]
    },
    {
        "id": "mustard",
        "name_en": "Mustard (सरसों)",
        "name_hi": "सरसों",
        "season": "Rabi",
        "suitable_soils": ["Sandy / Arid Soil (रेतीली मिट्टी)", "Alluvial Soil (जलोढ़ मिट्टी)", "Light Loam"],
        "min_water_mm": 350,
        "max_water_mm": 500,
        "duration_days": 110,
        "cost_per_acre": 9500,
        "avg_yield_quintals_per_acre": 8,
        "msp_or_base_price": 5650,
        "market_demand_trend": "High Edible Oil Demand",
        "risk_level": "Low",
        "fertilizer_schedule": [
            {"day": 0, "task": "Basal application of N, P, K and Sulphur"},
            {"day": 30, "task": "1st Irrigation at Rosette stage + Thinning"}
        ],
        "common_diseases": [
            {"name": "Alternaria Blight", "symptom": "Concentric dark brown spots on leaves", "remedy": "Mancozeb 75% WP spray"},
            {"name": "White Rust", "symptom": "White pustules on underside of leaves", "remedy": "Metalaxyl spray"}
        ]
    },
    {
        "id": "chana",
        "name_en": "Chickpea / Chana (चना)",
        "name_hi": "चना",
        "season": "Rabi",
        "suitable_soils": ["Red & Yellow Soil (लाल और पीली मिट्टी)", "Black Soil / Regur (काली मिट्टी)", "Light Loam"],
        "min_water_mm": 250,
        "max_water_mm": 400,
        "duration_days": 120,
        "cost_per_acre": 10000,
        "avg_yield_quintals_per_acre": 7.5,
        "msp_or_base_price": 5440,
        "market_demand_trend": "Very High Protein Demand",
        "risk_level": "Low",
        "fertilizer_schedule": [
            {"day": 0, "task": "Phosphorus rich basal application (SSP)"},
            {"day": 45, "task": "Nipping (topping) to encourage branching"}
        ],
        "common_diseases": [
            {"name": "Fusarium Wilt", "symptom": "Sudden yellowing and drooping of seedlings", "remedy": "Seed treatment with Carbendazim + Thiram"},
            {"name": "Pod Borer", "symptom": "Circular holes in pods", "remedy": "HaNPV or Emamectin benzoate"}
        ]
    },
    {
        "id": "maize",
        "name_en": "Maize / Corn (मक्का)",
        "name_hi": "मक्का",
        "season": "Kharif / Rabi",
        "suitable_soils": ["Alluvial Soil (जलोढ़ मिट्टी)", "Red & Yellow Soil (लाल और पीली मिट्टी)", "Clay Loam (दोमट मिट्टी)"],
        "min_water_mm": 500,
        "max_water_mm": 800,
        "duration_days": 95,
        "cost_per_acre": 12500,
        "avg_yield_quintals_per_acre": 24,
        "msp_or_base_price": 2225,
        "market_demand_trend": "High Poultry & Ethanol Demand",
        "risk_level": "Low",
        "fertilizer_schedule": [
            {"day": 0, "task": "Basal NPK application"},
            {"day": 25, "task": "Knee-high stage nitrogen side dressing"},
            {"day": 50, "task": "Tasselling stage irrigation"}
        ],
        "common_diseases": [
            {"name": "Fall Armyworm (फॉल आर्मीवर्म)", "symptom": "Shothole damage in whorl leaves", "remedy": "Spinetoram 12.5% SC spray"},
            {"name": "Maydis Leaf Blight", "symptom": "Elliptical tan lesions on leaves", "remedy": "Propiconazole spray"}
        ]
    },
    {
        "id": "tomato",
        "name_en": "Tomato (टमाटर)",
        "name_hi": "टमाटर",
        "season": "Zaid / All Season",
        "suitable_soils": ["Alluvial Soil (जलोढ़ मिट्टी)", "Sandy Loam (बलुई दोमट)"],
        "min_water_mm": 600,
        "max_water_mm": 900,
        "duration_days": 90,
        "cost_per_acre": 28000,
        "avg_yield_quintals_per_acre": 120,
        "msp_or_base_price": 2000, # Variable market price per quintal base
        "market_demand_trend": "High Fluctuating (High Peak Profit)",
        "risk_level": "High",
        "fertilizer_schedule": [
            {"day": 0, "task": "FYM + Bed preparation & staking setup"},
            {"day": 15, "task": "Drip fertigation with soluble NPK 19:19:19"},
            {"day": 45, "task": "Calcium Nitrate spray to prevent blossom end rot"}
        ],
        "common_diseases": [
            {"name": "Early Blight", "symptom": "Target-board concentric rings on leaves", "remedy": "Chlorothalonil or Mancozeb"},
            {"name": "Tomato Leaf Curl Virus", "symptom": "Stunted growth and curled yellow leaves", "remedy": "Control whiteflies with Imidacloprid"}
        ]
    }
]
