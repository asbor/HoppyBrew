#!/usr/bin/env python3
"""Master seed script to populate the database with all sample data."""

from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "services" / "backend"))

from logger_config import get_logger
from database import SessionLocal, Base, engine

logger = get_logger("MasterSeed")


def run_all_seeds() -> None:
    """
    Run all seed scripts to populate the database with sample data.
    Creates database tables if they don't exist.
    """
    logger.info("Starting master seeding process")
    
    # Create all tables if they don't exist
    logger.info("Creating database tables if they don't exist")
    Base.metadata.create_all(bind=engine, checkfirst=True)
    
    session = SessionLocal()
    
    try:
        # Import seed functions
        from seed_references import seed_references
        from seed_beer_styles import seed_beer_styles
        from seed_sample_dataset import seed_sample_dataset
        from seed_fermentation_profiles import seed_fermentation_profiles
        
        # Run reference seeder
        logger.info("Seeding references...")
        ref_count = seed_references(session)
        logger.info(f"Seeded {ref_count} references")
        
        # Run beer styles seeder (if XML file exists)
        logger.info("Seeding beer styles...")
        try:
            style_count = seed_beer_styles()
            logger.info(f"Seeded {style_count} beer styles")
        except FileNotFoundError as e:
            logger.warning(f"Skipping beer styles seeding: {e}")

        # Run fermentation profiles seeder
        logger.info("Seeding fermentation profiles...")
        try:
            seed_fermentation_profiles()
            logger.info("Seeded fermentation profiles")
        except Exception as e:
            logger.warning(f"Error seeding fermentation profiles: {e}")

        # Populate showcase dataset
        logger.info("Seeding sample dataset...")
        sample_summary = seed_sample_dataset(session)
        logger.info("Sample dataset summary: %s", sample_summary)
        
        logger.info("Master seeding process completed successfully")
        
    except Exception as e:
        logger.error(f"Error during seeding: {e}")
        raise
    finally:
        session.close()


def main() -> None:
    """Main entry point for the master seed script."""
    run_all_seeds()


if __name__ == "__main__":
    main()
