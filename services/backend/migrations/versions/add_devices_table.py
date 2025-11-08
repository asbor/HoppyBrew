"""Add devices table

Revision ID: add_devices_table
Revises: 84e86493f0d8
Create Date: 2025-11-05 22:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "add_devices_table"
down_revision: Union[str, None] = "84e86493f0d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create devices table
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("device_type", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("api_endpoint", sa.String(), nullable=True),
        sa.Column("api_token", sa.String(), nullable=True),
        sa.Column("calibration_data", sa.JSON(), nullable=True),
        sa.Column("configuration", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_devices_id"), "devices", ["id"], unique=False)


def downgrade() -> None:
    # Drop devices table
    op.drop_index(op.f("ix_devices_id"), table_name="devices")
    op.drop_table("devices")
