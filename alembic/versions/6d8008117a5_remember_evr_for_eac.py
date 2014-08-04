"""Remember evr for each build

Revision ID: 6d8008117a5
Revises: 2144a94d8b4b
Create Date: 2014-08-04 14:25:57.853078

"""

# revision identifiers, used by Alembic.
revision = '6d8008117a5'
down_revision = '2144a94d8b4b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('build', sa.Column('release', sa.String(), nullable=True))
    op.add_column('build', sa.Column('epoch', sa.Integer(), nullable=True))
    op.add_column('build', sa.Column('version', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('build', 'version')
    op.drop_column('build', 'epoch')
    op.drop_column('build', 'release')
    ### end Alembic commands ###
