"""Updated db relations

Revision ID: ead1af4779ed
Revises: 16e8e2976ede
Create Date: 2021-12-26 18:34:13.517741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ead1af4779ed'
down_revision = '16e8e2976ede'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('department_id', sa.String(), nullable=True))
    op.drop_constraint('employee_department_uuid_fkey', 'employee', type_='foreignkey')
    op.create_foreign_key(None, 'employee', 'department', ['department_id'], ['id'])
    op.drop_column('employee', 'department_uuid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('department_uuid', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.create_foreign_key('employee_department_uuid_fkey', 'employee', 'department', ['department_uuid'], ['uuid'])
    op.drop_column('employee', 'department_id')
    # ### end Alembic commands ###
