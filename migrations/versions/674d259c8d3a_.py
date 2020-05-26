"""empty message

Revision ID: 674d259c8d3a
Revises: f72d08b97572
Create Date: 2020-05-26 06:48:37.967370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '674d259c8d3a'
down_revision = 'f72d08b97572'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packages', sa.Column('url', sa.String(length=480), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('packages', 'url')
    # ### end Alembic commands ###