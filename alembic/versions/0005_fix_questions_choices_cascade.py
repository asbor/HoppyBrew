"""Fix questions/choices FK constraints with CASCADE delete

Revision ID: 0005
Revises: 0004
Create Date: 2025-11-07 22:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add CASCADE delete to choices.question_id foreign key"""
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    
    # Check database dialect
    is_sqlite = connection.dialect.name == 'sqlite'

    if is_sqlite:
        # SQLite requires batch mode for FK alterations
        with op.batch_alter_table('choices', schema=None) as batch_op:
            # Get existing foreign keys
            existing_fks = inspector.get_foreign_keys('choices')
            question_fk_name = None

            for fk in existing_fks:
                if fk['constrained_columns'] == ['question_id']:
                    question_fk_name = fk['name']
                    break

            if question_fk_name:
                batch_op.drop_constraint(question_fk_name, type_='foreignkey')

            # Add foreign key constraint with CASCADE delete
            batch_op.create_foreign_key(
                'fk_choices_question_id',
                'questions',
                ['question_id'],
                ['id'],
                ondelete='CASCADE'
            )
    else:
        # PostgreSQL can alter constraints directly
        existing_fks = inspector.get_foreign_keys('choices')
        question_fk_name = None

        for fk in existing_fks:
            if fk['constrained_columns'] == ['question_id']:
                question_fk_name = fk['name']
                break

        if question_fk_name:
            # Drop existing foreign key constraint
            op.drop_constraint(question_fk_name, 'choices', type_='foreignkey')

        # Add foreign key constraint with CASCADE delete
        op.create_foreign_key(
            'fk_choices_question_id',
            'choices',
            'questions',
            ['question_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade() -> None:
    """Revert to standard FK constraint without CASCADE"""
    connection = op.get_bind()
    is_sqlite = connection.dialect.name == 'sqlite'
    
    if is_sqlite:
        # SQLite requires batch mode for FK alterations
        with op.batch_alter_table('choices', schema=None) as batch_op:
            # Drop CASCADE constraint
            batch_op.drop_constraint('fk_choices_question_id', type_='foreignkey')

            # Restore basic foreign key constraint
            batch_op.create_foreign_key(
                'choices_question_id_fkey',
                'questions',
                ['question_id'],
                ['id']
            )
    else:
        # PostgreSQL can alter constraints directly
        # Drop CASCADE constraint
        op.drop_constraint('fk_choices_question_id', 'choices', type_='foreignkey')

        # Restore basic foreign key constraint
        op.create_foreign_key(
            'choices_question_id_fkey',
            'choices',
            'questions',
            ['question_id'],
            ['id']
        )
