"""remove unique

Revision ID: ba6663aa4db0
Revises: fb43eec50c64
Create Date: 2024-07-11 13:38:04.874580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba6663aa4db0'
down_revision = 'fb43eec50c64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.alter_column('stack',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.drop_constraint('projects_description_key', type_='unique')
        batch_op.drop_constraint('projects_docs_link_key', type_='unique')
        batch_op.drop_constraint('projects_github_link_key', type_='unique')
        batch_op.drop_constraint('projects_language_key', type_='unique')
        batch_op.drop_constraint('projects_name_key', type_='unique')
        batch_op.drop_constraint('projects_stack_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.create_unique_constraint('projects_stack_key', ['stack'])
        batch_op.create_unique_constraint('projects_name_key', ['name'])
        batch_op.create_unique_constraint('projects_language_key', ['language'])
        batch_op.create_unique_constraint('projects_github_link_key', ['github_link'])
        batch_op.create_unique_constraint('projects_docs_link_key', ['docs_link'])
        batch_op.create_unique_constraint('projects_description_key', ['description'])
        batch_op.alter_column('stack',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###
