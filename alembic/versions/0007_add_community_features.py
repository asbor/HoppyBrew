"""Add community features for recipe sharing

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-09 12:00:00.000000

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
    """Add community features: ratings, comments, stars, and user profiles"""
    
    # Add new fields to users table for profile
    op.add_column('user', sa.Column('bio', sa.Text, nullable=True))
    op.add_column('user', sa.Column('avatar_url', sa.String(500), nullable=True))
    op.add_column('user', sa.Column('website', sa.String(500), nullable=True))
    op.add_column('user', sa.Column('location', sa.String(200), nullable=True))
    
    # Add new fields to recipes table
    op.add_column('recipes', sa.Column('user_id', sa.Integer, nullable=True))
    op.add_column('recipes', sa.Column(
        'visibility',
        sa.Enum('private', 'public', 'unlisted', name='recipevisibility'),
        nullable=False,
        server_default='private'
    ))
    op.add_column('recipes', sa.Column(
        'created_at',
        sa.DateTime(timezone=True),
        server_default=sa.text('CURRENT_TIMESTAMP'),
        nullable=True
    ))
    op.add_column('recipes', sa.Column(
        'updated_at',
        sa.DateTime(timezone=True),
        server_default=sa.text('CURRENT_TIMESTAMP'),
        nullable=True
    ))
    
    # Add foreign key for recipe ownership
    op.create_foreign_key(
        'fk_recipes_user_id',
        'recipes', 'user',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    
    # Add indexes for recipes
    op.create_index('ix_recipes_user_id', 'recipes', ['user_id'])
    op.create_index('ix_recipes_visibility', 'recipes', ['visibility'])
    
    # Create recipe_ratings table
    op.create_table(
        'recipe_ratings',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('recipe_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('rating', sa.Float, nullable=False),
        sa.Column('review_text', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    )
    
    # Add indexes for recipe_ratings
    op.create_index('ix_recipe_ratings_recipe_id', 'recipe_ratings', ['recipe_id'])
    op.create_index('ix_recipe_ratings_user_id', 'recipe_ratings', ['user_id'])
    op.create_index('ix_recipe_ratings_user_recipe', 'recipe_ratings', ['user_id', 'recipe_id'], unique=True)
    
    # Create recipe_comments table
    op.create_table(
        'recipe_comments',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('recipe_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('parent_id', sa.Integer, nullable=True),
        sa.Column('comment_text', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['recipe_comments.id'], ondelete='CASCADE'),
    )
    
    # Add indexes for recipe_comments
    op.create_index('ix_recipe_comments_recipe_id', 'recipe_comments', ['recipe_id'])
    op.create_index('ix_recipe_comments_user_id', 'recipe_comments', ['user_id'])
    op.create_index('ix_recipe_comments_parent_id', 'recipe_comments', ['parent_id'])
    
    # Create recipe_stars table
    op.create_table(
        'recipe_stars',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('recipe_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    )
    
    # Add indexes for recipe_stars
    op.create_index('ix_recipe_stars_recipe_id', 'recipe_stars', ['recipe_id'])
    op.create_index('ix_recipe_stars_user_id', 'recipe_stars', ['user_id'])
    op.create_index('ix_recipe_stars_user_recipe', 'recipe_stars', ['user_id', 'recipe_id'], unique=True)


def downgrade() -> None:
    """Remove community features"""
    
    # Drop recipe_stars table
    op.drop_index('ix_recipe_stars_user_recipe', 'recipe_stars')
    op.drop_index('ix_recipe_stars_user_id', 'recipe_stars')
    op.drop_index('ix_recipe_stars_recipe_id', 'recipe_stars')
    op.drop_table('recipe_stars')
    
    # Drop recipe_comments table
    op.drop_index('ix_recipe_comments_parent_id', 'recipe_comments')
    op.drop_index('ix_recipe_comments_user_id', 'recipe_comments')
    op.drop_index('ix_recipe_comments_recipe_id', 'recipe_comments')
    op.drop_table('recipe_comments')
    
    # Drop recipe_ratings table
    op.drop_index('ix_recipe_ratings_user_recipe', 'recipe_ratings')
    op.drop_index('ix_recipe_ratings_user_id', 'recipe_ratings')
    op.drop_index('ix_recipe_ratings_recipe_id', 'recipe_ratings')
    op.drop_table('recipe_ratings')
    
    # Drop indexes from recipes table
    op.drop_index('ix_recipes_visibility', 'recipes')
    op.drop_index('ix_recipes_user_id', 'recipes')
    
    # Drop foreign key from recipes table
    op.drop_constraint('fk_recipes_user_id', 'recipes', type_='foreignkey')
    
    # Drop columns from recipes table
    op.drop_column('recipes', 'updated_at')
    op.drop_column('recipes', 'created_at')
    op.drop_column('recipes', 'visibility')
    op.drop_column('recipes', 'user_id')
    
    # Drop enum type
    op.execute('DROP TYPE recipevisibility')
    
    # Drop columns from user table
    op.drop_column('user', 'location')
    op.drop_column('user', 'website')
    op.drop_column('user', 'avatar_url')
    op.drop_column('user', 'bio')
