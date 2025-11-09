"""Add quality control tests table

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-09 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'quality_control_tests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.Integer(), nullable=False),
        sa.Column('test_date', sa.DateTime(), nullable=False),
        sa.Column('final_gravity', sa.Float(), nullable=True),
        sa.Column('abv_actual', sa.Float(), nullable=True),
        sa.Column('color', sa.String(length=100), nullable=True),
        sa.Column('clarity', sa.String(length=100), nullable=True),
        sa.Column('taste_notes', sa.Text(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('photo_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quality_control_tests_id'), 'quality_control_tests', ['id'], unique=False)
    op.create_index(op.f('ix_quality_control_tests_batch_id'), 'quality_control_tests', ['batch_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_quality_control_tests_batch_id'), table_name='quality_control_tests')
    op.drop_index(op.f('ix_quality_control_tests_id'), table_name='quality_control_tests')
    op.drop_table('quality_control_tests')
