"""empty message

Revision ID: 178e9c208218
Revises: 5998e9ee193
Create Date: 2014-11-16 19:09:06.666542

"""

# revision identifiers, used by Alembic.
revision = '178e9c208218'
down_revision = '5998e9ee193'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('issues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('closer_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pullrequests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('issue_id', sa.Integer(), nullable=True),
    sa.Column('origin_project_id', sa.Integer(), nullable=True),
    sa.Column('origin_project_ref', sa.String(length=1024), nullable=True),
    sa.Column('upstream_project_id', sa.Integer(), nullable=True),
    sa.Column('upstream_project_ref', sa.String(length=1024), nullable=True),
    sa.Column('origin_commit_sha', sa.String(length=40), nullable=True),
    sa.Column('upstream_commit_sha', sa.String(length=40), nullable=True),
    sa.Column('merged_commit_sha', sa.String(length=40), nullable=True),
    sa.Column('merger_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('merged_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'users', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users')
    op.drop_table('pullrequests')
    op.drop_table('issues')
    ### end Alembic commands ###
