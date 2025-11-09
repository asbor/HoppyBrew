"""add recipe community features

Revision ID: 0008_add_recipe_community
Revises: 0007_add_inventory_tracking
Create Date: 2025-11-09 12:07:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0008_add_recipe_community"
down_revision = "0007_add_inventory_tracking"
branch_labels = None
depends_on = None


def upgrade():
    # Add community features columns to recipes table
    op.add_column('recipes', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('recipes', sa.Column('is_public', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('recipes', sa.Column('forked_from_id', sa.Integer(), nullable=True))
    op.add_column('recipes', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('recipes', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    
    # Add foreign keys
    op.create_foreign_key('fk_recipes_user_id', 'recipes', 'user', ['user_id'], ['id'])
    op.create_foreign_key('fk_recipes_forked_from_id', 'recipes', 'recipes', ['forked_from_id'], ['id'])
    
    # Add indexes
    op.create_index('ix_recipes_user_id', 'recipes', ['user_id'])
    op.create_index('ix_recipes_is_public', 'recipes', ['is_public'])
    
    # Add profile columns to user table
    op.add_column('user', sa.Column('bio', sa.String(length=500), nullable=True))
    op.add_column('user', sa.Column('location', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('avatar_url', sa.String(length=255), nullable=True))
    
    # Create recipe_ratings table
    op.create_table(
        'recipe_ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('review_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_rating'),
    )
    op.create_index('ix_recipe_ratings_id', 'recipe_ratings', ['id'])
    op.create_index('ix_recipe_ratings_recipe_id', 'recipe_ratings', ['recipe_id'])
    op.create_index('ix_recipe_ratings_user_id', 'recipe_ratings', ['user_id'])
    
    # Create recipe_comments table
    op.create_table(
        'recipe_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('comment_text', sa.Text(), nullable=False),
        sa.Column('parent_comment_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_comment_id'], ['recipe_comments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_recipe_comments_id', 'recipe_comments', ['id'])
    op.create_index('ix_recipe_comments_recipe_id', 'recipe_comments', ['recipe_id'])
    op.create_index('ix_recipe_comments_user_id', 'recipe_comments', ['user_id'])
    op.create_index('ix_recipe_comments_parent_id', 'recipe_comments', ['parent_comment_id'])


def downgrade():
    # Drop tables
    op.drop_index('ix_recipe_comments_parent_id', 'recipe_comments')
    op.drop_index('ix_recipe_comments_user_id', 'recipe_comments')
    op.drop_index('ix_recipe_comments_recipe_id', 'recipe_comments')
    op.drop_index('ix_recipe_comments_id', 'recipe_comments')
    op.drop_table('recipe_comments')
    
    op.drop_index('ix_recipe_ratings_user_id', 'recipe_ratings')
    op.drop_index('ix_recipe_ratings_recipe_id', 'recipe_ratings')
    op.drop_index('ix_recipe_ratings_id', 'recipe_ratings')
    op.drop_table('recipe_ratings')
    
    # Remove user profile columns
    op.drop_column('user', 'avatar_url')
    op.drop_column('user', 'location')
    op.drop_column('user', 'bio')
    
    # Remove recipe community columns and indexes
    op.drop_index('ix_recipes_is_public', 'recipes')
    op.drop_index('ix_recipes_user_id', 'recipes')
    op.drop_constraint('fk_recipes_forked_from_id', 'recipes', type_='foreignkey')
    op.drop_constraint('fk_recipes_user_id', 'recipes', type_='foreignkey')
    op.drop_column('recipes', 'updated_at')
    op.drop_column('recipes', 'created_at')
    op.drop_column('recipes', 'forked_from_id')
    op.drop_column('recipes', 'is_public')
    op.drop_column('recipes', 'user_id')
