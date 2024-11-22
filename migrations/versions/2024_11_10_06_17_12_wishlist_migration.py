"""Wishlist migration

Revision ID: d9a67e9e5c53
Revises: 7ffad476533f
Create Date: 2024-11-10 06:17:12.177409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9a67e9e5c53'
down_revision = '7ffad476533f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wishlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('element', sa.String(length=50), nullable=False),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wishlist')
    # ### end Alembic commands ###
