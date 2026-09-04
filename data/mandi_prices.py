"""
Simulated Mandi Prices & Historical Analytics for Major Agricultural Commodities
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_mandi_price_history(crop_id):
    """
    Returns 12-month historical price trend data (₹/Quintal) and 3-month forecast
    """
    base_prices = {
        "wheat": 2250,
        "paddy": 2180,
        "soybean": 4500,
        "cotton": 6500,
        "mustard": 5500,
        "chana": 5300,
        "maize": 2150,
        "tomato": 2500
    }
    
    base = base_prices.get(crop_id, 3000)
    
    # Generate past 12 months
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_month_idx = datetime.now().month - 1
    
    # Reorder months to end with current month
    ordered_months = []
    prices = []
    forecast_flags = []
    
    np.random.seed(hash(crop_id) % 10000)
    fluctuations = np.sin(np.linspace(0, 3*np.pi, 15)) * (base * 0.12)
    
    for i in range(12):
        idx = (current_month_idx - 11 + i) % 12
        ordered_months.append(months[idx])
        noise = np.random.normal(0, base * 0.03)
        p = int(base + fluctuations[i] + noise)
        prices.append(max(p, int(base * 0.7)))
        forecast_flags.append("Historical")
        
    # Add 3 months forecast
    for i in range(1, 4):
        idx = (current_month_idx + i) % 12
        ordered_months.append(months[idx] + " (Fcst)")
        noise = np.random.normal(0, base * 0.02)
        p = int(base + fluctuations[11 + i] + noise * 1.5)
        prices.append(max(p, int(base * 0.75)))
        forecast_flags.append("Forecast")

    df = pd.DataFrame({
        "Month": ordered_months,
        "Price (₹/Quintal)": prices,
        "Type": forecast_flags
    })
    
    return df

def get_market_advisory(crop_id):
    """
    Returns optimal selling month and profit outlook
    """
    advisories = {
        "wheat": {"best_month": "April / May (Post Harvest)", "outlook": "Steady demand from flour mills. Hold 15% stock for festival surge."},
        "paddy": {"best_month": "January / February", "outlook": "Export demand remains strong. Basmati varieties fetching premium."},
        "soybean": {"best_month": "December / January", "outlook": "Global edible oil trends favor price appreciation in winter."},
        "cotton": {"textile": "March / April", "best_month": "March / April", "outlook": "Ginners stocking up. Good export realization expected."},
        "mustard": {"best_month": "May / June", "outlook": "Domestic oil extraction demand peaking."},
        "chana": {"best_month": "October / November", "outlook": "Festival season demand (Diwali/Festivals) pushes pulse prices."},
        "maize": {"best_month": "February / March", "outlook": "Poultry feed industry demand is buoyant."},
        "tomato": {"best_month": "Off-season (Monsoon or Winter Peak)", "outlook": "High price volatility. Cold storage linkage recommended."}
    }
    return advisories.get(crop_id, {"best_month": "3 months post harvest", "outlook": "Sell in phased manner to average out price volatility."})
