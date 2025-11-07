"""Add status field to batches table for phase-based workflow

Revision ID: add_batch_status
Revises: add_devices_table
Create Date: 2025-11-07 16:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "add_batch_status"
down_revision: Union[str, None] = "add_devices_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add status column to batches table"""

    # Add status column with default value
    op.add_column(
        "batches",
        sa.Column("status", sa.String(length=50), nullable=False, server_default="planning"),
    )

    # Create index on status for faster filtering
    op.create_index("ix_batches_status", "batches", ["status"])


def downgrade() -> None:
    """Remove status column from batches table"""

    # Drop index first
    op.drop_index("ix_batches_status", "batches")

    # Drop status column
    op.drop_column("batches", "status")
