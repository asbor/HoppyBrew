"""Add batch workflow history table

Revision ID: add_workflow_history
Revises: add_batch_status
Create Date: 2025-11-08 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = "add_workflow_history"
down_revision: Union[str, None] = "add_batch_status"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add batch_workflow_history table for tracking status changes"""

    # Create batch_workflow_history table
    op.create_table(
        "batch_workflow_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=False),
        sa.Column("from_status", sa.String(length=50), nullable=True),
        sa.Column("to_status", sa.String(length=50), nullable=False),
        sa.Column("changed_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column("notes", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for faster queries
    op.create_index("ix_batch_workflow_history_id", "batch_workflow_history", ["id"])
    op.create_index(
        "ix_batch_workflow_history_batch_id", "batch_workflow_history", ["batch_id"]
    )
    op.create_index(
        "ix_batch_workflow_history_changed_at", "batch_workflow_history", ["changed_at"]
    )


def downgrade() -> None:
    """Remove batch_workflow_history table"""

    # Drop indexes first
    op.drop_index("ix_batch_workflow_history_changed_at", "batch_workflow_history")
    op.drop_index("ix_batch_workflow_history_batch_id", "batch_workflow_history")
    op.drop_index("ix_batch_workflow_history_id", "batch_workflow_history")

    # Drop table
    op.drop_table("batch_workflow_history")
