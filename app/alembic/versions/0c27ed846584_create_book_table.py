"""Create book table

Revision ID: 0c27ed846584
Revises:
Create Date: 2025-10-07 18:38:59.012604

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision = "0c27ed846584"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "book",
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("author", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_book_id"), "book", ["id"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_book_id"), table_name="book")
    op.drop_table("book")
