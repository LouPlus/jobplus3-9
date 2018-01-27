"""add resume in delivery

Revision ID: 4cf1851e669d
Revises: 7f8305c65e18
Create Date: 2018-01-28 03:43:50.708895

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4cf1851e669d'
down_revision = '7f8305c65e18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('delivery', sa.Column('resume_up', sa.String(length=256), nullable=True))
    op.alter_column('jobseeker', 'seekername',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('jobseeker', 'seekername',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    op.drop_column('delivery', 'resume_up')
    # ### end Alembic commands ###
