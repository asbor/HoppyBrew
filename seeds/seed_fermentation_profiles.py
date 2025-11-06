"""
Seed script for fermentation profiles

Adds template fermentation profiles for common beer styles.
"""

import sys
import os

# Add parent directory to path to import Database modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from Database.Models import FermentationProfiles, FermentationSteps


def seed_fermentation_profiles():
    """Seed the database with example fermentation profiles"""
    db = SessionLocal()

    try:
        # Check if profiles already exist
        existing = (
            db.query(FermentationProfiles)
            .filter(FermentationProfiles.is_template == True)
            .count()
        )

        if existing > 0:
            print(f"Found {existing} existing template profiles. Skipping seed.")
            return

        # Standard Ale Profile
        ale_profile = FermentationProfiles(
            name="Standard Ale",
            description="Basic ale fermentation profile with primary and conditioning phases",
            is_pressurized=False,
            is_template=True,
        )
        db.add(ale_profile)
        db.flush()

        ale_steps = [
            FermentationSteps(
                fermentation_profile_id=ale_profile.id,
                step_order=1,
                name="Primary Fermentation",
                step_type="primary",
                temperature=20,
                duration_days=7,
                ramp_days=0,
                notes="Primary fermentation at 20°C",
            ),
            FermentationSteps(
                fermentation_profile_id=ale_profile.id,
                step_order=2,
                name="Conditioning",
                step_type="conditioning",
                temperature=18,
                duration_days=7,
                ramp_days=1,
                notes="Conditioning phase with gradual temperature ramp",
            ),
        ]
        for step in ale_steps:
            db.add(step)

        # Lager Profile
        lager_profile = FermentationProfiles(
            name="Lager",
            description="Traditional lager fermentation profile with lagering phase",
            is_pressurized=False,
            is_template=True,
        )
        db.add(lager_profile)
        db.flush()

        lager_steps = [
            FermentationSteps(
                fermentation_profile_id=lager_profile.id,
                step_order=1,
                name="Primary Fermentation",
                step_type="primary",
                temperature=10,
                duration_days=14,
                ramp_days=0,
            ),
            FermentationSteps(
                fermentation_profile_id=lager_profile.id,
                step_order=2,
                name="Diacetyl Rest",
                step_type="diacetyl_rest",
                temperature=18,
                duration_days=2,
                ramp_days=1,
            ),
            FermentationSteps(
                fermentation_profile_id=lager_profile.id,
                step_order=3,
                name="Lagering",
                step_type="lagering",
                temperature=2,
                duration_days=28,
                ramp_days=2,
            ),
        ]
        for step in lager_steps:
            db.add(step)

        # NEIPA Profile
        neipa_profile = FermentationProfiles(
            name="NEIPA",
            description="New England IPA fermentation profile with cold crash",
            is_pressurized=False,
            is_template=True,
        )
        db.add(neipa_profile)
        db.flush()

        neipa_steps = [
            FermentationSteps(
                fermentation_profile_id=neipa_profile.id,
                step_order=1,
                name="Primary Fermentation",
                step_type="primary",
                temperature=19,
                duration_days=4,
                ramp_days=0,
            ),
            FermentationSteps(
                fermentation_profile_id=neipa_profile.id,
                step_order=2,
                name="Dry Hop Conditioning",
                step_type="conditioning",
                temperature=21,
                duration_days=3,
                ramp_days=0,
            ),
            FermentationSteps(
                fermentation_profile_id=neipa_profile.id,
                step_order=3,
                name="Cold Crash",
                step_type="cold_crash",
                temperature=4,
                duration_days=2,
                ramp_days=1,
            ),
        ]
        for step in neipa_steps:
            db.add(step)

        # Commit all changes
        db.commit()
        print("Successfully seeded fermentation profiles:")
        print("  - Standard Ale (2 steps)")
        print("  - Lager (3 steps)")
        print("  - NEIPA (3 steps)")

    except Exception as e:
        db.rollback()
        print(f"Error seeding fermentation profiles: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_fermentation_profiles()
