#!/usr/bin/env python3
"""
Sample batch data seeder for HoppyBrew
Creates realistic sample batches with different statuses to demonstrate the brewing workflow
"""

import json
import datetime
from typing import List, Dict, Any

def create_sample_batches() -> List[Dict[str, Any]]:
    """Create a collection of sample batches in different phases"""
    
    base_date = datetime.datetime.now()
    
    sample_batches = [
        {
            "id": "33",
            "recipe_id": "1",
            "batch_name": "RECEPT BLACK CITRUS IPA (BJCP 21B) 50l",
            "batch_number": 33,
            "batch_size": 50.0,
            "brewer": "Asbjørn Bordoy",
            "status": "planning",
            "brew_date": (base_date + datetime.timedelta(days=3)).isoformat(),
            "created_at": (base_date - datetime.timedelta(days=1)).isoformat(),
            "updated_at": (base_date - datetime.timedelta(hours=2)).isoformat(),
            "notes": "Planning brew for next week. Need to check hop inventory.",
            "recipe": {
                "name": "Black Citrus IPA",
                "style": "BJCP 21B - Specialty IPA",
                "abv": 6.0,
                "ibu": 65,
                "og": 1.064,
                "fg": 1.018,
                "srm": 8.7
            }
        },
        {
            "id": "1",
            "recipe_id": "2", 
            "batch_name": "5 Yeast Experimental NEIPA",
            "batch_number": 1,
            "batch_size": 5.5,
            "brewer": "Asbjørn Bordoy",
            "status": "brewing",
            "brew_date": base_date.isoformat(),
            "created_at": (base_date - datetime.timedelta(days=7)).isoformat(),
            "updated_at": base_date.isoformat(),
            "og": 1.064,
            "notes": "Experimental batch with multiple yeast strains. Monitoring carefully.",
            "recipe": {
                "name": "5 Yeast Experimental NEIPA",
                "style": "New England IPA",
                "abv": 6.0,
                "ibu": 26,
                "og": 1.064,
                "fg": 1.018,
                "srm": 4.0
            }
        },
        {
            "id": "47",
            "recipe_id": "3",
            "batch_name": "Fermentation Batch #47",
            "batch_number": 47,
            "batch_size": 21.0,
            "brewer": "Asbjørn Bordoy", 
            "status": "fermenting",
            "brew_date": (base_date - datetime.timedelta(days=7)).isoformat(),
            "fermentation_start_date": (base_date - datetime.timedelta(days=6)).isoformat(),
            "created_at": (base_date - datetime.timedelta(days=10)).isoformat(),
            "updated_at": (base_date - datetime.timedelta(hours=1)).isoformat(),
            "og": 1.057,
            "fg": 1.031,
            "abv": 3.5,
            "notes": "Fermentation progressing well. SG dropping as expected.",
            "recipe": {
                "name": "American Pale Ale",
                "style": "American Pale Ale",
                "abv": 5.3,
                "ibu": 35,
                "og": 1.057,
                "fg": 1.012,
                "srm": 6.0
            }
        },
        {
            "id": "45",
            "recipe_id": "4",
            "batch_name": "Sample Blonde Ale", 
            "batch_number": 45,
            "batch_size": 23.0,
            "brewer": "Asbjørn Bordoy",
            "status": "conditioning",
            "brew_date": (base_date - datetime.timedelta(days=21)).isoformat(),
            "fermentation_start_date": (base_date - datetime.timedelta(days=20)).isoformat(),
            "conditioning_start_date": (base_date - datetime.timedelta(days=7)).isoformat(),
            "created_at": (base_date - datetime.timedelta(days=25)).isoformat(),
            "updated_at": (base_date - datetime.timedelta(days=7)).isoformat(),
            "og": 1.043,
            "fg": 1.009,
            "abv": 4.5,
            "notes": "Cold conditioning for clarity. Should be ready for packaging soon.",
            "recipe": {
                "name": "Sample Blonde Ale",
                "style": "Blonde Ale",
                "abv": 4.3,
                "ibu": 24,
                "og": 1.043,
                "fg": 1.009,
                "srm": 8.5
            }
        },
        {
            "id": "44",
            "recipe_id": "5",
            "batch_name": "Belgian Tripel Batch",
            "batch_number": 44,
            "batch_size": 20.0,
            "brewer": "Asbjørn Bordoy",
            "status": "packaging", 
            "brew_date": (base_date - datetime.timedelta(days=35)).isoformat(),
            "fermentation_start_date": (base_date - datetime.timedelta(days=34)).isoformat(),
            "packaging_date": (base_date - datetime.timedelta(days=5)).isoformat(),
            "created_at": (base_date - datetime.timedelta(days=40)).isoformat(),
            "updated_at": (base_date - datetime.timedelta(days=5)).isoformat(),
            "og": 1.085,
            "fg": 1.014,
            "abv": 9.5,
            "notes": "Packaged in bottles. Carbonating nicely. Should be ready in 2 weeks.",
            "recipe": {
                "name": "Belgian Tripel",
                "style": "26C Belgian Tripel", 
                "abv": 9.5,
                "ibu": 40,
                "og": 1.085,
                "fg": 1.014,
                "srm": 11.8
            }
        },
        {
            "id": "43",
            "recipe_id": "6",
            "batch_name": "Completed Stout Batch",
            "batch_number": 43,
            "batch_size": 19.0,
            "brewer": "Asbjørn Bordoy",
            "status": "complete",
            "brew_date": (base_date - datetime.timedelta(days=60)).isoformat(),
            "fermentation_start_date": (base_date - datetime.timedelta(days=59)).isoformat(),
            "packaging_date": (base_date - datetime.timedelta(days=30)).isoformat(),
            "completion_date": (base_date - datetime.timedelta(days=10)).isoformat(),
            "created_at": (base_date - datetime.timedelta(days=65)).isoformat(), 
            "updated_at": (base_date - datetime.timedelta(days=10)).isoformat(),
            "og": 1.072,
            "fg": 1.018,
            "abv": 7.1,
            "notes": "Excellent batch. Rich chocolate and coffee notes. Would brew again!",
            "recipe": {
                "name": "Imperial Stout",
                "style": "20C Imperial Stout",
                "abv": 7.1,
                "ibu": 60,
                "og": 1.072,
                "fg": 1.018,
                "srm": 40.0
            }
        }
    ]
    
    return sample_batches

