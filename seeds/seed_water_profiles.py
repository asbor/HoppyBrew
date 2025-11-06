#!/usr/bin/env python3
"""Seed script to populate the database with default water profiles."""

from __future__ import annotations

import sys
from pathlib import Path
from decimal import Decimal

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "services" / "backend"))

from sqlalchemy.orm import Session
from database import SessionLocal
from Database.Models.Profiles.water_profiles import WaterProfiles
from logger_config import get_logger

logger = get_logger("SeedWaterProfiles")


# Source Water Profiles
SOURCE_PROFILES = [
    {
        "name": "Reverse Osmosis Water",
        "description": "Nearly pure water ideal for building custom water profiles from scratch",
        "profile_type": "source",
        "calcium": Decimal("1"),
        "magnesium": Decimal("0"),
        "sodium": Decimal("8"),
        "chloride": Decimal("4"),
        "sulfate": Decimal("1"),
        "bicarbonate": Decimal("16"),
        "ph": Decimal("7.0"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Distilled Water",
        "description": "Pure water with zero mineral content",
        "profile_type": "source",
        "calcium": Decimal("0"),
        "magnesium": Decimal("0"),
        "sodium": Decimal("0"),
        "chloride": Decimal("0"),
        "sulfate": Decimal("0"),
        "bicarbonate": Decimal("0"),
        "ph": Decimal("7.0"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "JANA Natural Mineral Water",
        "description": "Natural mineral water from Czech Republic, suitable for Czech Pilsner",
        "profile_type": "source",
        "calcium": Decimal("30"),
        "magnesium": Decimal("10"),
        "sodium": Decimal("5"),
        "chloride": Decimal("6"),
        "sulfate": Decimal("15"),
        "bicarbonate": Decimal("90"),
        "ph": Decimal("7.8"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Typical Tap Water",
        "description": "Average municipal tap water profile",
        "profile_type": "source",
        "calcium": Decimal("50"),
        "magnesium": Decimal("15"),
        "sodium": Decimal("20"),
        "chloride": Decimal("40"),
        "sulfate": Decimal("50"),
        "bicarbonate": Decimal("100"),
        "ph": Decimal("7.5"),
        "is_default": True,
        "is_custom": False,
    },
]

# Target Brewing Profiles
TARGET_PROFILES = [
    # Amber profiles
    {
        "name": "Amber Balanced",
        "description": "Balanced mineral profile for amber ales and general brewing",
        "profile_type": "target",
        "style_category": "Amber Ales",
        "calcium": Decimal("50"),
        "magnesium": Decimal("10"),
        "sodium": Decimal("15"),
        "chloride": Decimal("63"),
        "sulfate": Decimal("75"),
        "bicarbonate": Decimal("40"),
        "ph": Decimal("7.0"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Amber Dry",
        "description": "Higher sulfate profile for crisp, dry amber beers",
        "profile_type": "target",
        "style_category": "Amber Ales",
        "calcium": Decimal("75"),
        "magnesium": Decimal("15"),
        "sodium": Decimal("10"),
        "chloride": Decimal("50"),
        "sulfate": Decimal("150"),
        "bicarbonate": Decimal("50"),
        "ph": Decimal("7.2"),
        "is_default": True,
        "is_custom": False,
    },
    # Black/Dark profiles
    {
        "name": "Black Balanced",
        "description": "Balanced profile for porters and stouts",
        "profile_type": "target",
        "style_category": "Stout/Porter",
        "calcium": Decimal("100"),
        "magnesium": Decimal("10"),
        "sodium": Decimal("50"),
        "chloride": Decimal("100"),
        "sulfate": Decimal("100"),
        "bicarbonate": Decimal("300"),
        "ph": Decimal("8.0"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Black Full",
        "description": "Rich, full-bodied profile for imperial stouts",
        "profile_type": "target",
        "style_category": "Stout/Porter",
        "calcium": Decimal("120"),
        "magnesium": Decimal("15"),
        "sodium": Decimal("60"),
        "chloride": Decimal("150"),
        "sulfate": Decimal("120"),
        "bicarbonate": Decimal("350"),
        "ph": Decimal("8.2"),
        "is_default": True,
        "is_custom": False,
    },
    # Hoppy profiles
    {
        "name": "Hoppy",
        "description": "High sulfate profile for West Coast IPAs",
        "profile_type": "target",
        "style_category": "IPA",
        "calcium": Decimal("100"),
        "magnesium": Decimal("18"),
        "sodium": Decimal("16"),
        "chloride": Decimal("75"),
        "sulfate": Decimal("300"),
        "bicarbonate": Decimal("0"),
        "ph": Decimal("6.5"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Hoppy Lite",
        "description": "Moderate sulfate for session IPAs and pale ales",
        "profile_type": "target",
        "style_category": "IPA",
        "calcium": Decimal("75"),
        "magnesium": Decimal("10"),
        "sodium": Decimal("10"),
        "chloride": Decimal("50"),
        "sulfate": Decimal("150"),
        "bicarbonate": Decimal("0"),
        "ph": Decimal("6.8"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Hoppy NEIPA",
        "description": "Balanced chloride-forward profile for New England IPAs",
        "profile_type": "target",
        "style_category": "IPA",
        "calcium": Decimal("100"),
        "magnesium": Decimal("18"),
        "sodium": Decimal("16"),
        "chloride": Decimal("186"),
        "sulfate": Decimal("93"),
        "bicarbonate": Decimal("0"),
        "ph": Decimal("6.5"),
        "is_default": True,
        "is_custom": False,
    },
    # Malty profiles
    {
        "name": "Malty",
        "description": "Chloride-forward profile for malty, sweet beers",
        "profile_type": "target",
        "style_category": "Malty Ales",
        "calcium": Decimal("75"),
        "magnesium": Decimal("10"),
        "sodium": Decimal("25"),
        "chloride": Decimal("150"),
        "sulfate": Decimal("75"),
        "bicarbonate": Decimal("100"),
        "ph": Decimal("7.2"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Sweet",
        "description": "High chloride profile for sweet, full-bodied beers",
        "profile_type": "target",
        "style_category": "Malty Ales",
        "calcium": Decimal("100"),
        "magnesium": Decimal("15"),
        "sodium": Decimal("30"),
        "chloride": Decimal("200"),
        "sulfate": Decimal("50"),
        "bicarbonate": Decimal("150"),
        "ph": Decimal("7.5"),
        "is_default": True,
        "is_custom": False,
    },
    # Regional profiles
    {
        "name": "Burton-on-Trent",
        "description": "Classic English Burton water for IPAs and pale ales",
        "profile_type": "target",
        "style_category": "English Pale Ale",
        "calcium": Decimal("275"),
        "magnesium": Decimal("45"),
        "sodium": Decimal("25"),
        "chloride": Decimal("35"),
        "sulfate": Decimal("650"),
        "bicarbonate": Decimal("260"),
        "ph": Decimal("8.0"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Dublin",
        "description": "Traditional Irish water profile for stouts",
        "profile_type": "target",
        "style_category": "Stout/Porter",
        "calcium": Decimal("115"),
        "magnesium": Decimal("4"),
        "sodium": Decimal("12"),
        "chloride": Decimal("19"),
        "sulfate": Decimal("55"),
        "bicarbonate": Decimal("319"),
        "ph": Decimal("8.2"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Pilsen",
        "description": "Soft water profile for Czech Pilsners",
        "profile_type": "target",
        "style_category": "Pilsner",
        "calcium": Decimal("7"),
        "magnesium": Decimal("3"),
        "sodium": Decimal("2"),
        "chloride": Decimal("5"),
        "sulfate": Decimal("5"),
        "bicarbonate": Decimal("15"),
        "ph": Decimal("7.0"),
        "is_default": True,
        "is_custom": False,
    },
    {
        "name": "Vienna",
        "description": "Moderate carbonate water for Vienna lagers and märzens",
        "profile_type": "target",
        "style_category": "Lager",
        "calcium": Decimal("200"),
        "magnesium": Decimal("60"),
        "sodium": Decimal("8"),
        "chloride": Decimal("12"),
        "sulfate": Decimal("125"),
        "bicarbonate": Decimal("120"),
        "ph": Decimal("7.8"),
        "is_default": True,
        "is_custom": False,
    },
]


def seed_water_profiles(db: Session) -> None:
    """Seed the database with default water profiles."""
    
    logger.info("Starting water profiles seed...")
    
    # Clear existing default profiles
    db.query(WaterProfiles).filter(WaterProfiles.is_default == True).delete()
    
    # Add source profiles
    logger.info(f"Seeding {len(SOURCE_PROFILES)} source water profiles...")
    for profile_data in SOURCE_PROFILES:
        profile = WaterProfiles(**profile_data)
        db.add(profile)
    
    # Add target profiles
    logger.info(f"Seeding {len(TARGET_PROFILES)} target water profiles...")
    for profile_data in TARGET_PROFILES:
        profile = WaterProfiles(**profile_data)
        db.add(profile)
    
    db.commit()
    logger.info("Water profiles seeded successfully!")
    
    # Print summary
    source_count = db.query(WaterProfiles).filter(
        WaterProfiles.profile_type == "source",
        WaterProfiles.is_default == True
    ).count()
    target_count = db.query(WaterProfiles).filter(
        WaterProfiles.profile_type == "target",
        WaterProfiles.is_default == True
    ).count()
    
    logger.info(f"Total default profiles: {source_count} source, {target_count} target")


def main() -> None:
    """Main function to run the seed script."""
    logger.info("Connecting to database...")
    
    # Import and create tables
    from database import Base, engine
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine, checkfirst=True)
    
    db = SessionLocal()
    
    try:
        seed_water_profiles(db)
    except Exception as e:
        logger.error(f"Error seeding water profiles: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
