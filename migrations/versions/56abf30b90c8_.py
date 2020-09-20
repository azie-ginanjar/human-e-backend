"""empty message

Revision ID: 56abf30b90c8
Revises: 
Create Date: 2020-09-20 16:01:35.545470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56abf30b90c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_v2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('business_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('marketplace_id', sa.String(), nullable=True),
    sa.Column('customer_id', sa.String(), nullable=True),
    sa.Column('has_active_subscription', sa.Boolean(), nullable=True),
    sa.Column('is_trialing', sa.String(), nullable=True),
    sa.Column('plan', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('epoch_created_at', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reset_token',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token_str', sa.String(), nullable=True),
    sa.Column('expiration_date', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_v2.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reset_token')
    op.drop_table('user_v2')
    # ### end Alembic commands ###