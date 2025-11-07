from __future__ import annotations

"""Enhance water profiles table with profile management features.

Revision ID: 0003
Revises: 0002
Create Date: 2024-11-06 10:20:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Numeric, Boolean, DateTime, Text, String
from sqlalchemy.exc import OperationalError, ProgrammingError, NoSuchTableError

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
    
    # Check if columns already exist (they might have been created by 0001_initial)
    # This allows the migration to be idempotent
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Get existing columns in the water table
    existing_columns = set()
    try:
        columns = inspector.get_columns('water')
        existing_columns = {col['name'] for col in columns}
    except (NoSuchTableError, OperationalError):
        # Table might not exist yet
        pass
    
    # Only add columns if they don't already exist
    with op.batch_alter_table('water', schema=None) as batch_op:
        # Add description field if it doesn't exist
        if 'description' not in existing_columns:
            batch_op.add_column(sa.Column('description', Text, nullable=True))

        # Add profile categorization if they don't exist
        if 'profile_type' not in existing_columns:
            batch_op.add_column(sa.Column('profile_type', String(50), nullable=False, server_default='source'))
        if 'style_category' not in existing_columns:
            batch_op.add_column(sa.Column('style_category', String(100), nullable=True))

        # Check if we need to alter ion concentration columns
        # Only alter if they are not already Numeric type
        if existing_columns:
            try:
                # Alter ion concentration columns to use Decimal for precision
                batch_op.alter_column('calcium', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
                batch_op.alter_column('magnesium', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
                batch_op.alter_column('sodium', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
                batch_op.alter_column('chloride', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
                batch_op.alter_column('sulfate', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
                batch_op.alter_column('bicarbonate', type_=Numeric(ION_PRECISION, ION_SCALE), nullable=False, server_default='0')
                
                # Alter pH to use Decimal
                batch_op.alter_column('ph', type_=Numeric(PH_PRECISION, PH_SCALE), nullable=True)
            except (OperationalError, ProgrammingError):
                # Columns might already be the correct type
                pass

        # Add additional water properties if they don't exist
        if 'total_alkalinity' not in existing_columns:
            batch_op.add_column(sa.Column('total_alkalinity', Numeric(ION_PRECISION, ION_SCALE), nullable=True))
        if 'residual_alkalinity' not in existing_columns:
            batch_op.add_column(sa.Column('residual_alkalinity', Numeric(ION_PRECISION, ION_SCALE), nullable=True))

        # Update notes column to Text if it's not already
        if existing_columns:
            try:
                batch_op.alter_column('notes', type_=Text, nullable=True)
            except (OperationalError, ProgrammingError):
                pass  # Already Text

        # Add metadata columns if they don't exist
        if 'is_default' not in existing_columns:
            batch_op.add_column(sa.Column('is_default', Boolean, nullable=False, server_default='0'))
        if 'is_custom' not in existing_columns:
            batch_op.add_column(sa.Column('is_custom', Boolean, nullable=False, server_default='1'))
        if 'created_at' not in existing_columns:
            batch_op.add_column(sa.Column('created_at', DateTime, nullable=False, server_default=sa.func.now()))
        if 'updated_at' not in existing_columns:
            batch_op.add_column(sa.Column('updated_at', DateTime, nullable=False, server_default=sa.func.now()))

        # Make name required if it's not already
        if existing_columns:
            try:
                batch_op.alter_column('name', nullable=False)
            except (OperationalError, ProgrammingError):
                pass  # Already not nullable


def downgrade() -> None:
    """Downgrade water profiles table to original schema."""
    
    # Check which columns exist before trying to drop them
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    existing_columns = set()
    try:
        columns = inspector.get_columns('water')
        existing_columns = {col['name'] for col in columns}
    except (NoSuchTableError, OperationalError):
        return  # Table doesn't exist, nothing to downgrade

    with op.batch_alter_table('water', schema=None) as batch_op:
        # Remove new columns only if they exist
        if 'description' in existing_columns:
            batch_op.drop_column('description')
        if 'profile_type' in existing_columns:
            batch_op.drop_column('profile_type')
        if 'style_category' in existing_columns:
            batch_op.drop_column('style_category')
        if 'total_alkalinity' in existing_columns:
            batch_op.drop_column('total_alkalinity')
        if 'residual_alkalinity' in existing_columns:
            batch_op.drop_column('residual_alkalinity')
        if 'is_default' in existing_columns:
            batch_op.drop_column('is_default')
        if 'is_custom' in existing_columns:
            batch_op.drop_column('is_custom')
        if 'created_at' in existing_columns:
            batch_op.drop_column('created_at')
        if 'updated_at' in existing_columns:
            batch_op.drop_column('updated_at')

        # Revert ion concentration columns to Integer
        try:
            batch_op.alter_column('calcium', type_=sa.Integer, nullable=True)
            batch_op.alter_column('magnesium', type_=sa.Integer, nullable=True)
            batch_op.alter_column('sodium', type_=sa.Integer, nullable=True)
            batch_op.alter_column('chloride', type_=sa.Integer, nullable=True)
            batch_op.alter_column('sulfate', type_=sa.Integer, nullable=True)
            batch_op.alter_column('bicarbonate', type_=sa.Integer, nullable=True)
            batch_op.alter_column('ph', type_=sa.Integer, nullable=True)
            batch_op.alter_column('notes', type_=String(255), nullable=True)
            batch_op.alter_column('name', nullable=True)
        except (OperationalError, ProgrammingError):
            pass  # Columns might not exist or already correct type
