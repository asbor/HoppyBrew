"""Add status field to batches table for phase-based workflow

Revision ID: 0003
Revises: 0002
Create Date: 2025-11-07 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade():
    """Add status column to batches table"""
    
    # Add status column with default value
    op.add_column('batches', 
        sa.Column('status', sa.String(length=50), nullable=False, server_default='planning')
    )
    
    # Create index on status for faster filtering
    op.create_index('ix_batches_status', 'batches', ['status'])


def downgrade():
    """Remove status column from batches table"""
    
    # Drop index first
    op.drop_index('ix_batches_status', 'batches')
    
    # Drop status column
    op.drop_column('batches', 'status')
