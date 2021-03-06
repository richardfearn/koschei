"""Add collection.pkgdb_branch

Revision ID: 49889794b4d7
Revises: 515f0581e6f7
Create Date: 2016-03-11 15:34:48.148939

"""

# revision identifiers, used by Alembic.
revision = '49889794b4d7'
down_revision = '515f0581e6f7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collection', sa.Column('branch', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('collection', 'branch')
    ### end Alembic commands ###
