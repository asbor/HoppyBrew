"""Add cost tracking fields to ingredients and batch costs table

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-08 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add cost tracking capabilities"""
    
    # Add cost_per_unit to recipe_hops
    op.add_column('recipe_hops', sa.Column('cost_per_unit', sa.Float, nullable=True))
    
    # Add cost_per_unit to inventory_hops
    op.add_column('inventory_hops', sa.Column('cost_per_unit', sa.Float, nullable=True))
    
    # Add cost_per_unit to recipe_yeasts
    op.add_column('recipe_yeasts', sa.Column('cost_per_unit', sa.Float, nullable=True))
    
    # Add cost_per_unit to inventory_yeasts
    op.add_column('inventory_yeasts', sa.Column('cost_per_unit', sa.Float, nullable=True))
    
    # Add cost_per_unit to recipe_miscs
    op.add_column('recipe_miscs', sa.Column('cost_per_unit', sa.Float, nullable=True))
    
    # Add cost_per_unit to inventory_miscs
    op.add_column('inventory_miscs', sa.Column('cost_per_unit', sa.Float, nullable=True))
    
    # Create batch_costs table
    op.create_table(
        'batch_costs',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('batch_id', sa.Integer, sa.ForeignKey('batches.id'), nullable=False, unique=True),
        
        # Ingredient costs
        sa.Column('fermentables_cost', sa.Float, default=0.0, nullable=False),
        sa.Column('hops_cost', sa.Float, default=0.0, nullable=False),
        sa.Column('yeasts_cost', sa.Float, default=0.0, nullable=False),
        sa.Column('miscs_cost', sa.Float, default=0.0, nullable=False),
        
        # Utility costs
        sa.Column('electricity_cost', sa.Float, default=0.0, nullable=False),
        sa.Column('water_cost', sa.Float, default=0.0, nullable=False),
        sa.Column('gas_cost', sa.Float, default=0.0, nullable=False),
        
        # Other costs
        sa.Column('labor_cost', sa.Float, default=0.0, nullable=False),
        sa.Column('packaging_cost', sa.Float, default=0.0, nullable=False),
        sa.Column('other_cost', sa.Float, default=0.0, nullable=False),
        
        # Sales information
        sa.Column('expected_yield_volume', sa.Float, nullable=True),
        sa.Column('selling_price_per_unit', sa.Float, nullable=True),
        sa.Column('unit_type', sa.String, default='pint', nullable=False),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime, default=datetime.now, nullable=False),
        sa.Column('updated_at', sa.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
    )
    
    # Create indexes for batch_costs
    op.create_index('ix_batch_costs_batch_id', 'batch_costs', ['batch_id'])


def downgrade() -> None:
    """Remove cost tracking capabilities"""
    
    # Drop batch_costs table
    op.drop_index('ix_batch_costs_batch_id', 'batch_costs')
    op.drop_table('batch_costs')
    
    # Remove cost_per_unit from ingredient tables
    op.drop_column('recipe_hops', 'cost_per_unit')
    op.drop_column('inventory_hops', 'cost_per_unit')
    op.drop_column('recipe_yeasts', 'cost_per_unit')
    op.drop_column('inventory_yeasts', 'cost_per_unit')
    op.drop_column('recipe_miscs', 'cost_per_unit')
    op.drop_column('inventory_miscs', 'cost_per_unit')
