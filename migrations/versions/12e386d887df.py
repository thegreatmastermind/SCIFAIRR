"""empty message

Revision ID: 12e386d887df
Revises: 
Create Date: 2024-03-28 12:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12e386d887df'
down_revision = None  # This should be the previous revision ID if applicable
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns for food-related information
    op.add_column('entry', sa.Column('food_name', sa.String(length=255)))
    op.add_column('entry', sa.Column('food_description', sa.String(length=1000)))
    
    # Alter columns to change sleep times from Time to DateTime
    op.alter_column('entry', 'sleep_start_time', existing_type=sa.Time(), type_=sa.DateTime())
    op.alter_column('entry', 'sleep_end_time', existing_type=sa.Time(), type_=sa.DateTime())

    # Convert existing data from Time to DateTime
    op.execute("UPDATE entry SET sleep_start_time = datetime('1900-01-01', sleep_start_time)")
    op.execute("UPDATE entry SET sleep_end_time = datetime('1900-01-01', sleep_end_time)")


def downgrade():
    # Convert sleep times back to Time
    op.execute("UPDATE entry SET sleep_start_time = time(sleep_start_time)")
    op.execute("UPDATE entry SET sleep_end_time = time(sleep_end_time)")

    # Remove added columns
    op.drop_column('entry', 'food_name')
    op.drop_column('entry', 'food_description')

def downgrade():
    # Alter columns to change data types back to Time
    op.alter_column('entry', 'sleep_start_time', existing_type=sa.DateTime(), type_=sa.Time())
    op.alter_column('entry', 'sleep_end_time', existing_type=sa.DateTime(), type_=sa.Time())

    # Convert existing data from DateTime to Time
    op.execute("UPDATE entry SET sleep_start_time = time(sleep_start_time)")
    op.execute("UPDATE entry SET sleep_end_time = time(sleep_end_time)")

