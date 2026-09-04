"""
Direct Marketplace, Buyer Demand Board & Contract Farming Module (Local JSON / SQLite DB)
"""

import json
import os
from datetime import datetime

DB_FILE = "marketplace_data.json"

def init_db():
    if not os.path.exists(DB_FILE):
        initial_data = {
            "listings": [
                {
                    "id": "L101",
                    "farmer_name": "Ramesh Patil",
                    "district": "Nashik, Maharashtra",
                    "crop": "Wheat (गेहूं)",
                    "quantity_quintals": 150,
                    "expected_price": 2350,
                    "harvest_date": "2026-04-15",
                    "status": "Available / Open for Contract"
                },
                {
                    "id": "L102",
                    "farmer_name": "Gurpreet Singh",
                    "district": "Ludhiana, Punjab",
                    "crop": "Paddy / Rice (धान)",
                    "quantity_quintals": 300,
                    "expected_price": 2400,
                    "harvest_date": "2026-11-20",
                    "status": "Under Negotiation"
                },
                {
                    "id": "L103",
                    "farmer_name": "Suresh Deshmukh",
                    "district": "Indore, Madhya Pradesh",
                    "crop": "Soybean (सोयाबीन)",
                    "quantity_quintals": 80,
                    "expected_price": 4700,
                    "harvest_date": "2026-10-10",
                    "status": "Available / Open for Contract"
                }
            ],
            "buyer_demands": [
                {
                    "id": "B201",
                    "buyer_org": "AgroCorp Foods Ltd.",
                    "crop": "Wheat (गेहूं)",
                    "required_quintals": 1000,
                    "offered_price": 2380,
                    "delivery_location": "Mumbai Hub",
                    "contact": "procurement@agrocorp.in"
                },
                {
                    "id": "B202",
                    "buyer_org": "National Retail Syndicate",
                    "crop": "Tomato (टमाटर)",
                    "required_quintals": 250,
                    "offered_price": 2200,
                    "delivery_location": "Delhi Mandi",
                    "contact": "supply@nrsretail.com"
                }
            ]
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=4)

def load_data():
    init_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_farmer_listing(farmer_name, district, crop, quantity, price, harvest_date):
    data = load_data()
    new_id = f"L10{len(data['listings']) + 1}"
    listing = {
        "id": new_id,
        "farmer_name": farmer_name,
        "district": district,
        "crop": crop,
        "quantity_quintals": int(quantity),
        "expected_price": float(price),
        "harvest_date": str(harvest_date),
        "status": "Available / Open for Contract"
    }
    data["listings"].append(listing)
    save_data(data)
    return True

def add_buyer_demand(buyer_org, crop, quantity, price, location, contact):
    data = load_data()
    new_id = f"B20{len(data['buyer_demands']) + 1}"
    demand = {
        "id": new_id,
        "buyer_org": buyer_org,
        "crop": crop,
        "required_quintals": int(quantity),
        "offered_price": float(price),
        "delivery_location": location,
        "contact": contact
    }
    data["buyer_demands"].append(demand)
    save_data(data)
    return True
