"""Add temperature controller integration fields

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-08 17:30:00.000000

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
    """Add fields for temperature controller integration"""
    
    # Add device_id and source to fermentation_readings
    op.add_column('fermentation_readings', sa.Column(
        'device_id', sa.Integer, nullable=True))
    op.add_column('fermentation_readings', sa.Column(
        'source', sa.String(50), nullable=True, server_default='manual'))
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_fermentation_readings_device_id',
        'fermentation_readings', 'devices',
        ['device_id'], ['id'],
        ondelete='SET NULL'
    )
    
    # Add index for device_id lookups
    op.create_index('ix_fermentation_readings_device_id',
                    'fermentation_readings', ['device_id'])
    
    # Add batch_id to devices for device-to-batch association
    op.add_column('devices', sa.Column(
        'batch_id', sa.Integer, nullable=True))
    op.create_foreign_key(
        'fk_devices_batch_id',
        'devices', 'batches',
        ['batch_id'], ['id'],
        ondelete='SET NULL'
    )
    op.create_index('ix_devices_batch_id', 'devices', ['batch_id'])
    
    # Add alert configuration to devices
    op.add_column('devices', sa.Column(
        'alert_config', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Add auto-import settings
    op.add_column('devices', sa.Column(
        'auto_import_enabled', sa.Boolean, default=True, nullable=False, server_default='true'))
    op.add_column('devices', sa.Column(
        'import_interval_seconds', sa.Integer, default=900, nullable=False, server_default='900'))
    op.add_column('devices', sa.Column(
        'last_import_at', sa.DateTime(timezone=True), nullable=True))
    
    # Add manual override flag
    op.add_column('devices', sa.Column(
        'manual_override', sa.Boolean, default=False, nullable=False, server_default='false'))


def downgrade() -> None:
    """Remove temperature controller integration fields"""
    
    # Remove device fields
    op.drop_column('devices', 'manual_override')
    op.drop_column('devices', 'last_import_at')
    op.drop_column('devices', 'import_interval_seconds')
    op.drop_column('devices', 'auto_import_enabled')
    op.drop_column('devices', 'alert_config')
    op.drop_index('ix_devices_batch_id', 'devices')
    op.drop_constraint('fk_devices_batch_id', 'devices', type_='foreignkey')
    op.drop_column('devices', 'batch_id')
    
    # Remove fermentation_readings fields
    op.drop_index('ix_fermentation_readings_device_id', 'fermentation_readings')
    op.drop_constraint('fk_fermentation_readings_device_id', 'fermentation_readings', type_='foreignkey')
    op.drop_column('fermentation_readings', 'source')
    op.drop_column('fermentation_readings', 'device_id')
