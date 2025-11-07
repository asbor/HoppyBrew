"""Add comprehensive beer styles tables

Revision ID: 0002
Revises: 0001
Create Date: 2025-11-06 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, Text, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.exc import OperationalError, ProgrammingError


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    """Create new beer style management tables"""
    
    # Check if tables already exist (they might have been created by 0001_initial)
    # This allows the migration to be idempotent
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Create style_guideline_sources table only if it doesn't exist
    if 'style_guideline_sources' not in existing_tables:
        op.create_table(
            'style_guideline_sources',
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('name', String(255), nullable=False),
            Column('year', Integer, nullable=True),
            Column('abbreviation', String(20), nullable=True),
            Column('description', Text, nullable=True),
            Column('is_active', Boolean, default=True),
            Column('created_at', DateTime(timezone=True), server_default=sa.func.now()),
            Column('updated_at', DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        )
        
        # Create indexes on style_guideline_sources
        op.create_index('idx_guideline_source_name', 'style_guideline_sources', ['name'])
        op.create_index('idx_guideline_source_active', 'style_guideline_sources', ['is_active'])
    
    # Create style_categories table only if it doesn't exist
    if 'style_categories' not in existing_tables:
        op.create_table(
            'style_categories',
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('guideline_source_id', Integer, ForeignKey('style_guideline_sources.id'), nullable=False),
            Column('name', String(255), nullable=False),
            Column('code', String(20), nullable=True),
            Column('description', Text, nullable=True),
            Column('parent_category_id', Integer, ForeignKey('style_categories.id'), nullable=True),
        )
        
        # Create indexes on style_categories
        op.create_index('idx_category_guideline', 'style_categories', ['guideline_source_id'])
        op.create_index('idx_category_parent', 'style_categories', ['parent_category_id'])
        op.create_index('idx_category_code', 'style_categories', ['code'])
    
    # Create beer_styles table only if it doesn't exist
    if 'beer_styles' not in existing_tables:
        op.create_table(
            'beer_styles',
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('guideline_source_id', Integer, ForeignKey('style_guideline_sources.id'), nullable=True),
            Column('category_id', Integer, ForeignKey('style_categories.id'), nullable=True),
            Column('name', String(255), nullable=False),
            Column('style_code', String(20), nullable=True),
            Column('subcategory', String(100), nullable=True),
            
            # Basic Parameters
            Column('abv_min', Numeric(4, 2), nullable=True),
            Column('abv_max', Numeric(4, 2), nullable=True),
            Column('og_min', Numeric(5, 3), nullable=True),
            Column('og_max', Numeric(5, 3), nullable=True),
            Column('fg_min', Numeric(5, 3), nullable=True),
            Column('fg_max', Numeric(5, 3), nullable=True),
            Column('ibu_min', Integer, nullable=True),
            Column('ibu_max', Integer, nullable=True),
            Column('color_min_ebc', Numeric(6, 2), nullable=True),
            Column('color_max_ebc', Numeric(6, 2), nullable=True),
            Column('color_min_srm', Numeric(6, 2), nullable=True),
            Column('color_max_srm', Numeric(6, 2), nullable=True),
            
            # Detailed Descriptions
            Column('description', Text, nullable=True),
            Column('aroma', Text, nullable=True),
            Column('appearance', Text, nullable=True),
            Column('flavor', Text, nullable=True),
            Column('mouthfeel', Text, nullable=True),
            Column('overall_impression', Text, nullable=True),
            Column('comments', Text, nullable=True),
            Column('history', Text, nullable=True),
            Column('ingredients', Text, nullable=True),
            Column('comparison', Text, nullable=True),
            Column('examples', Text, nullable=True),
            
            # Metadata
            Column('is_custom', Boolean, default=False),
            Column('created_by', Integer, nullable=True),
            Column('created_at', DateTime(timezone=True), server_default=sa.func.now()),
            Column('updated_at', DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        )
        
        # Create indexes on beer_styles
        op.create_index('idx_beer_style_name', 'beer_styles', ['name'])
        op.create_index('idx_beer_style_code', 'beer_styles', ['style_code'])
        op.create_index('idx_beer_style_guideline', 'beer_styles', ['guideline_source_id'])
        op.create_index('idx_beer_style_category', 'beer_styles', ['category_id'])
        op.create_index('idx_beer_style_custom', 'beer_styles', ['is_custom'])
        op.create_index('idx_beer_style_abv', 'beer_styles', ['abv_min', 'abv_max'])
        op.create_index('idx_beer_style_ibu', 'beer_styles', ['ibu_min', 'ibu_max'])


def downgrade():
    """Drop beer style management tables"""
    
    # Check if tables exist before dropping
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Drop beer_styles table and its indexes if they exist
    if 'beer_styles' in existing_tables:
        # Drop indexes first (if they exist)
        try:
            op.drop_index('idx_beer_style_ibu', 'beer_styles')
            op.drop_index('idx_beer_style_abv', 'beer_styles')
            op.drop_index('idx_beer_style_custom', 'beer_styles')
            op.drop_index('idx_beer_style_category', 'beer_styles')
            op.drop_index('idx_beer_style_guideline', 'beer_styles')
            op.drop_index('idx_beer_style_code', 'beer_styles')
            op.drop_index('idx_beer_style_name', 'beer_styles')
        except (OperationalError, ProgrammingError):
            pass  # Indexes might not exist
        
        op.drop_table('beer_styles')
    
    # Drop style_categories table and its indexes if they exist
    if 'style_categories' in existing_tables:
        try:
            op.drop_index('idx_category_code', 'style_categories')
            op.drop_index('idx_category_parent', 'style_categories')
            op.drop_index('idx_category_guideline', 'style_categories')
        except (OperationalError, ProgrammingError):
            pass  # Indexes might not exist
        
        op.drop_table('style_categories')
    
    # Drop style_guideline_sources table and its indexes if they exist
    if 'style_guideline_sources' in existing_tables:
        try:
            op.drop_index('idx_guideline_source_active', 'style_guideline_sources')
            op.drop_index('idx_guideline_source_name', 'style_guideline_sources')
        except (OperationalError, ProgrammingError):
            pass  # Indexes might not exist
        
        op.drop_table('style_guideline_sources')
