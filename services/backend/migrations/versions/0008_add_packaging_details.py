"""add packaging details table

Revision ID: 0008_add_packaging_details
Revises: 0007_add_inventory_tracking
Create Date: 2025-11-09 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = "0008_add_packaging_details"
down_revision = "0007_add_inventory_tracking"
branch_labels = None
depends_on = None


def upgrade():
    # Create packaging_details table
    op.create_table(
        "packaging_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=False),
        sa.Column("method", sa.String(length=50), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column("carbonation_method", sa.String(length=50), nullable=True),
        sa.Column("volumes", sa.Float(), nullable=True),
        sa.Column("container_count", sa.Integer(), nullable=True),
        sa.Column("container_size", sa.Float(), nullable=True),
        sa.Column("priming_sugar_type", sa.String(length=50), nullable=True),
        sa.Column("priming_sugar_amount", sa.Float(), nullable=True),
        sa.Column("carbonation_temp", sa.Float(), nullable=True),
        sa.Column("carbonation_psi", sa.Float(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column("updated_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("batch_id"),
    )
    op.create_index("ix_packaging_details_id", "packaging_details", ["id"])
    op.create_index("ix_packaging_details_batch_id", "packaging_details", ["batch_id"], unique=True)


def downgrade():
    op.drop_index("ix_packaging_details_batch_id", "packaging_details")
    op.drop_index("ix_packaging_details_id", "packaging_details")
    op.drop_table("packaging_details")
