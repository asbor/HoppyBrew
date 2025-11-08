"""add barcode fields to inventory tables

Revision ID: 0008_add_barcode_fields
Revises: 0007_add_inventory_tracking
Create Date: 2025-11-08 17:30:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0008_add_barcode_fields"
down_revision = "0007_add_inventory_tracking"
branch_labels = None
depends_on = None


def upgrade():
    # Add barcode column to inventory_hops
    op.add_column(
        "inventory_hops",
        sa.Column("barcode", sa.String(), nullable=True),
    )
    op.create_index(
        "ix_inventory_hops_barcode", "inventory_hops", ["barcode"], unique=True
    )

    # Add barcode column to inventory_fermentables
    op.add_column(
        "inventory_fermentables",
        sa.Column("barcode", sa.String(), nullable=True),
    )
    op.create_index(
        "ix_inventory_fermentables_barcode",
        "inventory_fermentables",
        ["barcode"],
        unique=True,
    )

    # Add barcode column to inventory_yeasts
    op.add_column(
        "inventory_yeasts",
        sa.Column("barcode", sa.String(), nullable=True),
    )
    op.create_index(
        "ix_inventory_yeasts_barcode", "inventory_yeasts", ["barcode"], unique=True
    )

    # Add barcode column to inventory_miscs
    op.add_column(
        "inventory_miscs",
        sa.Column("barcode", sa.String(), nullable=True),
    )
    op.create_index(
        "ix_inventory_miscs_barcode", "inventory_miscs", ["barcode"], unique=True
    )


def downgrade():
    # Remove barcode columns and indexes
    op.drop_index("ix_inventory_miscs_barcode", "inventory_miscs")
    op.drop_column("inventory_miscs", "barcode")

    op.drop_index("ix_inventory_yeasts_barcode", "inventory_yeasts")
    op.drop_column("inventory_yeasts", "barcode")

    op.drop_index("ix_inventory_fermentables_barcode", "inventory_fermentables")
    op.drop_column("inventory_fermentables", "barcode")

    op.drop_index("ix_inventory_hops_barcode", "inventory_hops")
    op.drop_column("inventory_hops", "barcode")
