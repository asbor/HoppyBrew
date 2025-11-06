#!/usr/bin/env python3
"""
Sample data loader for HoppyBrew backend
Loads the generated sample data into the FastAPI backend via API calls
"""

import json
import requests
import sys
from typing import Dict, Any, List

# Backend API configuration
API_BASE_URL = "http://localhost:8000"

def load_json_file(filename: str) -> Dict[str, Any]:
    """Load JSON data from file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found. Run generate_sample_data.py first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {filename}")
        sys.exit(1)

def check_backend_connection() -> bool:
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def load_recipes(recipes: List[Dict[str, Any]]) -> Dict[str, str]:
    """Load recipes and return mapping of old_id -> new_id"""
    print("📝 Loading recipes...")
    
    recipe_id_mapping = {}
    
    for recipe in recipes:
        old_id = recipe.pop('id')  # Remove old ID
        
        try:
            response = requests.post(f"{API_BASE_URL}/recipes", json=recipe)
            if response.status_code == 201:
                new_recipe = response.json()
                recipe_id_mapping[old_id] = str(new_recipe['id'])
                print(f"  ✅ Created recipe: {recipe['name']}")
            else:
                print(f"  ❌ Failed to create recipe {recipe['name']}: {response.text}")
        except requests.RequestException as e:
            print(f"  ❌ Error creating recipe {recipe['name']}: {e}")
    
    return recipe_id_mapping

def load_batches(batches: List[Dict[str, Any]], recipe_mapping: Dict[str, str]) -> Dict[str, str]:
    """Load batches and return mapping of old_id -> new_id"""
    print("🍺 Loading batches...")
    
    batch_id_mapping = {}
    
    for batch in batches:
        old_id = batch.pop('id')  # Remove old ID
        old_recipe_id = batch['recipe_id']
        
        # Update recipe_id with new mapping
        if old_recipe_id in recipe_mapping:
            batch['recipe_id'] = int(recipe_mapping[old_recipe_id])
        else:
            print(f"  ⚠️  Warning: Recipe ID {old_recipe_id} not found in mapping")
            continue
        
        # Remove recipe object if it exists (not part of API schema)
        batch.pop('recipe', None)
        
        try:
            response = requests.post(f"{API_BASE_URL}/batches", json=batch)
            if response.status_code == 201:
                new_batch = response.json()
                batch_id_mapping[old_id] = str(new_batch['id'])
                print(f"  ✅ Created batch: {batch['batch_name']} (Status: {batch['status']})")
            else:
                print(f"  ❌ Failed to create batch {batch['batch_name']}: {response.text}")
        except requests.RequestException as e:
            print(f"  ❌ Error creating batch {batch['batch_name']}: {e}")
    
    return batch_id_mapping

def load_readings(readings: List[Dict[str, Any]], batch_mapping: Dict[str, str]):
    """Load batch readings"""
    print("📊 Loading batch readings...")
    
    for reading in readings:
        reading.pop('id', None)  # Remove old ID
        old_batch_id = reading['batch_id']
        
        # Update batch_id with new mapping
        if old_batch_id in batch_mapping:
            reading['batch_id'] = int(batch_mapping[old_batch_id])
        else:
            print(f"  ⚠️  Warning: Batch ID {old_batch_id} not found in mapping")
            continue
        
        try:
            # Note: Adjust endpoint based on your actual API structure
            response = requests.post(f"{API_BASE_URL}/batch_readings", json=reading)
            if response.status_code == 201:
                print(f"  ✅ Created reading for batch {old_batch_id}: SG {reading['gravity']}")
            else:
                print(f"  ❌ Failed to create reading: {response.text}")
        except requests.RequestException as e:
            print(f"  ❌ Error creating reading: {e}")

def main():
    """Main loading process"""
    print("🚀 Loading Sample Data into HoppyBrew Backend")
    print("=" * 50)
    
    # Check backend connection
    if not check_backend_connection():
        print("❌ Error: Cannot connect to backend at http://localhost:8000")
        print("   Make sure the backend is running: cd services/backend && python main.py")
        sys.exit(1)
    
    print("✅ Backend connection successful")
    
    # Load sample data files
    try:
        data = load_json_file('sample_brewing_data.json')
        recipes = data['recipes']
        batches = data['batches'] 
        readings = data['batch_readings']
    except KeyError as e:
        print(f"❌ Error: Missing key {e} in sample data")
        sys.exit(1)
    
    print(f"📄 Loaded {len(recipes)} recipes, {len(batches)} batches, {len(readings)} readings")
    print()
    
    # Load data in order (recipes first, then batches, then readings)
    recipe_mapping = load_recipes(recipes)
    print()
    
    batch_mapping = load_batches(batches, recipe_mapping)
    print()
    
    load_readings(readings, batch_mapping)
    print()
    
    print("🎉 Sample data loading complete!")
    print("\nYou can now:")
    print("  - Visit http://localhost:3000/batches to see the batch list")
    print("  - Click on any batch to see the brewing workflow phases")
    print("  - Try different batch statuses:")
    print("    • Planning phase: Batch #33")
    print("    • Brew day phase: Batch #1") 
    print("    • Fermentation phase: Batch #47")
    print("    • Conditioning phase: Batch #45")
    print("    • Packaged phase: Batch #44")
    print("    • Completed phase: Batch #43")

if __name__ == "__main__":
    main()