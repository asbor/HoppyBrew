"""Add recipe ingredient fields and recipe versions table

Revision ID: add_recipe_editor_features
Revises: add_batch_status
Create Date: 2024-11-08 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "add_recipe_editor_features"
down_revision: Union[str, None] = "add_batch_status"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add stage and duration fields to recipe ingredients and create recipe_versions table"""

    # Add stage and duration columns to recipe_hops
    op.add_column(
        "recipe_hops",
        sa.Column("stage", sa.String(), nullable=True),
    )
    op.add_column(
        "recipe_hops",
        sa.Column("duration", sa.Integer(), nullable=True),
    )

    # Add stage and duration columns to recipe_fermentables
    op.add_column(
        "recipe_fermentables",
        sa.Column("stage", sa.String(), nullable=True),
    )
    op.add_column(
        "recipe_fermentables",
        sa.Column("duration", sa.Integer(), nullable=True),
    )

    # Add stage and duration columns to recipe_yeasts
    op.add_column(
        "recipe_yeasts",
        sa.Column("stage", sa.String(), nullable=True),
    )
    op.add_column(
        "recipe_yeasts",
        sa.Column("duration", sa.Integer(), nullable=True),
    )

    # Add stage and duration columns to recipe_miscs
    op.add_column(
        "recipe_miscs",
        sa.Column("stage", sa.String(), nullable=True),
    )
    op.add_column(
        "recipe_miscs",
        sa.Column("duration", sa.Integer(), nullable=True),
    )

    # Create recipe_versions table
    op.create_table(
        "recipe_versions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("version_name", sa.String(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("recipe_snapshot", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recipe_versions_recipe_id", "recipe_versions", ["recipe_id"])
    op.create_index(
        "ix_recipe_versions_version_number", "recipe_versions", ["version_number"]
    )


def downgrade() -> None:
    """Remove stage and duration fields and recipe_versions table"""

    # Drop recipe_versions table and its indexes
    op.drop_index("ix_recipe_versions_version_number", "recipe_versions")
    op.drop_index("ix_recipe_versions_recipe_id", "recipe_versions")
    op.drop_table("recipe_versions")

    # Drop stage and duration columns from recipe_miscs
    op.drop_column("recipe_miscs", "duration")
    op.drop_column("recipe_miscs", "stage")

    # Drop stage and duration columns from recipe_yeasts
    op.drop_column("recipe_yeasts", "duration")
    op.drop_column("recipe_yeasts", "stage")

    # Drop stage and duration columns from recipe_fermentables
    op.drop_column("recipe_fermentables", "duration")
    op.drop_column("recipe_fermentables", "stage")

    # Drop stage and duration columns from recipe_hops
    op.drop_column("recipe_hops", "duration")
    op.drop_column("recipe_hops", "stage")
