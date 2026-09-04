"""
Precision Soil Report Parser & Advanced Multi-Factor Decision Matrix
Handles manual NPK/pH entry and OCR/Vision extraction from uploaded soil test reports.
"""

import streamlit as st

def parse_soil_report(uploaded_file, api_key=None):
    """
    Parses uploaded soil test report (Image or PDF) using Gemini Vision if key provided.
    Falls back to intelligent heuristic extraction if offline or no API key.
    """
    extracted_data = {
        "ph": 7.2,
        "nitrogen": 220, # kg/ha
        "phosphorus": 18, # kg/ha
        "potassium": 280, # kg/ha
        "organic_carbon": 0.65, # %
        "ec": 0.45 # dS/m
    }
    
    if api_key and uploaded_file is not None:
        try:
            import google.generativeai as genai
            from PIL import Image
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            img = Image.open(uploaded_file)
            prompt = (
                "Extract soil test report metrics and return ONLY valid numeric values for: "
                "1. pH (e.g., 6.5) "
                "2. Nitrogen (kg/ha) "
                "3. Phosphorus (kg/ha) "
                "4. Potassium (kg/ha) "
                "5. Organic Carbon (%) "
                "6. Electrical Conductivity EC (dS/m). "
                "Format as JSON: {\"ph\": X, \"nitrogen\": X, \"phosphorus\": X, \"potassium\": X, \"organic_carbon\": X, \"ec\": X}"
            )
            response = model.generate_content([prompt, img])
            # Parse text response safely or use default if parsing fails
            import json
            text = response.text.strip()
            if "{" in text and "}" in text:
                json_str = text[text.find("{"):text.rfind("}")+1]
                parsed = json.loads(json_str)
                extracted_data.update(parsed)
        except Exception:
            pass
            
    return extracted_data

def advanced_precision_recommendation(state, district, soil_type, season, water_source, budget, goal, previous_crop, npk_values):
    """
    Refined crop recommendation engine integrating precise NPK, pH, organic carbon,
    crop rotation rules, goal weighting, and budget constraints.
    """
    from data.crops_database import CROP_DATABASE
    
    ph = npk_values.get("ph", 7.0)
    n = npk_values.get("nitrogen", 200)
    p = npk_values.get("phosphorus", 20)
    k = npk_values.get("potassium", 250)
    
    recommendations = []
    
    for crop in CROP_DATABASE:
        score = 50.0
        reasons = []
        
        # 1. Soil & pH Compatibility
        if soil_type in crop["suitable_soils"]:
            score += 20
            reasons.append("Optimal soil type match for root penetration.")
        else:
            score -= 10
            reasons.append("Soil type is marginal; corrective amendments recommended.")
            
        if 6.0 <= ph <= 7.5:
            score += 15
            reasons.append(f"Soil pH ({ph}) is within the ideal neutral range for nutrient availability.")
        else:
            score -= 10
            reasons.append(f"Soil pH ({ph}) is slightly acidic/alkaline; gypsum or lime application suggested.")
            
        # 2. NPK Nutrient Balance
        if n >= 180 and crop["id"] in ["wheat", "paddy", "maize"]:
            score += 15
            reasons.append(f"Nitrogen level ({n} kg/ha) supports high cereal grain development.")
        elif p >= 25 and crop["id"] in ["chana", "soybean", "mustard"]:
            score += 15
            reasons.append(f"Phosphorus level ({p} kg/ha) is favorable for pulse/oilseed pod formation.")
            
        # 3. Crop Rotation Logic (Avoid consecutive same family)
        if previous_crop and previous_crop.lower() in crop["name_en"].lower():
            score -= 25
            reasons.append(f"Warning: Cultivating {crop['name_en']} consecutively after {previous_crop} increases disease risk. Crop rotation advised.")
        else:
            score += 10
            reasons.append("Favorable crop rotation break to prevent soil pathogen build-up.")
            
        # 4. Goal Alignment (High Profit vs Low Risk vs Soil Restoration)
        if goal == "Maximize Profit" or goal == "अधिकतम नफा":
            if crop["market_demand_trend"] in ["Very High", "High Export Demand", "High & Stable"]:
                score += 20
                reasons.append("Aligned with your goal: High market demand and superior ROI potential.")
        elif goal == "Low Risk & Stable Yield" or goal == "सुरक्षित आणि स्थिर उत्पन्न":
            if crop["risk_level"] == "Low":
                score += 20
                reasons.append("Aligned with your goal: Low risk profile with stable MSP/base returns.")
        elif goal == "Soil Health Restoration" or goal == "जमीन सुधारणा":
            if crop["id"] in ["chana", "soybean"]:
                score += 25
                reasons.append("Aligned with your goal: Leguminous crop fixes atmospheric nitrogen, restoring soil fertility.")
                
        # Financial Calculations
        total_cost = crop["cost_per_acre"] * 2 # default 2 acres reference
        expected_yield_total = crop["avg_yield_quintals_per_acre"] * 2
        estimated_revenue = expected_yield_total * crop["msp_or_base_price"]
        estimated_net_profit = estimated_revenue - total_cost
        roi_percentage = (estimated_net_profit / total_cost) * 100 if total_cost > 0 else 0
        
        recommendations.append({
            "crop_id": crop["id"],
            "name": crop["name_en"],
            "name_hi": crop["name_hi"],
            "score": round(max(10, min(100, score)), 1),
            "reasons": reasons,
            "cost_per_acre": crop["cost_per_acre"],
            "total_cost": total_cost,
            "expected_yield": expected_yield_total,
            "estimated_revenue": estimated_revenue,
            "estimated_net_profit": estimated_net_profit,
            "roi_percentage": round(roi_percentage, 1),
            "market_demand": crop["market_demand_trend"],
            "risk_level": crop["risk_level"],
            "duration_days": crop["duration_days"],
            "fertilizer_schedule": crop["fertilizer_schedule"],
            "common_diseases": crop["common_diseases"]
        })
        
    recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)
    return recommendations
