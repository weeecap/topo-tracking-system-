"""initial

Revision ID: 77b45d8adf84
Revises: 
Create Date: 2025-11-06 13:26:03.326574

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '77b45d8adf84'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Create Enums first ###
    userrole_enum = postgresql.ENUM('cartographer', 'validator', 'admin', 'superuser', name='userrole', create_type=False)
    userrole_enum.create(op.get_bind(), checkfirst=True)
    
    taskstatus_enum = postgresql.ENUM('TODO', 'in_progress', 'review', 'done', name='taskstatus', create_type=False)
    taskstatus_enum.create(op.get_bind(), checkfirst=True)

    # ### Create tables in correct order ###
    
    # 1. First independent table: forms
    op.create_table('forms',
        sa.Column('form_id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('form_id')
    )
    op.create_index('ix_forms_form_id', 'forms', ['form_id'], unique=False)

    # 2. Second independent table: users
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('surname', sa.String(length=50), nullable=False),
        sa.Column('role', userrole_enum, nullable=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('is_user', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('is_super_admin', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)

    # 3. Finally dependent table: tasks (depends on forms and users)
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('status', taskstatus_enum, server_default='TODO', nullable=False),
        sa.Column('priority', sa.Integer(), server_default='1', nullable=False),
        sa.Column('assignee_id', sa.Integer(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
        sa.Column('form_id', sa.Integer(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['form_id'], ['forms.form_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)


def downgrade() -> None:
    # ### Drop tables in reverse order ###
    op.drop_index('ix_tasks_id', table_name='tasks')
    op.drop_table('tasks')
    
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    
    op.drop_index('ix_forms_form_id', table_name='forms')
    op.drop_table('forms')
    
    # ### Drop Enums ###
    op.execute('DROP TYPE IF EXISTS taskstatus')
    op.execute('DROP TYPE IF EXISTS userrole')
