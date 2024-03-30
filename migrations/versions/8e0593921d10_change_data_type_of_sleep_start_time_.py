"""Change data type of sleep_start_time and sleep_end_time columns

Revision ID: 8e0593921d10
Revises: f85b5d8c58ed
Create Date: 2024-03-29 12:22:18.047932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e0593921d10'
down_revision = 'f85b5d8c58ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.alter_column('sleep_start_time',
               existing_type=sa.TIME(),
               type_=sa.DateTime(),
               existing_nullable=True)
        batch_op.alter_column('sleep_end_time',
               existing_type=sa.TIME(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('entry', schema=None) as batch_op:
        batch_op.alter_column('sleep_end_time',
               existing_type=sa.DateTime(),
               type_=sa.TIME(),
               existing_nullable=True)
        batch_op.alter_column('sleep_start_time',
               existing_type=sa.DateTime(),
               type_=sa.TIME(),
               existing_nullable=True)

    # ### end Alembic commands ###