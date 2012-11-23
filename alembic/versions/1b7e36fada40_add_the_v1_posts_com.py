"""Add the v1 posts, comments and votes tables

Revision ID: 1b7e36fada40
Revises: None
Create Date: 2012-11-22 22:25:04.726000

"""

# revision identifiers, used by Alembic.
revision = '1b7e36fada40'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable = False),
    sa.Column('title', sa.String(length = 50), nullable = False),
    sa.Column('body', sa.Text(), nullable = False),
    sa.Column('author', sa.String(length = 8), nullable = True),
    sa.Column('replies_enabled', sa.Boolean(), nullable = False),
    sa.Column('post_date', sa.DateTime(), nullable = False),
    sa.Column('author_gender', sa.Enum('M', 'F', 'O'), nullable = False),
    sa.Column('saw_gender', sa.Enum('M', 'F', 'O'), nullable = False),
    sa.Column('is_visible', sa.Boolean(), nullable = False),
    sa.Column('been_moderated', sa.Boolean(), nullable = False),
    sa.Column('ip', sa.String(length = 15), nullable = False),
    sa.Column('num_contacts', sa.Integer(), nullable = False),
    sa.Column('sticky', sa.Boolean(), nullable = False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable = False),
    sa.Column('post_id', sa.Integer(), nullable = False),
    sa.Column('post_date', sa.DateTime(), nullable = False),
    sa.Column('body', sa.Text(), nullable = False),
    sa.Column('author_gender', sa.Enum('M', 'F', 'O'), nullable = False),
    sa.Column('ip', sa.String(length = 15), nullable = False),
    sa.Column('is_visible', sa.Boolean(), nullable = False),
    sa.Column('author', sa.String(length = 8), nullable = True),
    sa.Column('replies_enabled', sa.Boolean(), nullable = False),
    sa.Column('num_contacts', sa.Integer(), nullable = False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'],),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote',
    sa.Column('id', sa.Integer(), nullable = False),
    sa.Column('comment_id', sa.Integer(), nullable = False),
    sa.Column('direction', sa.Enum('UP', 'DOWN'), nullable = False),
    sa.Column('voter', sa.String(length = 8), nullable = False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'],),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    op.drop_table('vote')
    op.drop_table('comment')
    op.drop_table('post')
    ### end Alembic commands ###
