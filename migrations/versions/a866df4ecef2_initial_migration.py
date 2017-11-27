"""initial migration

Revision ID: a866df4ecef2
Revises: 
Create Date: 2017-11-13 01:21:56.388721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a866df4ecef2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('png',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('_id', sa.String(length=64), nullable=True),
    sa.Column('bianhao', sa.String(length=64), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.Column('local_url', sa.String(length=128), nullable=True),
    sa.Column('cdn_url', sa.String(length=128), nullable=True),
    sa.Column('cat', sa.Integer(), nullable=True),
    sa.Column('cat_1', sa.Integer(), nullable=True),
    sa.Column('cat_2', sa.Integer(), nullable=True),
    sa.Column('dpi', sa.String(length=8), nullable=True),
    sa.Column('img', sa.String(length=64), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('down', sa.Integer(), nullable=True),
    sa.Column('fav', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(length=16), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('format', sa.String(length=4), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('attr', sa.String(length=128), nullable=True),
    sa.Column('is_spider', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('_id'),
    sa.UniqueConstraint('bianhao')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('png')
    # ### end Alembic commands ###
