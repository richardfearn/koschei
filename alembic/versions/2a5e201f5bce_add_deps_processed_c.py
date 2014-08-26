"""Add deps_processed column to build

Revision ID: 2a5e201f5bce
Revises: 2c9d7b6afc9b
Create Date: 2014-08-25 23:46:45.472996

"""

# revision identifiers, used by Alembic.
revision = '2a5e201f5bce'
down_revision = '2c9d7b6afc9b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('build', sa.Column('deps_processed', sa.Boolean(), server_default='false', nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('build', 'deps_processed')
    ### end Alembic commands ###