"""added db relations

Revision ID: def7f3fad11b
Revises: af47d023df1a
Create Date: 2021-12-26 02:02:26.801101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'def7f3fad11b'
down_revision = 'af47d023df1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('department', sa.String(), nullable=True))
    op.drop_constraint('employee_department_id_fkey', 'employee', type_='foreignkey')
    op.create_foreign_key(None, 'employee', 'department', ['department'], ['name'])
    op.drop_column('employee', 'department_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('department_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'employee', type_='foreignkey')
    op.create_foreign_key('employee_department_id_fkey', 'employee', 'department', ['department_id'], ['id'])
    op.drop_column('employee', 'department')
    # ### end Alembic commands ###
