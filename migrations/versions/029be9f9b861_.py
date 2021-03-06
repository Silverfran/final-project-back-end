"""empty message

Revision ID: 029be9f9b861
Revises: a0695d2d861d
Create Date: 2020-05-08 20:33:45.917105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '029be9f9b861'
down_revision = 'a0695d2d861d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    # ### end Alembic commands ###
