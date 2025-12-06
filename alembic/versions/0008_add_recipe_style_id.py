from __future__ import annotations

"""Add style_id to recipes for beer style linkage.

Revision ID: 0008
Revises: 0007_add_yeast_management
Create Date: 2024-12-06 09:00:00.000000

This migration adds a style_id foreign key column to the recipes table
to enable linking recipes to beer styles from the beer_styles table.

Related: Recipe-to-style linkage feature
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007_add_yeast_management"
branch_labels = None
depends_on = None


def has_column(bind, table_name: str, column_name: str) -> bool:
    """Check if a table has a specific column."""
    inspector = inspect(bind)
    try:
        columns = inspector.get_columns(table_name)
        return any(col['name'] == column_name for col in columns)
    except Exception:
        return False


def has_index(bind, table_name: str, index_name: str) -> bool:
    """Check if a table has a specific index."""
    inspector = inspect(bind)
    try:
        indexes = inspector.get_indexes(table_name)
        return any(idx['name'] == index_name for idx in indexes)
    except Exception:
        return False


def upgrade() -> None:
    """Add style_id column and index to recipes table."""
    bind = op.get_bind()

    # Add style_id column if it doesn't exist
    if not has_column(bind, 'recipes', 'style_id'):
        op.add_column(
            'recipes',
            sa.Column(
                'style_id',
                sa.Integer(),
                sa.ForeignKey('beer_styles.id'),
                nullable=True
            )
        )

    # Add index for style_id if it doesn't exist
    if not has_index(bind, 'recipes', 'ix_recipes_style_id'):
        op.create_index(
            'ix_recipes_style_id',
            'recipes',
            ['style_id'],
            unique=False
        )


def downgrade() -> None:
    """Remove style_id column and index from recipes table."""
    bind = op.get_bind()

    # Drop index first
    if has_index(bind, 'recipes', 'ix_recipes_style_id'):
        op.drop_index('ix_recipes_style_id', table_name='recipes')

    # Drop column
    if has_column(bind, 'recipes', 'style_id'):
        op.drop_column('recipes', 'style_id')
