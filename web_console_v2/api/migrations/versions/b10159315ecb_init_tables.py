"""init tables

Revision ID: b10159315ecb
Revises: 
Create Date: 2021-01-10 22:25:00.518665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b10159315ecb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects_v2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.Column('config', sa.Text(), nullable=True),
    sa.Column('certificate', sa.Text(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_v2_name'), 'projects_v2', ['name'], unique=True)
    op.create_index(op.f('ix_projects_v2_token'), 'projects_v2', ['token'], unique=False)
    op.create_table('template_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('group_alias', sa.String(length=255), nullable=False),
    sa.Column('config', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_template_v2_group_alias'), 'template_v2', ['group_alias'], unique=False)
    op.create_index(op.f('ix_template_v2_name'), 'template_v2', ['name'], unique=True)
    op.create_table('users_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_v2_username'), 'users_v2', ['username'], unique=False)
    op.create_table('workflow_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('config', sa.Text(), nullable=True),
    sa.Column('forkable', sa.Boolean(), nullable=True),
    sa.Column('forked_from', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('state', sa.Enum('INVALID', 'NEW', 'READY', 'RUNNING', 'STOPPED', name='workflowstate'), nullable=True),
    sa.Column('target_state', sa.Enum('INVALID', 'NEW', 'READY', 'RUNNING', 'STOPPED', name='workflowstate'), nullable=True),
    sa.Column('transaction_state', sa.Enum('READY', 'ABORTED', 'COORDINATOR_PREPARE', 'COORDINATOR_COMMITTABLE', 'COORDINATOR_COMMITTING', 'COORDINATOR_ABORTING', 'PARTICIPANT_PREPARE', 'PARTICIPANT_COMMITTABLE', 'PARTICIPANT_COMMITTING', 'PARTICIPANT_ABORTING', name='transactionstate'), nullable=True),
    sa.Column('transaction_err', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects_v2.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_v2_name'), 'workflow_v2', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workflow_v2_name'), table_name='workflow_v2')
    op.drop_table('workflow_v2')
    op.drop_index(op.f('ix_users_v2_username'), table_name='users_v2')
    op.drop_table('users_v2')
    op.drop_index(op.f('ix_template_v2_name'), table_name='template_v2')
    op.drop_index(op.f('ix_template_v2_group_alias'), table_name='template_v2')
    op.drop_table('template_v2')
    op.drop_index(op.f('ix_projects_v2_token'), table_name='projects_v2')
    op.drop_index(op.f('ix_projects_v2_name'), table_name='projects_v2')
    op.drop_table('projects_v2')
    # ### end Alembic commands ###