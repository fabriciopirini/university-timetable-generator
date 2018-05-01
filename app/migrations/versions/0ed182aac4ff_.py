"""empty message

Revision ID: 0ed182aac4ff
Revises: ce642cb311c7
Create Date: 2018-04-30 12:54:24.910697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ed182aac4ff'
down_revision = 'ce642cb311c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('disciplinas', sa.Column('curso', sa.String(length=5), nullable=True))
    op.create_foreign_key(None, 'turmas', 'disciplinas', ['idDisciplina'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'turmas', type_='foreignkey')
    op.drop_column('disciplinas', 'curso')
    # ### end Alembic commands ###
