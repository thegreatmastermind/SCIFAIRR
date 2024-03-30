"""Change data type of sleep_start_time and sleep_end_time columns to Time and delete all entries

Revision ID: a3e7263c42d1
Revises: 8e0593921d10
Create Date: 2024-03-30 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3e7263c42d1'
down_revision = '8e0593921d10'
branch_labels = None
depends_on = None


def upgrade():
    # Change data type of sleep_start_time and sleep_end_time columns to Time
    op.alter_column('entry', 'sleep_start_time', existing_type=sa.DateTime(), type_=sa.Time())
    op.alter_column('entry', 'sleep_end_time', existing_type=sa.DateTime(), type_=sa.Time())


def downgrade():
    # Change data type of sleep_start_time and sleep_end_time columns back to DateTime
    op.alter_column('entry', 'sleep_start_time', existing_type=sa.Time(), type_=sa.DateTime())
    op.alter_column('entry', 'sleep_end_time', existing_type=sa.Time(), type_=sa.DateTime())

    # Deleting all entries from the entry table
    op.execute("DELETE FROM entry")
