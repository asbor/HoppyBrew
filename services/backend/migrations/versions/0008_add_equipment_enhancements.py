"""add equipment efficiency and batch association

Revision ID: 0008_add_equipment_enhancements
Revises: 0007_add_inventory_tracking
Create Date: 2025-11-09 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0008_add_equipment_enhancements"
down_revision = "0007_add_inventory_tracking"
branch_labels = None
depends_on = None


def upgrade():
    # Add efficiency tracking fields to equipment table
    op.add_column(
        "equipment",
        sa.Column("brewhouse_efficiency", sa.Float(), nullable=True)
    )
    op.add_column(
        "equipment",
        sa.Column("mash_efficiency", sa.Float(), nullable=True)
    )
    
    # Add equipment_id foreign key to batches table
    op.add_column(
        "batches",
        sa.Column("equipment_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "fk_batches_equipment_id",
        "batches",
        "equipment",
        ["equipment_id"],
        ["id"],
    )
    op.create_index(
        "ix_batches_equipment_id",
        "batches",
        ["equipment_id"],
    )


def downgrade():
    # Remove equipment_id from batches
    op.drop_index("ix_batches_equipment_id", table_name="batches")
    op.drop_constraint("fk_batches_equipment_id", "batches", type_="foreignkey")
    op.drop_column("batches", "equipment_id")
    
    # Remove efficiency fields from equipment
    op.drop_column("equipment", "mash_efficiency")
    op.drop_column("equipment", "brewhouse_efficiency")
