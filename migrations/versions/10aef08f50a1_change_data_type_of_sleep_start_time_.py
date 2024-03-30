"""Change data type of sleep_start_time and sleep_end_time columns to Time and delete all entries

Revision ID: 10aef08f50a1
Revises: a3e7263c42d1
Create Date: 2024-03-29 13:54:34.696850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10aef08f50a1'
down_revision = 'a3e7263c42d1'
branch_labels = None
depends_on = None


def upgrade():
    # Delete all entries from the 'entry' table
    op.execute("DELETE FROM entry")

    # Change data type of 'sleep_start_time' column to 'Time'
    op.alter_column('entry', 'sleep_start_time', existing_type=sa.DateTime(), type_=sa.Time())

    # Change data type of 'sleep_end_time' column to 'Time'
    op.alter_column('entry', 'sleep_end_time', existing_type=sa.DateTime(), type_=sa.Time())


def downgrade():
    # No downgrade needed as it's a destructive operation (deleting data)
    pass
