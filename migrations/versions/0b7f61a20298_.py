"""empty message

Revision ID: 0b7f61a20298
Revises: 2e3a304af656
Create Date: 2019-03-16 23:08:28.044983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b7f61a20298'
down_revision = '2e3a304af656'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist')
    # ### end Alembic commands ###
