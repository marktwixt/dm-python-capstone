"""empty message

Revision ID: b6578650ccb1
Revises: 
Create Date: 2023-06-26 15:27:33.200034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6578650ccb1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.drop_column('status')

    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('trail_system_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'trail_systems', ['trail_system_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('trail_system_id')

    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
