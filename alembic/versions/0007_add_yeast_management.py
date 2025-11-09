"""Add yeast management tables

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-09 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add yeast management tables and enhance inventory_yeasts"""
    
    # Create yeast_strains table
    op.create_table(
        'yeast_strains',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('laboratory', sa.String(), nullable=True),
        sa.Column('product_id', sa.String(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('form', sa.String(), nullable=True),
        sa.Column('min_temperature', sa.Float(), nullable=True),
        sa.Column('max_temperature', sa.Float(), nullable=True),
        sa.Column('flocculation', sa.String(), nullable=True),
        sa.Column('attenuation_min', sa.Float(), nullable=True),
        sa.Column('attenuation_max', sa.Float(), nullable=True),
        sa.Column('alcohol_tolerance', sa.Float(), nullable=True),
        sa.Column('best_for', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('max_reuse', sa.Integer(), nullable=True, default=5),
        sa.Column('viability_days_dry', sa.Integer(), nullable=True, default=1095),
        sa.Column('viability_days_liquid', sa.Integer(), nullable=True, default=180),
        sa.Column('viability_days_slant', sa.Integer(), nullable=True, default=730),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_yeast_strains_id', 'yeast_strains', ['id'])
    op.create_index('ix_yeast_strains_name', 'yeast_strains', ['name'])
    op.create_index('ix_yeast_strains_product_id', 'yeast_strains', ['product_id'])
    
    # Create yeast_harvests table
    op.create_table(
        'yeast_harvests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_batch_id', sa.Integer(), nullable=True),
        sa.Column('source_inventory_id', sa.Integer(), nullable=True),
        sa.Column('yeast_strain_id', sa.Integer(), nullable=False),
        sa.Column('harvest_date', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('generation', sa.Integer(), nullable=False, default=1),
        sa.Column('parent_harvest_id', sa.Integer(), nullable=True),
        sa.Column('quantity_harvested', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(20), nullable=False, server_default='ml'),
        sa.Column('viability_at_harvest', sa.Float(), nullable=True),
        sa.Column('cell_count', sa.Float(), nullable=True),
        sa.Column('storage_method', sa.String(), nullable=True),
        sa.Column('storage_temperature', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('used_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['source_batch_id'], ['batches.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['yeast_strain_id'], ['yeast_strains.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_harvest_id'], ['yeast_harvests.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_yeast_harvests_id', 'yeast_harvests', ['id'])
    op.create_index('ix_yeast_harvests_yeast_strain_id', 'yeast_harvests', ['yeast_strain_id'])
    op.create_index('ix_yeast_harvests_source_batch_id', 'yeast_harvests', ['source_batch_id'])
    op.create_index('ix_yeast_harvests_status', 'yeast_harvests', ['status'])
    
    # Add yeast management fields to inventory_yeasts
    op.add_column('inventory_yeasts', sa.Column('yeast_strain_id', sa.Integer(), nullable=True))
    op.add_column('inventory_yeasts', sa.Column('manufacture_date', sa.DateTime(), nullable=True))
    op.add_column('inventory_yeasts', sa.Column('expiry_date', sa.DateTime(), nullable=True))
    op.add_column('inventory_yeasts', sa.Column('generation', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('inventory_yeasts', sa.Column('harvest_id', sa.Integer(), nullable=True))
    op.add_column('inventory_yeasts', sa.Column('current_viability', sa.Float(), nullable=True))
    op.add_column('inventory_yeasts', sa.Column('last_viability_check', sa.DateTime(), nullable=True))
    
    # Add foreign keys for inventory_yeasts
    op.create_foreign_key(
        'fk_inventory_yeasts_yeast_strain_id',
        'inventory_yeasts', 'yeast_strains',
        ['yeast_strain_id'], ['id'],
        ondelete='SET NULL'
    )
    op.create_foreign_key(
        'fk_inventory_yeasts_harvest_id',
        'inventory_yeasts', 'yeast_harvests',
        ['harvest_id'], ['id'],
        ondelete='SET NULL'
    )
    
    # Add indexes for better query performance
    op.create_index('ix_inventory_yeasts_yeast_strain_id', 'inventory_yeasts', ['yeast_strain_id'])
    op.create_index('ix_inventory_yeasts_harvest_id', 'inventory_yeasts', ['harvest_id'])
    op.create_index('ix_inventory_yeasts_generation', 'inventory_yeasts', ['generation'])


def downgrade() -> None:
    """Remove yeast management tables and fields"""
    
    # Remove indexes from inventory_yeasts
    op.drop_index('ix_inventory_yeasts_generation', 'inventory_yeasts')
    op.drop_index('ix_inventory_yeasts_harvest_id', 'inventory_yeasts')
    op.drop_index('ix_inventory_yeasts_yeast_strain_id', 'inventory_yeasts')
    
    # Remove foreign keys from inventory_yeasts
    op.drop_constraint('fk_inventory_yeasts_harvest_id', 'inventory_yeasts', type_='foreignkey')
    op.drop_constraint('fk_inventory_yeasts_yeast_strain_id', 'inventory_yeasts', type_='foreignkey')
    
    # Remove columns from inventory_yeasts
    op.drop_column('inventory_yeasts', 'last_viability_check')
    op.drop_column('inventory_yeasts', 'current_viability')
    op.drop_column('inventory_yeasts', 'harvest_id')
    op.drop_column('inventory_yeasts', 'generation')
    op.drop_column('inventory_yeasts', 'expiry_date')
    op.drop_column('inventory_yeasts', 'manufacture_date')
    op.drop_column('inventory_yeasts', 'yeast_strain_id')
    
    # Drop yeast_harvests table
    op.drop_index('ix_yeast_harvests_status', 'yeast_harvests')
    op.drop_index('ix_yeast_harvests_source_batch_id', 'yeast_harvests')
    op.drop_index('ix_yeast_harvests_yeast_strain_id', 'yeast_harvests')
    op.drop_index('ix_yeast_harvests_id', 'yeast_harvests')
    op.drop_table('yeast_harvests')
    
    # Drop yeast_strains table
    op.drop_index('ix_yeast_strains_product_id', 'yeast_strains')
    op.drop_index('ix_yeast_strains_name', 'yeast_strains')
    op.drop_index('ix_yeast_strains_id', 'yeast_strains')
    op.drop_table('yeast_strains')
