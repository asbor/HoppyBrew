from __future__ import annotations

"""Enhance water profiles table with profile management features.

Revision ID: 0003_water_profiles_enhancement
Revises: 0002
Create Date: 2024-11-06 10:20:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Numeric, Boolean, DateTime, Text, String

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

# Constants for numeric precision
ION_PRECISION = 8
ION_SCALE = 2
PH_PRECISION = 4
PH_SCALE = 2


def upgrade() -> None:
    """Upgrade water profiles table with enhanced profile management features."""

    # Add new columns for profile management
    with op.batch_alter_table('water', schema=None) as batch_op:
        # Add description field
        batch_op.add_column(sa.Column('description', Text, nullable=True))

        # Add profile categorization
        batch_op.add_column(sa.Column('profile_type', String(50), nullable=False, server_default='source'))
        batch_op.add_column(sa.Column('style_category', String(100), nullable=True))

        # Alter ion concentration columns to use Decimal for precision
        batch_op.alter_column('calcium', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
        batch_op.alter_column('magnesium', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
        batch_op.alter_column('sodium', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
        batch_op.alter_column('chloride', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
        batch_op.alter_column('sulfate', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
        batch_op.alter_column('bicarbonate', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')

        # Alter pH to use Decimal
        batch_op.alter_column('ph', type_=Numeric(PH_PRECISION, PH_SCALE), nullable=True)

        # Add additional water properties
        batch_op.add_column(sa.Column('total_alkalinity', Numeric(ION_PRECISION, ION_SCALE), nullable=True))
        batch_op.add_column(sa.Column('residual_alkalinity', Numeric(ION_PRECISION, ION_SCALE), nullable=True))

        # Update notes column to Text
        batch_op.alter_column('notes', type_=Text, nullable=True)

        # Add metadata columns
        batch_op.add_column(sa.Column('is_default', Boolean, nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('is_custom', Boolean, nullable=False, server_default='1'))
        batch_op.add_column(sa.Column('created_at', DateTime, nullable=False, server_default=sa.func.now()))
        batch_op.add_column(sa.Column('updated_at', DateTime, nullable=False, server_default=sa.func.now()))

        # Make name required
        batch_op.alter_column('name', nullable=False)


def downgrade() -> None:
    """Downgrade water profiles table to original schema."""

    with op.batch_alter_table('water', schema=None) as batch_op:
        # Remove new columns
        batch_op.drop_column('description')
        batch_op.drop_column('profile_type')
        batch_op.drop_column('style_category')
        batch_op.drop_column('total_alkalinity')
        batch_op.drop_column('residual_alkalinity')
        batch_op.drop_column('is_default')
        batch_op.drop_column('is_custom')
        batch_op.drop_column('created_at')
        batch_op.drop_column('updated_at')

        # Revert ion concentration columns to Integer
        batch_op.alter_column('calcium', type_=sa.Integer, nullable=True)
        batch_op.alter_column('magnesium', type_=sa.Integer, nullable=True)
        batch_op.alter_column('sodium', type_=sa.Integer, nullable=True)
        batch_op.alter_column('chloride', type_=sa.Integer, nullable=True)
        batch_op.alter_column('sulfate', type_=sa.Integer, nullable=True)
        batch_op.alter_column('bicarbonate', type_=sa.Integer, nullable=True)

        # Revert pH to Integer
        batch_op.alter_column('ph', type_=sa.Integer, nullable=True)

        # Revert notes to String
        batch_op.alter_column('notes', type_=String(255), nullable=True)

        # Make name nullable again
        batch_op.alter_column('name', nullable=True)
