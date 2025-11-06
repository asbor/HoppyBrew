#!/usr/bin/env python3
"""Seed script to populate the database with sample reference data."""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "services" / "backend"))

from sqlalchemy.orm import Session
from database import SessionLocal
from Database.Models.references import References
from logger_config import get_logger

logger = get_logger("SeedReferences")


SAMPLE_REFERENCES = [
    {
        "name": "Brewfather",
        "url": "https://brewfather.app",
        "description": "Comprehensive brewing software for planning and managing your homebrewing",
        "category": "Software",
        "favicon_url": "https://brewfather.app/favicon.ico",
    },
    {
        "name": "BJCP Style Guidelines",
        "url": "https://www.bjcp.org/style/2021/beer/",
        "description": "Beer Judge Certification Program 2021 Style Guidelines",
        "category": "Style Guide",
        "favicon_url": None,
    },
    {
        "name": "How to Brew by John Palmer",
        "url": "http://www.howtobrew.com/",
        "description": "The definitive guide to making beer at home",
        "category": "Education",
        "favicon_url": None,
    },
    {
        "name": "Brewer's Friend",
        "url": "https://www.brewersfriend.com/",
        "description": "Brewing calculators and recipe design tools",
        "category": "Tools",
        "favicon_url": None,
    },
    {
        "name": "HomebrewTalk",
        "url": "https://www.homebrewtalk.com/",
        "description": "Community forum for homebrewing discussions",
        "category": "Community",
        "favicon_url": None,
    },
    {
        "name": "r/Homebrewing",
        "url": "https://www.reddit.com/r/Homebrewing/",
        "description": "Reddit community for homebrewers",
        "category": "Community",
        "favicon_url": None,
    },
    {
        "name": "Beersmith",
        "url": "https://beersmith.com/",
        "description": "Recipe design and brewing software",
        "category": "Software",
        "favicon_url": None,
    },
    {
        "name": "The Mad Fermentationist",
        "url": "https://www.themadfermentationist.com/",
        "description": "Blog about homebrewing and professional brewing",
        "category": "Blog",
        "favicon_url": None,
    },
]


def seed_references(session: Session | None = None) -> int:
    """
    Seed the database with sample reference data.
    
    Args:
        session: Optional SQLAlchemy session (creates one if not provided)
        
    Returns:
        Number of references created or updated
    """
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True
    
    try:
        count = 0
        for ref_data in SAMPLE_REFERENCES:
            # Check if reference already exists
            existing = (
                session.query(References)
                .filter(References.url == ref_data["url"])
                .first()
            )
            
            if existing:
                # Update existing reference
                for key, value in ref_data.items():
                    if value is not None:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
                logger.info(f"Updated reference: {ref_data['name']}")
            else:
                # Create new reference
                reference = References(
                    name=ref_data["name"],
                    url=ref_data["url"],
                    description=ref_data.get("description"),
                    category=ref_data.get("category"),
                    favicon_url=ref_data.get("favicon_url"),
                    created_at=datetime.now(),
                )
                session.add(reference)
                logger.info(f"Created reference: {ref_data['name']}")
            count += 1
        
        session.commit()
        logger.info(f"Seeded {count} references")
        return count
    
    except Exception as e:
        logger.error(f"Error seeding references: {e}")
        session.rollback()
        raise
    finally:
        if close_session:
            session.close()


def main() -> None:
    """Main entry point for the seed script."""
    logger.info("Starting reference seeding process")
    count = seed_references()
    logger.info(f"Successfully seeded {count} references")


if __name__ == "__main__":
    main()
