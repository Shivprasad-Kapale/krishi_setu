"""
Smart Crop Planner Engine: Computes ROI, Soil Suitability, Water Requirements, and Rank Crops.
"""

from data.crops_database import CROP_DATABASE

def calculate_crop_recommendations(state, district, soil_type, land_size, season, water_source, budget_per_acre, farmer_experience=0, previous_crops=[]):
    """
    Evaluates all crops in the database against farmer's constraints and scores them
    using advanced weighted multi-factor decision matrix.
    """
    recommendations = []
    
    weights = {
        "soil_match": 0.25,
        "season_match": 0.20,
        "budget_match": 0.20,
        "water_match": 0.20,
        "market_demand": 0.15
    }
    
    for crop in CROP_DATABASE:
        score = 50.0
        reasons = []
        
        # 1. Soil Suitability Check
        if soil_type in crop["suitable_soils"]:
            soil_score = 100
            reasons.append("✅ Perfect soil match for root development & nutrient uptake")
        else:
            soil_score = 40
            reasons.append("⚠️ Soil type is suboptimal; requires organic amendment")
            
        # 2. Season Match
        if season.lower() in crop["season"].lower() or "all season" in crop["season"].lower():
            season_score = 100
            reasons.append(f"✅ Aligned with optimal growing season ({crop['season']})")
        else:
            season_score = 30
            reasons.append(f"⚠️ Out of primary season ({crop['season']}); needs controlled environment")
            
        # 3. Budget & Cost Check
        if budget_per_acre >= crop["cost_per_acre"]:
            budget_score = 100
            reasons.append("✅ Budget covers estimated cultivation cost per acre")
        else:
            budget_score = 20
            reasons.append(f"❌ Budget is lower than estimated cost (₹{crop['cost_per_acre']:,}/acre)")
            
        # 4. Water Availability Check
        water_score_map = {"Rainfed Only": 400, "Tube Well / Borewell": 900, "Canal Irrigation": 1200, "Drip / Sprinkler": 700}
        available_water = water_score_map.get(water_source, 600)
        
        if available_water >= crop["min_water_mm"]:
            water_score = 100
            reasons.append(f"✅ Water availability ({available_water}mm) meets crop needs ({crop['min_water_mm']}mm)")
        else:
            water_score = 10
            reasons.append(f"❌ Water deficit: Crop requires min {crop['min_water_mm']}mm")
            
        # 5. Market Demand
        demand_score = 90 if "High" in crop["market_demand_trend"] else 70
        
        # Weighted Final Score Calculation
        final_score = (
            soil_score * weights["soil_match"] +
            season_score * weights["season_match"] +
            budget_score * weights["budget_match"] +
            water_score * weights["water_match"] +
            demand_score * weights["market_demand"]
        )
            
        # Financial Calculations
        total_cost = crop["cost_per_acre"] * land_size
        expected_yield_total = crop["avg_yield_quintals_per_acre"] * land_size
        estimated_revenue = expected_yield_total * crop["msp_or_base_price"]
        estimated_net_profit = estimated_revenue - total_cost
        roi_percentage = (estimated_net_profit / total_cost) * 100 if total_cost > 0 else 0
        
        recommendations.append({
            "crop_id": crop["id"],
            "name": crop["name_en"],
            "name_hi": crop["name_hi"],
            "score": round(max(10, min(100, final_score)), 1),
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
        
    # Sort by Score descending
    recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)
    return recommendations
