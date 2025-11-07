#!/usr/bin/env python3
"""
Quick seed data script for HoppyBrew development
Creates minimal sample data to make the application useful for testing
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is healthy and running")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the backend running on port 8000?")
        return False

def add_sample_fermentables():
    """Add basic fermentables for brewing"""
    fermentables = [
        {
            "name": "Pale Malt (2-Row)",
            "type": "Base Malt",
            "origin": "UK",
            "supplier": "Crisp",
            "color_ebc": 5.0,
            "max_in_batch": 100.0,
            "potential": 1.036,
            "inventory_kg": 25.0
        },
        {
            "name": "Munich Malt",
            "type": "Base Malt", 
            "origin": "Germany",
            "supplier": "Weyermann",
            "color_ebc": 16.0,
            "max_in_batch": 80.0,
            "potential": 1.035,
            "inventory_kg": 10.0
        },
        {
            "name": "Crystal 60L",
            "type": "Crystal/Caramel",
            "origin": "UK",
            "supplier": "Crisp",
            "color_ebc": 118.0,
            "max_in_batch": 15.0,
            "potential": 1.034,
            "inventory_kg": 5.0
        },
        {
            "name": "Chocolate Malt",
            "type": "Roasted",
            "origin": "UK", 
            "supplier": "Crisp",
            "color_ebc": 1000.0,
            "max_in_batch": 10.0,
            "potential": 1.028,
            "inventory_kg": 2.0
        }
    ]
    
    print("🌾 Adding sample fermentables...")
    for fermentable in fermentables:
        try:
            response = requests.post(f"{BASE_URL}/inventory/fermentables", json=fermentable)
            if response.status_code in [200, 201]:
                print(f"  ✅ Added: {fermentable['name']}")
            else:
                print(f"  ❌ Failed to add {fermentable['name']}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error adding {fermentable['name']}: {str(e)}")

def add_sample_hops():
    """Add basic hops for brewing"""
    hops = [
        {
            "name": "Cascade",
            "alpha_acids": 6.5,
            "beta_acids": 5.0,
            "cohumulone": 35.0,
            "origin": "USA",
            "hop_type": "Aroma",
            "form": "Pellet",
            "inventory_grams": 500.0
        },
        {
            "name": "Citra",
            "alpha_acids": 12.0,
            "beta_acids": 4.0,
            "cohumulone": 22.0,
            "origin": "USA", 
            "hop_type": "Aroma",
            "form": "Pellet",
            "inventory_grams": 250.0
        },
        {
            "name": "East Kent Goldings",
            "alpha_acids": 5.5,
            "beta_acids": 3.0,
            "cohumulone": 25.0,
            "origin": "UK",
            "hop_type": "Aroma",
            "form": "Whole",
            "inventory_grams": 200.0
        },
        {
            "name": "Magnum",
            "alpha_acids": 14.0,
            "beta_acids": 5.5,
            "cohumulone": 25.0,
            "origin": "Germany",
            "hop_type": "Bittering", 
            "form": "Pellet",
            "inventory_grams": 300.0
        }
    ]
    
    print("🌿 Adding sample hops...")
    for hop in hops:
        try:
            response = requests.post(f"{BASE_URL}/inventory/hops", json=hop)
            if response.status_code in [200, 201]:
                print(f"  ✅ Added: {hop['name']}")
            else:
                print(f"  ❌ Failed to add {hop['name']}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error adding {hop['name']}: {str(e)}")

def add_sample_yeasts():
    """Add basic yeasts for brewing"""
    yeasts = [
        {
            "name": "SafAle US-05",
            "lab": "Fermentis",
            "product_id": "US-05",
            "yeast_type": "Ale",
            "form": "Dry",
            "attenuation": 81.0,
            "flocculation": "Medium",
            "tolerance": 12.0,
            "temp_range_low": 15.0,
            "temp_range_high": 24.0,
            "inventory_units": 10
        },
        {
            "name": "SafLager S-23",
            "lab": "Fermentis",
            "product_id": "S-23", 
            "yeast_type": "Lager",
            "form": "Dry",
            "attenuation": 82.0,
            "flocculation": "High",
            "tolerance": 15.0,
            "temp_range_low": 9.0,
            "temp_range_high": 22.0,
            "inventory_units": 5
        },
        {
            "name": "Wyeast 1056 American Ale",
            "lab": "Wyeast",
            "product_id": "1056",
            "yeast_type": "Ale", 
            "form": "Liquid",
            "attenuation": 77.0,
            "flocculation": "Medium-Low",
            "tolerance": 11.0,
            "temp_range_low": 16.0,
            "temp_range_high": 22.0,
            "inventory_units": 3
        }
    ]
    
    print("🦠 Adding sample yeasts...")
    for yeast in yeasts:
        try:
            response = requests.post(f"{BASE_URL}/inventory/yeasts", json=yeast)
            if response.status_code in [200, 201]:
                print(f"  ✅ Added: {yeast['name']}")
            else:
                print(f"  ❌ Failed to add {yeast['name']}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error adding {yeast['name']}: {str(e)}")

def main():
    print("🍺 HoppyBrew Quick Seed Data Script")
    print("=" * 40)
    
    if not check_api_health():
        print("\n❌ Cannot proceed without a healthy API connection.")
        print("💡 Make sure the backend is running: docker-compose up -d backend")
        sys.exit(1)
    
    print("\n🌱 Adding basic brewing ingredients...")
    
    add_sample_fermentables()
    add_sample_hops() 
    add_sample_yeasts()
    
    print("\n" + "=" * 40)
    print("✅ Seed data script completed!")
    print("\n💡 Next steps:")
    print("   1. Visit http://localhost:3000 to see the frontend")
    print("   2. Check inventory pages to see the sample data")
    print("   3. Try creating a recipe with the sample ingredients")
    print("   4. Visit http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    main()