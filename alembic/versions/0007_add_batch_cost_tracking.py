"""Add batch cost tracking tables

Revision ID: 0007
Revises: 0006
Create Date: 2024-11-08

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
    # Create batch_costs table
    op.create_table(
        'batch_costs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('fermentables_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('hops_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('yeasts_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('miscs_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('electricity_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('water_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('gas_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('other_utility_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('labor_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('packaging_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('other_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cost_per_liter', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('cost_per_pint', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('target_price_per_pint', sa.Float(), nullable=True),
        sa.Column('profit_margin', sa.Float(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_batch_costs_id', 'batch_costs', ['id'], unique=False)
    op.create_index('ix_batch_costs_batch_id', 'batch_costs', ['batch_id'], unique=False)
    op.create_index('ix_batch_costs_created_at', 'batch_costs', ['created_at'], unique=False)

    # Create utility_cost_configs table
    op.create_table(
        'utility_cost_configs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('electricity_rate_per_kwh', sa.Float(), nullable=True),
        sa.Column('water_rate_per_liter', sa.Float(), nullable=True),
        sa.Column('gas_rate_per_unit', sa.Float(), nullable=True),
        sa.Column('avg_electricity_kwh_per_batch', sa.Float(), nullable=True),
        sa.Column('avg_water_liters_per_batch', sa.Float(), nullable=True),
        sa.Column('avg_gas_units_per_batch', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(), nullable=False, server_default='USD'),
        sa.Column('is_active', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_utility_cost_configs_id', 'utility_cost_configs', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_utility_cost_configs_id', table_name='utility_cost_configs')
    op.drop_table('utility_cost_configs')
    op.drop_index('ix_batch_costs_created_at', table_name='batch_costs')
    op.drop_index('ix_batch_costs_batch_id', table_name='batch_costs')
    op.drop_index('ix_batch_costs_id', table_name='batch_costs')
    op.drop_table('batch_costs')
