"""add beerxml fields to ingredient models

Revision ID: add_beerxml_fields
Revises: 84e86493f0d8
Create Date: 2025-11-08

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_beerxml_fields'
down_revision = '84e86493f0d8'
branch_labels = None
depends_on = None


def upgrade():
    # Add BeerXML fields to recipe_hops table
    with op.batch_alter_table('recipe_hops', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('substitutes', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('humulene', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('caryophyllene', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('cohumulone', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('myrcene', sa.Float(), nullable=True))

    # Add BeerXML fields to recipe_fermentables table
    with op.batch_alter_table('recipe_fermentables', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('add_after_boil', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('coarse_fine_diff', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('moisture', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('diastatic_power', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('protein', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('max_in_batch', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('recommend_mash', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('ibu_gal_per_lb', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('display_amount', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('inventory', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('display_color', sa.String(), nullable=True))

    # Add BeerXML fields to recipe_yeasts table
    with op.batch_alter_table('recipe_yeasts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('display_amount', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('disp_min_temp', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('disp_max_temp', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('inventory', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('culture_date', sa.String(), nullable=True))

    # Update recipe_miscs table - change types from Integer to Float and add version
    with op.batch_alter_table('recipe_miscs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('version', sa.Integer(), nullable=True))
        # Note: Changing column types from Integer to Float
        # This will be handled by altering the existing columns
        batch_op.alter_column('amount',
                              existing_type=sa.Integer(),
                              type_=sa.Float(),
                              existing_nullable=True)
        batch_op.alter_column('time',
                              existing_type=sa.Integer(),
                              type_=sa.Float(),
                              existing_nullable=True)
        batch_op.alter_column('inventory',
                              existing_type=sa.Integer(),
                              type_=sa.String(),
                              existing_nullable=True)
        batch_op.alter_column('batch_size',
                              existing_type=sa.Integer(),
                              type_=sa.Float(),
                              existing_nullable=True)


def downgrade():
    # Remove BeerXML fields from recipe_miscs table
    with op.batch_alter_table('recipe_miscs', schema=None) as batch_op:
        batch_op.drop_column('version')
        batch_op.alter_column('batch_size',
                              existing_type=sa.Float(),
                              type_=sa.Integer(),
                              existing_nullable=True)
        batch_op.alter_column('inventory',
                              existing_type=sa.String(),
                              type_=sa.Integer(),
                              existing_nullable=True)
        batch_op.alter_column('time',
                              existing_type=sa.Float(),
                              type_=sa.Integer(),
                              existing_nullable=True)
        batch_op.alter_column('amount',
                              existing_type=sa.Float(),
                              type_=sa.Integer(),
                              existing_nullable=True)

    # Remove BeerXML fields from recipe_yeasts table
    with op.batch_alter_table('recipe_yeasts', schema=None) as batch_op:
        batch_op.drop_column('culture_date')
        batch_op.drop_column('inventory')
        batch_op.drop_column('disp_max_temp')
        batch_op.drop_column('disp_min_temp')
        batch_op.drop_column('display_amount')
        batch_op.drop_column('version')

    # Remove BeerXML fields from recipe_fermentables table
    with op.batch_alter_table('recipe_fermentables', schema=None) as batch_op:
        batch_op.drop_column('display_color')
        batch_op.drop_column('inventory')
        batch_op.drop_column('display_amount')
        batch_op.drop_column('ibu_gal_per_lb')
        batch_op.drop_column('recommend_mash')
        batch_op.drop_column('max_in_batch')
        batch_op.drop_column('protein')
        batch_op.drop_column('diastatic_power')
        batch_op.drop_column('moisture')
        batch_op.drop_column('coarse_fine_diff')
        batch_op.drop_column('add_after_boil')
        batch_op.drop_column('version')

    # Remove BeerXML fields from recipe_hops table
    with op.batch_alter_table('recipe_hops', schema=None) as batch_op:
        batch_op.drop_column('myrcene')
        batch_op.drop_column('cohumulone')
        batch_op.drop_column('caryophyllene')
        batch_op.drop_column('humulene')
        batch_op.drop_column('substitutes')
        batch_op.drop_column('version')