def create_sample_readings() -> List[Dict[str, Any]]:
    """Create sample fermentation readings for active batches"""
    
    base_date = datetime.datetime.now()
    
    readings = [
        # Readings for Batch #47 (fermenting)
        {
            "id": "1",
            "batch_id": "47",
            "reading_date": (base_date - datetime.timedelta(days=6)).isoformat(),
            "gravity": 1.057,
            "temperature": 20.5,
            "ph": 5.2,
            "notes": "Fermentation started - pitched yeast"
        },
        {
            "id": "2", 
            "batch_id": "47",
            "reading_date": (base_date - datetime.timedelta(days=4)).isoformat(),
            "gravity": 1.045,
            "temperature": 21.1,
            "ph": 4.8,
            "notes": "Active fermentation - lots of foam"
        },
        {
            "id": "3",
            "batch_id": "47", 
            "reading_date": (base_date - datetime.timedelta(days=2)).isoformat(),
            "gravity": 1.038,
            "temperature": 21.0,
            "ph": 4.5,
            "notes": "Fermentation slowing down"
        },
        {
            "id": "4",
            "batch_id": "47",
            "reading_date": (base_date - datetime.timedelta(hours=12)).isoformat(),
            "gravity": 1.031,
            "temperature": 21.1,
            "ph": 4.2,
            "notes": "Current reading - fermentation nearly complete"
        }
    ]
    
    return readings

