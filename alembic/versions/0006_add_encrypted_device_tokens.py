"""Add encrypted storage for device API tokens

Revision ID: 0006
Revises: 0005
Create Date: 2025-11-07 22:25:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add encrypted token storage and deprecate plaintext api_token"""
    # Add new encrypted token field
    op.add_column('devices', sa.Column(
        'api_token_encrypted', sa.Text, nullable=True))
    op.add_column('devices', sa.Column(
        'token_salt', sa.String(64), nullable=True))

    # Add index for better performance on token lookups
    op.create_index('idx_devices_token_encrypted',
                    'devices', ['api_token_encrypted'])

    # Note: In production, you would:
    # 1. Migrate existing api_token values to encrypted storage
    # 2. Clear plaintext api_token values after migration
    # 3. Eventually drop the api_token column


def downgrade() -> None:
    """Remove encrypted token storage"""
    op.drop_index('idx_devices_token_encrypted', 'devices')
    op.drop_column('devices', 'token_salt')
    op.drop_column('devices', 'api_token_encrypted')
