"""add oauth

Revision ID: 134b6ad70b5c
Revises: 44775f747bfe
Create Date: 2013-12-04 20:15:30.299940

"""

# revision identifiers, used by Alembic.
revision = '134b6ad70b5c'
down_revision = '44775f747bfe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oauth_clients',
    sa.Column('name', sa.Unicode(length=50), nullable=True),
    sa.Column('description', sa.Unicode(length=300), nullable=True),
    sa.Column('client_id', sa.Unicode(length=100), nullable=False),
    sa.Column('client_secret', sa.Unicode(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_confidential', sa.Boolean(), nullable=False),
    sa.Column('redirect_uri', sa.UnicodeText(), nullable=False),
    sa.Column('_default_scopes', sa.UnicodeText(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('client_id')
    )
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token_type', sa.Unicode(length=10), nullable=False),
    sa.Column('client_id', sa.Unicode(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('access_token', sa.Unicode(length=255), nullable=True),
    sa.Column('refresh_token', sa.Unicode(length=255), nullable=True),
    sa.Column('expires', sa.DateTime(timezone=True), nullable=False),
    sa.Column('_scopes', sa.UnicodeText(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['oauth_clients.client_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token'),
    sa.UniqueConstraint('refresh_token')
    )
    op.create_table('grants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Unicode(length=100), nullable=False),
    sa.Column('code', sa.Unicode(length=255), nullable=False),
    sa.Column('redirect_uri', sa.UnicodeText(), nullable=True),
    sa.Column('_scopes', sa.UnicodeText(), nullable=True),
    sa.Column('expires', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['oauth_clients.client_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grants')
    op.drop_table('tokens')
    op.drop_table('oauth_clients')
    ### end Alembic commands ###
