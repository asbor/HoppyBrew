#!/usr/bin/env python3
"""
Fix invalid batch statuses in the database.
Converts any invalid statuses to valid BatchStatus values.
"""

import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import get_db, engine
from Database.Models import Batches
from Database.enums import BatchStatus

# Status mapping for known invalid values
STATUS_MAPPING = {
    "brew_day": "brewing",
    "brewday": "brewing",
    "brew": "brewing",
    "ferment": "fermenting",
    "condition": "conditioning",
    "package": "packaging",
    "completed": "complete",
    "done": "complete",
}


def fix_batch_statuses():
    """Fix any invalid batch statuses in the database"""
    db = next(get_db())

    try:
        # Get all batches
        batches = db.query(Batches).all()

        fixed_count = 0
        invalid_batches = []

        for batch in batches:
            original_status = batch.status

            # Check if status is valid
            try:
                BatchStatus(original_status)
                # Valid status, no change needed
                continue
            except ValueError:
                # Invalid status - try to map it
                normalized_status = original_status.lower().strip()

                if normalized_status in STATUS_MAPPING:
                    new_status = STATUS_MAPPING[normalized_status]
                    batch.status = new_status
                    fixed_count += 1
                    print(
                        f"Fixed batch {batch.id} ({batch.batch_name}): '{original_status}' -> '{new_status}'")
                else:
                    # Unknown invalid status - default to planning
                    batch.status = BatchStatus.PLANNING.value
                    fixed_count += 1
                    print(
                        f"Fixed batch {batch.id} ({batch.batch_name}): '{original_status}' -> 'planning' (default)")

                invalid_batches.append({
                    "id": batch.id,
                    "name": batch.batch_name,
                    "old_status": original_status,
                    "new_status": batch.status
                })

        if fixed_count > 0:
            db.commit()
            print(f"\n✅ Fixed {fixed_count} batches with invalid statuses")
            print("\nInvalid batches found:")
            for b in invalid_batches:
                print(
                    f"  - Batch {b['id']}: {b['name']} ({b['old_status']} -> {b['new_status']})")
        else:
            print("✅ All batch statuses are valid!")

        # Show current status distribution
        print("\n📊 Current status distribution:")
        status_counts = db.query(Batches.status, text(
            "count(*) as count")).group_by(Batches.status).all()
        for status, count in status_counts:
            print(f"  - {status}: {count}")

        return fixed_count

    except Exception as e:
        print(f"❌ Error fixing batch statuses: {e}", file=sys.stderr)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🔧 Checking and fixing batch statuses...\n")
    fixed = fix_batch_statuses()
    sys.exit(0 if fixed >= 0 else 1)
