from __future__ import annotations

"""Add foreign key indexes for performance optimization.

Revision ID: 0004
Revises: 0003
Create Date: 2025-11-07 20:00:00.000000

This migration adds missing foreign key indexes on inventory and profile tables
to prevent table scans and improve query performance significantly.

Related: Issue #123 - Database Performance Optimization
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def get_existing_indexes(bind, table_name: str) -> set[str]:
    """Get set of existing index names for a table."""
    inspector = inspect(bind)
    try:
        indexes = inspector.get_indexes(table_name)
        return {idx['name'] for idx in indexes}
    except Exception:
        return set()


def has_column(bind, table_name: str, column_name: str) -> bool:
    """Check if a table has a specific column."""
    inspector = inspect(bind)
    try:
        columns = inspector.get_columns(table_name)
        return any(col['name'] == column_name for col in columns)
    except Exception:
        return False


def upgrade() -> None:
    """Add foreign key indexes for performance optimization."""

    bind = op.get_bind()

    # Inventory Fermentables indexes
    if 'inventory_fermentables' in inspect(bind).get_table_names():
        existing = get_existing_indexes(bind, 'inventory_fermentables')

        if has_column(bind, 'inventory_fermentables', 'batch_id') and 'idx_inventory_fermentables_batch_id' not in existing:
            op.create_index(
                'idx_inventory_fermentables_batch_id',
                'inventory_fermentables',
                ['batch_id']
            )

        # Only create recipe_id index if column exists
        if has_column(bind, 'inventory_fermentables', 'recipe_id') and 'idx_inventory_fermentables_recipe_id' not in existing:
            op.create_index(
                'idx_inventory_fermentables_recipe_id',
                'inventory_fermentables',
                ['recipe_id']
            )

    # Inventory Hops indexes
    if 'inventory_hops' in inspect(bind).get_table_names():
        existing = get_existing_indexes(bind, 'inventory_hops')

        if has_column(bind, 'inventory_hops', 'batch_id') and 'idx_inventory_hops_batch_id' not in existing:
            op.create_index(
                'idx_inventory_hops_batch_id',
                'inventory_hops',
                ['batch_id']
            )

        # Only create recipe_id index if column exists
        if has_column(bind, 'inventory_hops', 'recipe_id') and 'idx_inventory_hops_recipe_id' not in existing:
            op.create_index(
                'idx_inventory_hops_recipe_id',
                'inventory_hops',
                ['recipe_id']
            )

    # Inventory Yeasts indexes
    if 'inventory_yeasts' in inspect(bind).get_table_names():
        existing = get_existing_indexes(bind, 'inventory_yeasts')

        if has_column(bind, 'inventory_yeasts', 'batch_id') and 'idx_inventory_yeasts_batch_id' not in existing:
            op.create_index(
                'idx_inventory_yeasts_batch_id',
                'inventory_yeasts',
                ['batch_id']
            )

        # Only create recipe_id index if column exists
        if has_column(bind, 'inventory_yeasts', 'recipe_id') and 'idx_inventory_yeasts_recipe_id' not in existing:
            op.create_index(
                'idx_inventory_yeasts_recipe_id',
                'inventory_yeasts',
                ['recipe_id']
            )

    # Inventory Miscs indexes
    if 'inventory_miscs' in inspect(bind).get_table_names():
        existing = get_existing_indexes(bind, 'inventory_miscs')

        if has_column(bind, 'inventory_miscs', 'batch_id') and 'idx_inventory_miscs_batch_id' not in existing:
            op.create_index(
                'idx_inventory_miscs_batch_id',
                'inventory_miscs',
                ['batch_id']
            )

        # Only create recipe_id index if column exists
        if has_column(bind, 'inventory_miscs', 'recipe_id') and 'idx_inventory_miscs_recipe_id' not in existing:
            op.create_index(
                'idx_inventory_miscs_recipe_id',
                'inventory_miscs',
                ['recipe_id']
            )

    # Fermentation Steps index
    if 'fermentation_steps' in inspect(bind).get_table_names():
        existing = get_existing_indexes(bind, 'fermentation_steps')

        if 'idx_fermentation_steps_profile_id' not in existing:
            op.create_index(
                'idx_fermentation_steps_profile_id',
                'fermentation_steps',
                ['fermentation_profile_id']
            )

    # Mash Step index
    if 'mash_step' in inspect(bind).get_table_names():
        existing = get_existing_indexes(bind, 'mash_step')

        if 'idx_mash_step_mash_id' not in existing:
            op.create_index(
                'idx_mash_step_mash_id',
                'mash_step',
                ['mash_id']
            )

    # Choices index
    if 'choices' in inspect(bind).get_table_names():
        existing = get_existing_indexes(bind, 'choices')

        if 'idx_choices_question_id' not in existing:
            op.create_index(
                'idx_choices_question_id',
                'choices',
                ['question_id']
            )


def downgrade() -> None:
    """Remove foreign key indexes."""

    bind = op.get_bind()

    # Drop indexes in reverse order
    if 'choices' in inspect(bind).get_table_names():
        try:
            op.drop_index('idx_choices_question_id', table_name='choices')
        except Exception:
            pass

    if 'mash_step' in inspect(bind).get_table_names():
        try:
            op.drop_index('idx_mash_step_mash_id', table_name='mash_step')
        except Exception:
            pass

    if 'fermentation_steps' in inspect(bind).get_table_names():
        try:
            op.drop_index('idx_fermentation_steps_profile_id',
                          table_name='fermentation_steps')
        except Exception:
            pass

    if 'inventory_miscs' in inspect(bind).get_table_names():
        try:
            op.drop_index('idx_inventory_miscs_recipe_id',
                          table_name='inventory_miscs')
            op.drop_index('idx_inventory_miscs_batch_id',
                          table_name='inventory_miscs')
        except Exception:
            pass

    if 'inventory_yeasts' in inspect(bind).get_table_names():
        try:
            op.drop_index('idx_inventory_yeasts_recipe_id',
                          table_name='inventory_yeasts')
            op.drop_index('idx_inventory_yeasts_batch_id',
                          table_name='inventory_yeasts')
        except Exception:
            pass

    if 'inventory_hops' in inspect(bind).get_table_names():
        try:
            op.drop_index('idx_inventory_hops_recipe_id',
                          table_name='inventory_hops')
            op.drop_index('idx_inventory_hops_batch_id',
                          table_name='inventory_hops')
        except Exception:
            pass

    if 'inventory_fermentables' in inspect(bind).get_table_names():
        try:
            op.drop_index('idx_inventory_fermentables_recipe_id',
                          table_name='inventory_fermentables')
            op.drop_index('idx_inventory_fermentables_batch_id',
                          table_name='inventory_fermentables')
        except Exception:
            pass
