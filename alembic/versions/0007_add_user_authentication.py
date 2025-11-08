"""Add user authentication and authorization tables

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create user table with authentication fields"""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    # Check if table already exists
    if 'user' not in inspector.get_table_names():
        op.create_table(
            'user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=50), nullable=False),
            sa.Column('email', sa.String(length=100), nullable=False),
            sa.Column('password', sa.String(), nullable=True),  # Kept for backwards compatibility
            sa.Column('hashed_password', sa.String(length=255), nullable=True),
            sa.Column('first_name', sa.String(), nullable=True),
            sa.Column('last_name', sa.String(), nullable=True),
            sa.Column('role', sa.Enum('admin', 'brewer', 'viewer', name='userrole'), nullable=False, server_default='viewer'),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
            sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        
        # Create indexes
        op.create_index('ix_user_id', 'user', ['id'], unique=False)
        op.create_index('ix_user_username', 'user', ['username'], unique=True)
        op.create_index('ix_user_email', 'user', ['email'], unique=True)
    else:
        # Table exists, check and add missing columns
        existing_columns = [col['name'] for col in inspector.get_columns('user')]
        
        if 'hashed_password' not in existing_columns:
            op.add_column('user', sa.Column('hashed_password', sa.String(length=255), nullable=True))
        
        if 'role' not in existing_columns:
            # Create enum type if it doesn't exist (PostgreSQL)
            try:
                op.execute("CREATE TYPE userrole AS ENUM ('admin', 'brewer', 'viewer')")
            except:
                pass  # Type might already exist or we're using SQLite
            
            op.add_column('user', sa.Column('role', sa.Enum('admin', 'brewer', 'viewer', name='userrole'), nullable=False, server_default='viewer'))
        
        if 'is_active' not in existing_columns:
            op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'))
        
        if 'is_verified' not in existing_columns:
            op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='0'))
        
        if 'created_at' not in existing_columns:
            op.add_column('user', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
        
        if 'updated_at' not in existing_columns:
            op.add_column('user', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
        
        # Ensure indexes exist
        existing_indexes = [idx['name'] for idx in inspector.get_indexes('user')]
        
        if 'ix_user_username' not in existing_indexes:
            try:
                op.create_index('ix_user_username', 'user', ['username'], unique=True)
            except:
                pass  # Index might already exist
        
        if 'ix_user_email' not in existing_indexes:
            try:
                op.create_index('ix_user_email', 'user', ['email'], unique=True)
            except:
                pass  # Index might already exist


def downgrade() -> None:
    """Drop user table"""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    if 'user' in inspector.get_table_names():
        op.drop_index('ix_user_email', table_name='user')
        op.drop_index('ix_user_username', table_name='user')
        op.drop_index('ix_user_id', table_name='user')
        op.drop_table('user')
        
        # Drop enum type for PostgreSQL
        try:
            op.execute("DROP TYPE IF EXISTS userrole")
        except:
            pass  # We're using SQLite or type doesn't exist
