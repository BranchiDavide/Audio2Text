"""Added additional attributes to transcription

Revision ID: 7694b094af6a
Revises: a6227f7ed900
Create Date: 2024-11-24 22:08:26.412219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7694b094af6a'
down_revision = 'a6227f7ed900'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transcription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('detected_lang', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('model', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('transcription_time', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transcription', schema=None) as batch_op:
        batch_op.drop_column('transcription_time')
        batch_op.drop_column('model')
        batch_op.drop_column('detected_lang')

    # ### end Alembic commands ###