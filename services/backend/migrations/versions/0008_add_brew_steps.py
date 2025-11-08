"""add brew_steps table

Revision ID: 0008_add_brew_steps
Revises: 0007_add_inventory_tracking
Create Date: 2025-11-08 17:30:00.000000

"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = "0008_add_brew_steps"
down_revision = "0007_add_inventory_tracking"
branch_labels = None
depends_on = None


def upgrade():
    # Create brew_steps table
    op.create_table(
        "brew_steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=False),
        sa.Column("step_name", sa.String(length=100), nullable=False),
        sa.Column("step_type", sa.String(length=50), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("temperature", sa.Integer(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, default=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column("updated_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column("order_index", sa.Integer(), nullable=False, default=0),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_brew_steps_id", "brew_steps", ["id"])
    op.create_index("ix_brew_steps_batch_id", "brew_steps", ["batch_id"])
    op.create_index("ix_brew_steps_completed", "brew_steps", ["completed"])


def downgrade():
    op.drop_index("ix_brew_steps_completed", "brew_steps")
    op.drop_index("ix_brew_steps_batch_id", "brew_steps")
    op.drop_index("ix_brew_steps_id", "brew_steps")
    op.drop_table("brew_steps")
