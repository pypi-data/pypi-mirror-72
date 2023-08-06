"""add to already existing app"""

revision = 'c69f3a6d8bea'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'googleplusauth_info',
        sa.Column('uid', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('registered', sa.Boolean(), default=False, nullable=False),
        sa.Column('just_connected', sa.Boolean(), default=False, nullable=False),
        sa.Column('profile_picture', sa.String(512), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('google_id', sa.Unicode(255), nullable=False),
        sa.Column('access_token', sa.UnicodeText, nullable=False),
        sa.Column('access_token_expiry', sa.DateTime(), nullable=False),
    )
    op.create_unique_constraint('uq_google_id', 'googleplusauth_info', ['google_id'])
    op.create_foreign_key('fk_user_google', 'googleplusauth_info', 'tg_user', ['user_id'], ['user_id'])

def downgrade():
    op.drop_table('googleplusauth_info')
