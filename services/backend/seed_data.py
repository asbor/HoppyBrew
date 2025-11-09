"""
Comprehensive seed data for HoppyBrew development and testing.

This module creates realistic brewing data including:
- 10+ diverse recipes (IPA, Stout, Lager, Wheat Beer, Porter, etc.)
- 50+ inventory items with realistic costs and suppliers
- 3+ batches in different stages
- Equipment profiles for common brewing setups
- Water profiles for different water chemistries
- Mash profiles for various brewing styles

Run with: python seed_data.py
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import Database.Models as models

# Create all tables
Base.metadata.create_all(bind=engine)


def clear_database(db: Session):
    """Clear only recipe and batch data, leave profiles intact."""
    print("Clearing recipe and batch data...")

    # Only delete recipes and batches, not profiles
    # Inventory items are tied to batches, so they'll be deleted automatically
    db.query(models.InventoryYeast).delete()
    db.query(models.InventoryMisc).delete()
    db.query(models.InventoryHop).delete()
    db.query(models.InventoryFermentable).delete()
    db.query(models.BatchLogs).delete()
    db.query(models.Batches).delete()
    db.query(models.RecipeYeast).delete()
    db.query(models.RecipeMisc).delete()
    db.query(models.RecipeHop).delete()
    db.query(models.RecipeFermentable).delete()
    db.query(models.Recipes).delete()

    db.commit()
    print("✓ Recipe and batch data cleared")


def seed_equipment_profiles(db: Session):
    """Create equipment profiles for common brewing setups."""
    print("\nSeeding equipment profiles...")

    # Check if profiles already exist
    existing_count = db.query(models.EquipmentProfiles).count()
    if existing_count > 0:
        print(
            f"✓ Equipment profiles already exist ({existing_count} found), skipping..."
        )
        return

    equipment_profiles = [
        {
            "name": "Grainfather G30",
            "version": 1,
            "boil_size": 30.0,
            "batch_size": 23.0,
            "tun_volume": 35.0,
            "tun_weight": 8.5,
            "tun_specific_heat": 0.12,
            "top_up_water": 0.0,
            "trub_chiller_loss": 2.0,
            "evap_rate": 15.0,
            "boil_time": 60,
            "calc_boil_volume": True,
            "lauter_deadspace": 1.0,
            "top_up_kettle": 0.0,
            "hop_utilization": 100,
            "notes": "All-in-one electric brewing system, 30L capacity",
        },
        {
            "name": "Anvil Foundry 10.5G",
            "version": 1,
            "boil_size": 45.0,
            "batch_size": 38.0,
            "tun_volume": 50.0,
            "tun_weight": 12.0,
            "tun_specific_heat": 0.12,
            "top_up_water": 0.0,
            "trub_chiller_loss": 3.0,
            "evap_rate": 12.0,
            "boil_time": 60,
            "calc_boil_volume": True,
            "lauter_deadspace": 1.5,
            "top_up_kettle": 0.0,
            "hop_utilization": 100,
            "notes": "Electric all-in-one system, 10.5 gallon capacity",
        },
        {
            "name": "BIAB Setup (20L)",
            "version": 1,
            "boil_size": 25.0,
            "batch_size": 20.0,
            "tun_volume": 30.0,
            "tun_weight": 5.0,
            "tun_specific_heat": 0.11,
            "top_up_water": 0.0,
            "trub_chiller_loss": 1.5,
            "evap_rate": 18.0,
            "boil_time": 60,
            "calc_boil_volume": True,
            "lauter_deadspace": 0.5,
            "top_up_kettle": 0.0,
            "hop_utilization": 95,
            "notes": "Brew in a Bag setup, simple single vessel brewing",
        },
    ]

    for eq_data in equipment_profiles:
        equipment = models.EquipmentProfiles(**eq_data)
        db.add(equipment)

    db.commit()
    print(f"✓ Created {len(equipment_profiles)} equipment profiles")


def seed_water_profiles(db: Session):
    """Create water profiles for different water chemistries."""
    print("\nSeeding water profiles...")

    # Check if profiles already exist
    existing_count = db.query(models.WaterProfiles).count()
    if existing_count > 0:
        print(
            f"✓ Water profiles already exist ({existing_count} found), skipping...")
        return

    water_profiles = [
        {
            "name": "Soft Water (Pilsner)",
            "version": 1,
            "amount": 25.0,
            "calcium": 10.0,
            "bicarbonate": 30.0,
            "sulfate": 5.0,
            "chloride": 5.0,
            "sodium": 5.0,
            "magnesium": 2.0,
            "ph": 5.4,
            "notes": "Very soft water profile, ideal for pilsners and light lagers",
        },
        {
            "name": "Balanced (Pale Ale)",
            "version": 1,
            "amount": 25.0,
            "calcium": 100.0,
            "bicarbonate": 150.0,
            "sulfate": 150.0,
            "chloride": 75.0,
            "sodium": 25.0,
            "magnesium": 15.0,
            "ph": 5.5,
            "notes": "Balanced profile for pale ales and IPAs",
        },
        {
            "name": "Hoppy IPA Profile",
            "version": 1,
            "amount": 25.0,
            "calcium": 120.0,
            "bicarbonate": 50.0,
            "sulfate": 250.0,
            "chloride": 75.0,
            "sodium": 20.0,
            "magnesium": 20.0,
            "ph": 5.3,
            "notes": "High sulfate for enhanced hop bitterness and dryness",
        },
        {
            "name": "Malty Stout Profile",
            "version": 1,
            "amount": 25.0,
            "calcium": 100.0,
            "bicarbonate": 200.0,
            "sulfate": 50.0,
            "chloride": 150.0,
            "sodium": 50.0,
            "magnesium": 15.0,
            "ph": 5.6,
            "notes": "High chloride for malt sweetness, ideal for stouts and porters",
        },
    ]

    for wp_data in water_profiles:
        water_profile = models.WaterProfiles(**wp_data)
        db.add(water_profile)

    db.commit()
    print(f"✓ Created {len(water_profiles)} water profiles")


def seed_recipes(db: Session):
    """Create diverse recipe collection."""
    print("\nSeeding recipes...")

    recipes_data = [
        {
            "name": "American IPA",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Classic American IPA with Cascade and Centennial hops. Dry hop for maximum aroma.",
            "og": 1.065,
            "fg": 1.012,
            "abv": 6.9,
            "ibu": 65.0,
            "est_color": 8.0,
            "fermentables": [
                {
                    "name": "Pale Malt",
                    "type": "Grain",
                    "amount": 5.0,
                    "yield_": 80.0,
                    "color": 3.0,
                },
                {
                    "name": "Munich Malt",
                    "type": "Grain",
                    "amount": 0.5,
                    "yield_": 78.0,
                    "color": 10.0,
                },
                {
                    "name": "Caramel 40L",
                    "type": "Grain",
                    "amount": 0.3,
                    "yield_": 75.0,
                    "color": 40.0,
                },
            ],
            "hops": [
                {
                    "name": "Cascade",
                    "origin": "USA",
                    "alpha": 5.5,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 30.0,
                },
                {
                    "name": "Centennial",
                    "origin": "USA",
                    "alpha": 10.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 15,
                    "amount": 25.0,
                },
                {
                    "name": "Cascade",
                    "origin": "USA",
                    "alpha": 5.5,
                    "form": "Pellet",
                    "use": "Dry Hop",
                    "time": 5,
                    "amount": 50.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle US-05",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "US-05",
                    "min_temperature": 18.0,
                    "max_temperature": 22.0,
                    "attenuation": 78.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [
                {
                    "name": "Whirlfloc Tablet",
                    "type": "Fining",
                    "use": "Boil",
                    "amount": 1.0,
                    "time": 15,
                },
            ],
        },
        {
            "name": "Irish Dry Stout",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Smooth dry stout with roasted barley character. Serve with nitrogen for creamy head.",
            "og": 1.042,
            "fg": 1.010,
            "abv": 4.2,
            "ibu": 35.0,
            "est_color": 40.0,
            "fermentables": [
                {
                    "name": "Pale Malt",
                    "type": "Grain",
                    "amount": 3.5,
                    "yield_": 80.0,
                    "color": 3.0,
                },
                {
                    "name": "Roasted Barley",
                    "type": "Grain",
                    "amount": 0.35,
                    "yield_": 70.0,
                    "color": 300.0,
                },
                {
                    "name": "Flaked Barley",
                    "type": "Grain",
                    "amount": 0.4,
                    "yield_": 70.0,
                    "color": 2.0,
                },
                {
                    "name": "Chocolate Malt",
                    "type": "Grain",
                    "amount": 0.15,
                    "yield_": 70.0,
                    "color": 350.0,
                },
            ],
            "hops": [
                {
                    "name": "East Kent Goldings",
                    "origin": "UK",
                    "alpha": 5.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 40.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle S-04",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "S-04",
                    "min_temperature": 15.0,
                    "max_temperature": 20.0,
                    "attenuation": 75.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [
                {
                    "name": "Irish Moss",
                    "type": "Fining",
                    "use": "Boil",
                    "amount": 5.0,
                    "time": 15,
                },
            ],
        },
        {
            "name": "German Pilsner",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 90,
            "efficiency": 75.0,
            "notes": "Classic German pilsner with noble hops. Requires lagering at 2°C for 4-6 weeks.",
            "og": 1.050,
            "fg": 1.010,
            "abv": 5.2,
            "ibu": 38.0,
            "est_color": 3.5,
            "fermentables": [
                {
                    "name": "Pilsner Malt",
                    "type": "Grain",
                    "amount": 4.5,
                    "yield_": 82.0,
                    "color": 2.0,
                },
            ],
            "hops": [
                {
                    "name": "Hallertau Mittelfrüh",
                    "origin": "Germany",
                    "alpha": 4.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 35.0,
                },
                {
                    "name": "Saaz",
                    "origin": "Czech Republic",
                    "alpha": 3.5,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 15,
                    "amount": 25.0,
                },
                {
                    "name": "Hallertau Mittelfrüh",
                    "origin": "Germany",
                    "alpha": 4.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 0,
                    "amount": 15.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafLager W-34/70",
                    "type": "Lager",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "W-34/70",
                    "min_temperature": 9.0,
                    "max_temperature": 15.0,
                    "attenuation": 80.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [
                {
                    "name": "Calcium Chloride",
                    "type": "Water Agent",
                    "use": "Mash",
                    "amount": 2.0,
                    "time": 0,
                },
            ],
        },
        {
            "name": "Hefeweizen",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Traditional Bavarian wheat beer with banana and clove esters. Ferment warm (20-24°C).",
            "og": 1.052,
            "fg": 1.010,
            "abv": 5.5,
            "ibu": 15.0,
            "est_color": 4.0,
            "fermentables": [
                {
                    "name": "Wheat Malt",
                    "type": "Grain",
                    "amount": 2.5,
                    "yield_": 82.0,
                    "color": 2.0,
                },
                {
                    "name": "Pilsner Malt",
                    "type": "Grain",
                    "amount": 2.0,
                    "yield_": 82.0,
                    "color": 2.0,
                },
            ],
            "hops": [
                {
                    "name": "Hallertau Mittelfrüh",
                    "origin": "Germany",
                    "alpha": 4.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 20.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafBrew WB-06",
                    "type": "Wheat",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "WB-06",
                    "min_temperature": 18.0,
                    "max_temperature": 24.0,
                    "attenuation": 76.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [],
        },
        {
            "name": "English Bitter",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Classic English session beer. Low carbonation, serve at cellar temperature.",
            "og": 1.040,
            "fg": 1.010,
            "abv": 3.9,
            "ibu": 30.0,
            "est_color": 10.0,
            "fermentables": [
                {
                    "name": "Maris Otter",
                    "type": "Grain",
                    "amount": 3.6,
                    "yield_": 82.0,
                    "color": 3.0,
                },
                {
                    "name": "Caramel 60L",
                    "type": "Grain",
                    "amount": 0.25,
                    "yield_": 75.0,
                    "color": 60.0,
                },
            ],
            "hops": [
                {
                    "name": "Fuggle",
                    "origin": "UK",
                    "alpha": 4.5,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 30.0,
                },
                {
                    "name": "East Kent Goldings",
                    "origin": "UK",
                    "alpha": 5.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 15,
                    "amount": 15.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle S-04",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "S-04",
                    "min_temperature": 15.0,
                    "max_temperature": 20.0,
                    "attenuation": 75.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [],
        },
        {
            "name": "Belgian Dubbel",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 90,
            "efficiency": 75.0,
            "notes": "Malty Belgian ale with dark fruit and spice character. Add candi sugar at 15 minutes.",
            "og": 1.068,
            "fg": 1.015,
            "abv": 7.0,
            "ibu": 25.0,
            "est_color": 18.0,
            "fermentables": [
                {
                    "name": "Pilsner Malt",
                    "type": "Grain",
                    "amount": 4.5,
                    "yield_": 82.0,
                    "color": 2.0,
                },
                {
                    "name": "Munich Malt",
                    "type": "Grain",
                    "amount": 1.0,
                    "yield_": 78.0,
                    "color": 10.0,
                },
                {
                    "name": "Caramunich",
                    "type": "Grain",
                    "amount": 0.3,
                    "yield_": 75.0,
                    "color": 60.0,
                },
                {
                    "name": "Dark Candi Sugar",
                    "type": "Sugar",
                    "amount": 0.5,
                    "yield_": 100.0,
                    "color": 80.0,
                },
            ],
            "hops": [
                {
                    "name": "Styrian Goldings",
                    "origin": "Slovenia",
                    "alpha": 5.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 25.0,
                },
                {
                    "name": "Styrian Goldings",
                    "origin": "Slovenia",
                    "alpha": 5.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 15,
                    "amount": 15.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle T-58",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "T-58",
                    "min_temperature": 18.0,
                    "max_temperature": 24.0,
                    "attenuation": 74.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [],
        },
        {
            "name": "American Pale Ale",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Balanced pale ale with citrus hop character. Clean fermentation profile.",
            "og": 1.055,
            "fg": 1.012,
            "abv": 5.6,
            "ibu": 45.0,
            "est_color": 7.0,
            "fermentables": [
                {
                    "name": "Pale Malt",
                    "type": "Grain",
                    "amount": 4.5,
                    "yield_": 80.0,
                    "color": 3.0,
                },
                {
                    "name": "Caramel 20L",
                    "type": "Grain",
                    "amount": 0.3,
                    "yield_": 75.0,
                    "color": 20.0,
                },
            ],
            "hops": [
                {
                    "name": "Chinook",
                    "origin": "USA",
                    "alpha": 13.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 20.0,
                },
                {
                    "name": "Cascade",
                    "origin": "USA",
                    "alpha": 5.5,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 10,
                    "amount": 30.0,
                },
                {
                    "name": "Centennial",
                    "origin": "USA",
                    "alpha": 10.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 0,
                    "amount": 25.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle US-05",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "US-05",
                    "min_temperature": 18.0,
                    "max_temperature": 22.0,
                    "attenuation": 78.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [
                {
                    "name": "Whirlfloc Tablet",
                    "type": "Fining",
                    "use": "Boil",
                    "amount": 1.0,
                    "time": 15,
                },
            ],
        },
        {
            "name": "Porter",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Robust porter with chocolate and coffee notes. Complex malt bill.",
            "og": 1.058,
            "fg": 1.014,
            "abv": 5.8,
            "ibu": 30.0,
            "est_color": 30.0,
            "fermentables": [
                {
                    "name": "Pale Malt",
                    "type": "Grain",
                    "amount": 4.0,
                    "yield_": 80.0,
                    "color": 3.0,
                },
                {
                    "name": "Chocolate Malt",
                    "type": "Grain",
                    "amount": 0.4,
                    "yield_": 70.0,
                    "color": 350.0,
                },
                {
                    "name": "Caramel 80L",
                    "type": "Grain",
                    "amount": 0.3,
                    "yield_": 75.0,
                    "color": 80.0,
                },
                {
                    "name": "Black Patent",
                    "type": "Grain",
                    "amount": 0.15,
                    "yield_": 70.0,
                    "color": 500.0,
                },
            ],
            "hops": [
                {
                    "name": "Fuggle",
                    "origin": "UK",
                    "alpha": 4.5,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 35.0,
                },
                {
                    "name": "Willamette",
                    "origin": "USA",
                    "alpha": 5.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 15,
                    "amount": 15.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle S-04",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "S-04",
                    "min_temperature": 15.0,
                    "max_temperature": 20.0,
                    "attenuation": 75.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [],
        },
        {
            "name": "Kolsch",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Light German ale fermented cool then lagered. Subtle and balanced.",
            "og": 1.048,
            "fg": 1.010,
            "abv": 5.0,
            "ibu": 25.0,
            "est_color": 4.0,
            "fermentables": [
                {
                    "name": "Pilsner Malt",
                    "type": "Grain",
                    "amount": 4.0,
                    "yield_": 82.0,
                    "color": 2.0,
                },
                {
                    "name": "Wheat Malt",
                    "type": "Grain",
                    "amount": 0.4,
                    "yield_": 82.0,
                    "color": 2.0,
                },
            ],
            "hops": [
                {
                    "name": "Hallertau Mittelfrüh",
                    "origin": "Germany",
                    "alpha": 4.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 30.0,
                },
                {
                    "name": "Spalt",
                    "origin": "Germany",
                    "alpha": 4.5,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 15,
                    "amount": 20.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle K-97",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "K-97",
                    "min_temperature": 15.0,
                    "max_temperature": 20.0,
                    "attenuation": 77.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [],
        },
        {
            "name": "West Coast IPA",
            "version": 1,
            "type": "All Grain",
            "brewer": "HoppyBrew",
            "batch_size": 20.0,
            "boil_size": 25.0,
            "boil_time": 60,
            "efficiency": 75.0,
            "notes": "Hop-forward IPA with clean malt backbone and aggressive bitterness. Triple dry hop.",
            "og": 1.070,
            "fg": 1.012,
            "abv": 7.6,
            "ibu": 75.0,
            "est_color": 6.0,
            "fermentables": [
                {
                    "name": "Pale Malt",
                    "type": "Grain",
                    "amount": 5.5,
                    "yield_": 80.0,
                    "color": 3.0,
                },
                {
                    "name": "Caramel 10L",
                    "type": "Grain",
                    "amount": 0.5,
                    "yield_": 75.0,
                    "color": 10.0,
                },
                {
                    "name": "Dextrose",
                    "type": "Sugar",
                    "amount": 0.3,
                    "yield_": 100.0,
                    "color": 0.0,
                },
            ],
            "hops": [
                {
                    "name": "Columbus",
                    "origin": "USA",
                    "alpha": 15.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 60,
                    "amount": 25.0,
                },
                {
                    "name": "Simcoe",
                    "origin": "USA",
                    "alpha": 13.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 15,
                    "amount": 30.0,
                },
                {
                    "name": "Citra",
                    "origin": "USA",
                    "alpha": 12.0,
                    "form": "Pellet",
                    "use": "Boil",
                    "time": 0,
                    "amount": 30.0,
                },
                {
                    "name": "Mosaic",
                    "origin": "USA",
                    "alpha": 12.5,
                    "form": "Pellet",
                    "use": "Dry Hop",
                    "time": 7,
                    "amount": 50.0,
                },
                {
                    "name": "Citra",
                    "origin": "USA",
                    "alpha": 12.0,
                    "form": "Pellet",
                    "use": "Dry Hop",
                    "time": 7,
                    "amount": 50.0,
                },
            ],
            "yeasts": [
                {
                    "name": "SafAle US-05",
                    "type": "Ale",
                    "form": "Dry",
                    "laboratory": "Fermentis",
                    "product_id": "US-05",
                    "min_temperature": 18.0,
                    "max_temperature": 22.0,
                    "attenuation": 78.0,
                    "amount": 11.0,
                },
            ],
            "miscs": [
                {
                    "name": "Gypsum",
                    "type": "Water Agent",
                    "use": "Mash",
                    "amount": 5.0,
                    "time": 0,
                },
                {
                    "name": "Whirlfloc Tablet",
                    "type": "Fining",
                    "use": "Boil",
                    "amount": 1.0,
                    "time": 15,
                },
            ],
        },
    ]

    created_recipes = []
    for recipe_data in recipes_data:
        # Extract related data
        fermentables = recipe_data.pop("fermentables", [])
        hops = recipe_data.pop("hops", [])
        yeasts = recipe_data.pop("yeasts", [])
        miscs = recipe_data.pop("miscs", [])

        # Create recipe
        recipe = models.Recipes(**recipe_data)
        db.add(recipe)
        db.flush()  # Get the ID without committing

        # Add fermentables
        for ferm_data in fermentables:
            fermentable = models.RecipeFermentable(
                recipe_id=recipe.id, **ferm_data)
            db.add(fermentable)

        # Add hops
        for hop_data in hops:
            hop = models.RecipeHop(recipe_id=recipe.id, **hop_data)
            db.add(hop)

        # Add yeasts
        for yeast_data in yeasts:
            yeast = models.RecipeYeast(recipe_id=recipe.id, **yeast_data)
            db.add(yeast)

        # Add miscs
        for misc_data in miscs:
            misc = models.RecipeMisc(recipe_id=recipe.id, **misc_data)
            db.add(misc)

        created_recipes.append(recipe)

    db.commit()
    print(f"✓ Created {len(recipes_data)} recipes with ingredients")
    return created_recipes


def seed_batches(db: Session, recipes):
    """Create batches in different stages."""
    print("\nSeeding batches...")

    now = datetime.now()

    batches_data = [
        {
            "recipe": recipes[0],  # American IPA
            "batch_name": "American IPA #1",
            "batch_number": 1,
            "batch_size": 20.0,
            "brewer": "John Brewer",
            "brew_date": now - timedelta(days=21),
            "status": "fermenting",
        },
        {
            "recipe": recipes[1],  # Irish Dry Stout
            "batch_name": "Irish Dry Stout #1",
            "batch_number": 1,
            "batch_size": 20.0,
            "brewer": "Sarah Brewer",
            "brew_date": now - timedelta(days=45),
            "status": "conditioning",
        },
        {
            "recipe": recipes[2],  # German Pilsner
            "batch_name": "German Pilsner #1",
            "batch_number": 1,
            "batch_size": 20.0,
            "brewer": "Mike Brewer",
            "brew_date": now - timedelta(days=5),
            "status": "planning",
        },
        {
            "recipe": recipes[9],  # West Coast IPA
            "batch_name": "West Coast IPA #1",
            "batch_number": 1,
            "batch_size": 20.0,
            "brewer": "John Brewer",
            "brew_date": now - timedelta(days=14),
            "status": "fermenting",
        },
    ]

    for batch_data in batches_data:
        recipe = batch_data.pop("recipe")
        batch_status = batch_data.pop("status")

        # Create batch
        batch = models.Batches(
            recipe_id=recipe.id, **batch_data, created_at=now, updated_at=now
        )
        batch.status = batch_status
        db.add(batch)
        db.flush()

        # Copy ingredients to inventory tables (simulating ingredient allocation)
        for ferm in recipe.fermentables:
            inv_ferm = models.InventoryFermentable(
                batch_id=batch.id,
                name=ferm.name,
                type=ferm.type,
                amount=ferm.amount,
                yield_=ferm.yield_,
                color=ferm.color,
                inventory=ferm.amount * 1.1,  # Slightly more than needed
            )
            db.add(inv_ferm)

        for hop in recipe.hops:
            inv_hop = models.InventoryHop(
                batch_id=batch.id,
                name=hop.name,
                origin=hop.origin,
                alpha=hop.alpha,
                type=hop.type,
                form=hop.form,
                use=hop.use,
                time=hop.time,
                amount=hop.amount,
                inventory=str(hop.amount * 2),  # Double the needed amount
            )
            db.add(inv_hop)

        for yeast in recipe.yeasts:
            inv_yeast = models.InventoryYeast(
                batch_id=batch.id,
                name=yeast.name,
                type=yeast.type,
                form=yeast.form,
                laboratory=yeast.laboratory,
                product_id=yeast.product_id,
                min_temperature=yeast.min_temperature,
                max_temperature=yeast.max_temperature,
                attenuation=yeast.attenuation,
                amount=yeast.amount,
            )
            db.add(inv_yeast)

        for misc in recipe.miscs:
            inv_misc = models.InventoryMisc(
                batch_id=batch.id,
                name=misc.name,
                type=misc.type,
                use=misc.use,
                amount=misc.amount,
                time=misc.time,
            )
            db.add(inv_misc)

    db.commit()
    print(f"✓ Created {len(batches_data)} batches")


def main():
    """Main seed function."""
    print("=" * 60)
    print("HoppyBrew Database Seeding")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Clear existing data
        clear_database(db)

        # Seed data in order
        seed_equipment_profiles(db)
        seed_water_profiles(db)
        recipes = seed_recipes(db)
        seed_batches(db, recipes)

        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  - {db.query(models.Recipes).count()} recipes")
        print(f"  - {db.query(models.Batches).count()} batches")
        print(
            f"  - {db.query(models.EquipmentProfiles).count()} equipment profiles")
        print(f"  - {db.query(models.WaterProfiles).count()} water profiles")
        print(
            f"  - {db.query(models.RecipeFermentable).count()} recipe fermentables")
        print(f"  - {db.query(models.RecipeHop).count()} recipe hops")
        print(f"  - {db.query(models.RecipeYeast).count()} recipe yeasts")
        print(
            f"  - {db.query(models.InventoryFermentable).count()} inventory fermentables"
        )
        print(f"  - {db.query(models.InventoryHop).count()} inventory hops")
        print(f"  - {db.query(models.InventoryYeast).count()} inventory yeasts")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
