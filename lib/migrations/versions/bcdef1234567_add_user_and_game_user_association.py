"""add user table, user_id to reviews, and game_user association table

Revision ID: bcdef1234567
Revises: a28af33e6866
Create Date: 2024-06-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bcdef1234567'
down_revision = 'a28af33e6866'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
    )
    with op.batch_alter_table('reviews') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_reviews_user_id_users',
            'users',
            ['user_id'], ['id']
        )
    op.create_table('game_users',
        sa.Column('game_id', sa.Integer(), sa.ForeignKey('games.id'), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
    )

def downgrade() -> None:
    op.drop_table('game_users')
    with op.batch_alter_table('reviews') as batch_op:
        batch_op.drop_constraint('fk_reviews_user_id_users', type_='foreignkey')
        batch_op.drop_column('user_id')
    op.drop_table('users')
