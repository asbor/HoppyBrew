"""Add device integration fields

Revision ID: 0008
Revises: 0007
Create Date: 2025-11-11 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add device integration fields for temperature control"""
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    
    # Get existing columns
    existing_fr_columns = [col['name'] for col in inspector.get_columns('fermentation_readings')]
    existing_device_columns = [col['name'] for col in inspector.get_columns('devices')]
    
    # Add device_id to fermentation_readings to track which device created the reading
    if 'device_id' not in existing_fr_columns:
        op.add_column('fermentation_readings', sa.Column(
            'device_id', sa.Integer, sa.ForeignKey('devices.id', ondelete='SET NULL'), nullable=True))
    
    # Add source field to indicate if reading was manual or automatic
    if 'source' not in existing_fr_columns:
        op.add_column('fermentation_readings', sa.Column(
            'source', sa.String(50), nullable=True, server_default='manual'))
    
    # Add alert configuration to devices
    if 'alert_config' not in existing_device_columns:
        op.add_column('devices', sa.Column(
            'alert_config', sa.JSON, nullable=True))
    
    # Add batch_id to devices to link device to active batch
    if 'batch_id' not in existing_device_columns:
        op.add_column('devices', sa.Column(
            'batch_id', sa.Integer, sa.ForeignKey('batches.id', ondelete='SET NULL'), nullable=True))
    
    # Add last_reading_at to track when device last reported
    if 'last_reading_at' not in existing_device_columns:
        op.add_column('devices', sa.Column(
            'last_reading_at', sa.DateTime, nullable=True))
    
    # Add indexes for better query performance
    existing_indexes = [idx['name'] for idx in inspector.get_indexes('fermentation_readings')]
    if 'ix_fermentation_readings_device_id' not in existing_indexes:
        op.create_index('ix_fermentation_readings_device_id',
                       'fermentation_readings', ['device_id'])
    
    if 'ix_fermentation_readings_source' not in existing_indexes:
        op.create_index('ix_fermentation_readings_source',
                       'fermentation_readings', ['source'])


def downgrade() -> None:
    """Remove device integration fields"""
    op.drop_index('ix_fermentation_readings_source', 'fermentation_readings')
    op.drop_index('ix_fermentation_readings_device_id', 'fermentation_readings')
    op.drop_column('devices', 'last_reading_at')
    op.drop_column('devices', 'batch_id')
    op.drop_column('devices', 'alert_config')
    op.drop_column('fermentation_readings', 'source')
    op.drop_column('fermentation_readings', 'device_id')
