"""Added is_active field

Revision ID: 45d6757321b8
Revises: 4e5828fd695a
Create Date: 2024-11-11 13:59:36.433984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45d6757321b8'
down_revision = '4e5828fd695a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
