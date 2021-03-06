"""'收藏表'

Revision ID: a352daed5e31
Revises: cd4e9a614fc5
Create Date: 2017-11-20 00:42:10.460695

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a352daed5e31'
down_revision = 'cd4e9a614fc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('png_collect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('png_id', sa.Integer(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('user', 'status',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               existing_server_default=sa.text("'1'"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'status',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               existing_server_default=sa.text("'1'"))
    op.drop_table('png_collect')
    # ### end Alembic commands ###
