"""
Seed data for common yeast strains.

This script populates the yeast_strains table with commonly used brewing yeast strains.
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any

# Common yeast strains data
YEAST_STRAINS_DATA: List[Dict[str, Any]] = [
    # Fermentis Dry Yeasts
    {
        "name": "SafAle US-05",
        "laboratory": "Fermentis",
        "product_id": "US-05",
        "type": "Ale",
        "form": "Dry",
        "min_temperature": 15.0,
        "max_temperature": 24.0,
        "flocculation": "Medium",
        "attenuation_min": 78.0,
        "attenuation_max": 82.0,
        "alcohol_tolerance": 12.0,
        "best_for": "American ales, especially Pale Ales and IPAs",
        "notes": "Clean fermenting American ale yeast with neutral profile. Very popular for homebrewing.",
        "max_reuse": 5,
        "viability_days_dry": 1095
    },
    {
        "name": "SafAle S-04",
        "laboratory": "Fermentis",
        "product_id": "S-04",
        "type": "Ale",
        "form": "Dry",
        "min_temperature": 15.0,
        "max_temperature": 24.0,
        "flocculation": "High",
        "attenuation_min": 75.0,
        "attenuation_max": 79.0,
        "alcohol_tolerance": 11.0,
        "best_for": "English ales, especially bitters and porters",
        "notes": "English ale yeast providing a fast, clean fermentation with subtle fruity notes.",
        "max_reuse": 5,
        "viability_days_dry": 1095
    },
    {
        "name": "SafLager W-34/70",
        "laboratory": "Fermentis",
        "product_id": "W-34/70",
        "type": "Lager",
        "form": "Dry",
        "min_temperature": 9.0,
        "max_temperature": 15.0,
        "flocculation": "High",
        "attenuation_min": 80.0,
        "attenuation_max": 84.0,
        "alcohol_tolerance": 10.0,
        "best_for": "German lagers, pilsners, and continental beers",
        "notes": "Famous German lager strain producing clean, crisp beers.",
        "max_reuse": 5,
        "viability_days_dry": 1095
    },
    {
        "name": "SafAle K-97",
        "laboratory": "Fermentis",
        "product_id": "K-97",
        "type": "Ale",
        "form": "Dry",
        "min_temperature": 15.0,
        "max_temperature": 25.0,
        "flocculation": "High",
        "attenuation_min": 78.0,
        "attenuation_max": 82.0,
        "alcohol_tolerance": 12.0,
        "best_for": "German wheat beers and altbiers",
        "notes": "German ale yeast producing subtle fruity esters.",
        "max_reuse": 5,
        "viability_days_dry": 1095
    },

    # White Labs Liquid Yeasts
    {
        "name": "California Ale",
        "laboratory": "White Labs",
        "product_id": "WLP001",
        "type": "Ale",
        "form": "Liquid",
        "min_temperature": 18.0,
        "max_temperature": 22.0,
        "flocculation": "Medium",
        "attenuation_min": 73.0,
        "attenuation_max": 77.0,
        "alcohol_tolerance": 10.0,
        "best_for": "American ales and lagers",
        "notes": "Clean fermenting strain, very versatile.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },
    {
        "name": "English Ale",
        "laboratory": "White Labs",
        "product_id": "WLP002",
        "type": "Ale",
        "form": "Liquid",
        "min_temperature": 18.0,
        "max_temperature": 20.0,
        "flocculation": "Very High",
        "attenuation_min": 63.0,
        "attenuation_max": 70.0,
        "alcohol_tolerance": 10.0,
        "best_for": "English ales, especially ESB and bitters",
        "notes": "Classic British strain with malty character.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },
    {
        "name": "German Lager",
        "laboratory": "White Labs",
        "product_id": "WLP830",
        "type": "Lager",
        "form": "Liquid",
        "min_temperature": 10.0,
        "max_temperature": 13.0,
        "flocculation": "Medium",
        "attenuation_min": 74.0,
        "attenuation_max": 79.0,
        "alcohol_tolerance": 9.0,
        "best_for": "German lagers and pilsners",
        "notes": "Produces clean, malty German lagers.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },
    {
        "name": "Belgian Wit",
        "laboratory": "White Labs",
        "product_id": "WLP400",
        "type": "Ale",
        "form": "Liquid",
        "min_temperature": 18.0,
        "max_temperature": 23.0,
        "flocculation": "Medium",
        "attenuation_min": 74.0,
        "attenuation_max": 78.0,
        "alcohol_tolerance": 10.0,
        "best_for": "Belgian wit beers and spiced ales",
        "notes": "Slightly phenolic with mild fruitiness.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },

    # Wyeast Liquid Yeasts
    {
        "name": "American Ale",
        "laboratory": "Wyeast",
        "product_id": "1056",
        "type": "Ale",
        "form": "Liquid",
        "min_temperature": 16.0,
        "max_temperature": 22.0,
        "flocculation": "Low to Medium",
        "attenuation_min": 73.0,
        "attenuation_max": 77.0,
        "alcohol_tolerance": 11.0,
        "best_for": "American ales and lagers",
        "notes": "Very clean, crisp flavor, very versatile.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },
    {
        "name": "London ESB Ale",
        "laboratory": "Wyeast",
        "product_id": "1968",
        "type": "Ale",
        "form": "Liquid",
        "min_temperature": 18.0,
        "max_temperature": 22.0,
        "flocculation": "Very High",
        "attenuation_min": 67.0,
        "attenuation_max": 71.0,
        "alcohol_tolerance": 10.0,
        "best_for": "English ales, especially ESB and bitters",
        "notes": "Rich, malty profile with balanced fruitiness.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },
    {
        "name": "German Ale/Kölsch",
        "laboratory": "Wyeast",
        "product_id": "2565",
        "type": "Ale",
        "form": "Liquid",
        "min_temperature": 13.0,
        "max_temperature": 20.0,
        "flocculation": "Low",
        "attenuation_min": 73.0,
        "attenuation_max": 77.0,
        "alcohol_tolerance": 10.0,
        "best_for": "Kölsch and continental ales",
        "notes": "Produces a crisp, dry beer with subdued fruitiness.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },
    {
        "name": "Belgian Witbier",
        "laboratory": "Wyeast",
        "product_id": "3944",
        "type": "Ale",
        "form": "Liquid",
        "min_temperature": 17.0,
        "max_temperature": 22.0,
        "flocculation": "Medium",
        "attenuation_min": 72.0,
        "attenuation_max": 76.0,
        "alcohol_tolerance": 10.0,
        "best_for": "Belgian wit and wheat beers",
        "notes": "Mild phenolic and ester production.",
        "max_reuse": 5,
        "viability_days_liquid": 180
    },
]


def seed_yeast_strains(db: Session) -> int:
    """
    Seed the database with common yeast strains.

    Args:
        db: Database session

    Returns:
        Number of strains added
    """
    from Database.Models import YeastStrain

    added_count = 0

    for strain_data in YEAST_STRAINS_DATA:
        # Check if strain already exists
        existing = db.query(YeastStrain).filter(
            YeastStrain.laboratory == strain_data["laboratory"],
            YeastStrain.product_id == strain_data["product_id"]
        ).first()

        if existing:
            # Update existing strain
            for key, value in strain_data.items():
                setattr(existing, key, value)
            print(f"Updated yeast strain: {strain_data['laboratory']} {strain_data['product_id']}")
        else:
            # Create new strain
            strain = YeastStrain(**strain_data)
            db.add(strain)
            added_count += 1
            print(f"Added yeast strain: {strain_data['laboratory']} {strain_data['product_id']}")

    try:
        db.commit()
        print(f"\nSuccessfully seeded {added_count} new yeast strains")
        return added_count
    except Exception as e:
        db.rollback()
        print(f"Error seeding yeast strains: {e}")
        raise


if __name__ == "__main__":
    """Run this script to seed yeast strains"""
    from database import SessionLocal

    print("Seeding yeast strains...")
    db = SessionLocal()
    try:
        count = seed_yeast_strains(db)
        print(f"Completed! Added {count} yeast strains to the database.")
    finally:
        db.close()
