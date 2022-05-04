"""Add new columns

Revision ID: 39454463a1b6
Revises: 684b0cbad63c
Create Date: 2022-04-29 11:46:27.076651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39454463a1b6'
down_revision = '684b0cbad63c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planet', sa.Column('distance_mil_miles', sa.String(), nullable=True))
    op.add_column('planet', sa.Column('planet_name', sa.String(), nullable=True))
    op.drop_column('planet', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('planet', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('planet', 'planet_name')
    op.drop_column('planet', 'distance_mil_miles')
    # ### end Alembic commands ###