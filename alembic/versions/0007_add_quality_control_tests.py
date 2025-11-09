"""Add quality control tests table

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add quality_control_tests table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    
    # Check if table already exists
    if "quality_control_tests" not in inspector.get_table_names():
        op.create_table(
            "quality_control_tests",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("batch_id", sa.Integer(), nullable=False),
            sa.Column("test_date", sa.DateTime(), nullable=False),
            sa.Column("final_gravity", sa.Float(), nullable=True),
            sa.Column("abv_actual", sa.Float(), nullable=True),
            sa.Column("color", sa.String(length=50), nullable=True),
            sa.Column("clarity", sa.String(length=50), nullable=True),
            sa.Column("taste_notes", sa.Text(), nullable=True),
            sa.Column("aroma_notes", sa.Text(), nullable=True),
            sa.Column("appearance_notes", sa.Text(), nullable=True),
            sa.Column("flavor_notes", sa.Text(), nullable=True),
            sa.Column("mouthfeel_notes", sa.Text(), nullable=True),
            sa.Column("score", sa.Float(), nullable=True),
            sa.Column("aroma_score", sa.Float(), nullable=True),
            sa.Column("appearance_score", sa.Float(), nullable=True),
            sa.Column("flavor_score", sa.Float(), nullable=True),
            sa.Column("mouthfeel_score", sa.Float(), nullable=True),
            sa.Column("overall_impression_score", sa.Float(), nullable=True),
            sa.Column("photo_path", sa.String(length=500), nullable=True),
            sa.Column("tester_name", sa.String(length=100), nullable=True),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(
                ["batch_id"],
                ["batches.id"],
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            "ix_quality_control_tests_id",
            "quality_control_tests",
            ["id"],
            unique=False,
        )
        op.create_index(
            "ix_qc_tests_batch_id",
            "quality_control_tests",
            ["batch_id"],
            unique=False,
        )
        op.create_index(
            "ix_qc_tests_test_date",
            "quality_control_tests",
            ["test_date"],
            unique=False,
        )
        print("✓ Created quality_control_tests table")
    else:
        print("✓ quality_control_tests table already exists")


def downgrade() -> None:
    """Remove quality_control_tests table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    
    if "quality_control_tests" in inspector.get_table_names():
        op.drop_index("ix_qc_tests_test_date", table_name="quality_control_tests")
        op.drop_index("ix_qc_tests_batch_id", table_name="quality_control_tests")
        op.drop_index("ix_quality_control_tests_id", table_name="quality_control_tests")
        op.drop_table("quality_control_tests")
        print("✓ Dropped quality_control_tests table")
    else:
        print("✓ quality_control_tests table does not exist")