def create_sample_recipes() -> List[Dict[str, Any]]:
    """Create sample recipes to link with batches"""
    
    recipes = [
        {
            "id": "1",
            "name": "Black Citrus IPA",
            "style": "BJCP 21B - Specialty IPA",
            "type": "All Grain",
            "abv": 6.0,
            "ibu": 65,
            "og": 1.064,
            "fg": 1.018,
            "srm": 8.7,
            "efficiency": 70.0,
            "batch_size": 50.0,
            "boil_time": 60,
            "description": "Bold IPA with citrus hops and roasted malt complexity",
            "created_at": datetime.datetime.now().isoformat()
        },
        {
            "id": "2", 
            "name": "5 Yeast Experimental NEIPA",
            "style": "New England IPA",
            "type": "All Grain",
            "abv": 6.0,
            "ibu": 26,
            "og": 1.064,
            "fg": 1.018,
            "srm": 4.0,
            "efficiency": 70.0,
            "batch_size": 5.5,
            "boil_time": 60,
            "description": "Experimental NEIPA with multiple yeast strains",
            "created_at": datetime.datetime.now().isoformat()
        },
        {
            "id": "3",
            "name": "American Pale Ale", 
            "style": "American Pale Ale",
            "type": "All Grain",
            "abv": 5.3,
            "ibu": 35,
            "og": 1.057,
            "fg": 1.012,
            "srm": 6.0,
            "efficiency": 72.0,
            "batch_size": 21.0,
            "boil_time": 60,
            "description": "Classic American Pale Ale with Cascade hops",
            "created_at": datetime.datetime.now().isoformat()
        },
        {
            "id": "4",
            "name": "Sample Blonde Ale",
            "style": "Blonde Ale", 
            "type": "All Grain",
            "abv": 4.3,
            "ibu": 24,
            "og": 1.043,
            "fg": 1.009,
            "srm": 8.5,
            "efficiency": 75.0,
            "batch_size": 23.0,
            "boil_time": 60,
            "description": "Light, easy-drinking blonde ale perfect for summer",
            "created_at": datetime.datetime.now().isoformat()
        },
        {
            "id": "5",
            "name": "Belgian Tripel",
            "style": "26C Belgian Tripel",
            "type": "All Grain", 
            "abv": 9.5,
            "ibu": 40,
            "og": 1.085,
            "fg": 1.014,
            "srm": 11.8,
            "efficiency": 76.0,
            "batch_size": 20.0,
            "boil_time": 90,
            "description": "Traditional Belgian Tripel with complex esters and phenols",
            "created_at": datetime.datetime.now().isoformat()
        },
        {
            "id": "6",
            "name": "Imperial Stout",
            "style": "20C Imperial Stout",
            "type": "All Grain",
            "abv": 7.1,
            "ibu": 60,
            "og": 1.072,
            "fg": 1.018,
            "srm": 40.0,
            "efficiency": 72.0,
            "batch_size": 19.0,
            "boil_time": 60,
            "description": "Rich imperial stout with chocolate and coffee notes",
            "created_at": datetime.datetime.now().isoformat()
        }
    ]
    
    return recipes

def main():
    """Generate and save sample data"""
    
    print("🍺 Generating HoppyBrew Sample Data...")
    
    # Create sample data
    batches = create_sample_batches()
    readings = create_sample_readings()
    recipes = create_sample_recipes()
    
    # Save to JSON files
    data = {
        "batches": batches,
        "batch_readings": readings,
        "recipes": recipes,
        "generated_at": datetime.datetime.now().isoformat(),
        "description": "Sample data for HoppyBrew brewing workflow demonstration"
    }
    
    # Save complete dataset
    with open('sample_brewing_data.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    # Save individual files for easier import
    with open('sample_batches.json', 'w') as f:
        json.dump(batches, f, indent=2, default=str)
        
    with open('sample_readings.json', 'w') as f:
        json.dump(readings, f, indent=2, default=str)
        
    with open('sample_recipes.json', 'w') as f:
        json.dump(recipes, f, indent=2, default=str)
    
    print(f"✅ Generated {len(batches)} sample batches")
    print(f"✅ Generated {len(readings)} fermentation readings") 
    print(f"✅ Generated {len(recipes)} sample recipes")
    print("\nSample batch statuses:")
    
    for batch in batches:
        print(f"  - Batch #{batch['batch_number']}: {batch['batch_name']} ({batch['status']})")
    
    print("\n📁 Files created:")
    print("  - sample_brewing_data.json (complete dataset)")
    print("  - sample_batches.json")
    print("  - sample_readings.json") 
    print("  - sample_recipes.json")
    
    print("\n🚀 Ready to demonstrate brewing workflow phases!")

if __name__ == "__main__":
    main()
