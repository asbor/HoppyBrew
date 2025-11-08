"""add inventory tracking tables

Revision ID: 0007_add_inventory_tracking
Revises: add_devices_table
Create Date: 2025-11-08 10:12:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '0007_add_inventory_tracking'
down_revision = 'add_devices_table'
branch_labels = None
depends_on = None


def upgrade():
    # Create batch_ingredients table
    op.create_table(
        'batch_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('inventory_item_id', sa.Integer(), nullable=False),
        sa.Column('inventory_item_type', sa.String(length=50), nullable=False),
        sa.Column('quantity_used', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_batch_ingredients_id', 'batch_ingredients', ['id'])
    op.create_index('ix_batch_ingredients_batch_id', 'batch_ingredients', ['batch_id'])
    op.create_index('ix_batch_ingredients_inventory_item_id', 'batch_ingredients', ['inventory_item_id'])

    # Create inventory_transactions table
    op.create_table(
        'inventory_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('inventory_item_id', sa.Integer(), nullable=False),
        sa.Column('inventory_item_type', sa.String(length=50), nullable=False),
        sa.Column('transaction_type', sa.String(length=50), nullable=False),
        sa.Column('quantity_change', sa.Float(), nullable=False),
        sa.Column('quantity_before', sa.Float(), nullable=False),
        sa.Column('quantity_after', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('reference_type', sa.String(length=50), nullable=True),
        sa.Column('reference_id', sa.Integer(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_inventory_transactions_id', 'inventory_transactions', ['id'])
    op.create_index('ix_inventory_transactions_item_id', 'inventory_transactions', ['inventory_item_id'])
    op.create_index('ix_inventory_transactions_created_at', 'inventory_transactions', ['created_at'])
    op.create_index('ix_inventory_transactions_transaction_type', 'inventory_transactions', ['transaction_type'])


def downgrade():
    op.drop_index('ix_inventory_transactions_transaction_type', 'inventory_transactions')
    op.drop_index('ix_inventory_transactions_created_at', 'inventory_transactions')
    op.drop_index('ix_inventory_transactions_item_id', 'inventory_transactions')
    op.drop_index('ix_inventory_transactions_id', 'inventory_transactions')
    op.drop_table('inventory_transactions')
    
    op.drop_index('ix_batch_ingredients_inventory_item_id', 'batch_ingredients')
    op.drop_index('ix_batch_ingredients_batch_id', 'batch_ingredients')
    op.drop_index('ix_batch_ingredients_id', 'batch_ingredients')
    op.drop_table('batch_ingredients')
