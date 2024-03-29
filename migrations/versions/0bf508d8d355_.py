"""empty message

Revision ID: 0bf508d8d355
Revises: 78b62fd11056
Create Date: 2019-02-17 16:21:43.444233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bf508d8d355'
down_revision = '78b62fd11056'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('content',
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('content_title', sa.String(length=160), nullable=False),
    sa.Column('content_type_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cover_key', sa.String(length=160), nullable=True),
    sa.Column('content_key', sa.String(length=160), nullable=True),
    sa.Column('summary', sa.String(length=5000), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.author_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['content_type_id'], ['content_type.content_type_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('content_id')
    )
    op.create_table('content_category',
    sa.Column('content_category_id', sa.Integer(), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.category_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['content_id'], ['content.content_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('content_category_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('content_category')
    op.drop_table('content')
    # ### end Alembic commands ###
