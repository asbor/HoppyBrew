"""Add packaging_details table

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-09 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create packaging_details table for batch packaging information"""
    op.create_table(
        'packaging_details',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('packaging_date', sa.DateTime(), nullable=False),
        sa.Column('method', sa.String(50), nullable=False),
        sa.Column('carbonation_method', sa.String(50), nullable=False),
        sa.Column('volumes_co2', sa.Float(), nullable=True),
        sa.Column('container_count', sa.Integer(), nullable=True),
        sa.Column('container_size', sa.Float(), nullable=True),
        sa.Column('priming_sugar_amount', sa.Float(), nullable=True),
        sa.Column('priming_sugar_type', sa.String(50), nullable=True),
        sa.Column('pressure_psi', sa.Float(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['batch_id'], 
            ['batches.id'], 
            ondelete='CASCADE'
        ),
        sa.UniqueConstraint('batch_id')
    )
    
    # Create indexes for better query performance
    op.create_index(
        'ix_packaging_details_batch_id', 
        'packaging_details', 
        ['batch_id']
    )
    op.create_index(
        'ix_packaging_details_date', 
        'packaging_details', 
        ['packaging_date']
    )
    op.create_index(
        'ix_packaging_details_id', 
        'packaging_details', 
        ['id']
    )


def downgrade() -> None:
    """Drop packaging_details table"""
    op.drop_index('ix_packaging_details_id', 'packaging_details')
    op.drop_index('ix_packaging_details_date', 'packaging_details')
    op.drop_index('ix_packaging_details_batch_id', 'packaging_details')
    op.drop_table('packaging_details')
