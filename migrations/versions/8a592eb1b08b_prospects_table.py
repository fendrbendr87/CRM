"""Prospects table

Revision ID: 8a592eb1b08b
Revises: 99dc802550e7
Create Date: 2018-10-19 22:16:15.094879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a592eb1b08b'
down_revision = '99dc802550e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prospects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('phone_cell', sa.Integer(), nullable=True),
    sa.Column('user_account_pk', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_account_pk'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prospects')
    # ### end Alembic commands ###
