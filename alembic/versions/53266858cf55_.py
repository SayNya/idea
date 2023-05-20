"""empty message

Revision ID: 53266858cf55
Revises: 782d1bcc9c83
Create Date: 2023-05-19 15:22:57.903757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "53266858cf55"
down_revision = "782d1bcc9c83"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "department_admin",
        sa.Column("admin_id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["admin_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.PrimaryKeyConstraint("admin_id", "department_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("department_admin")
    # ### end Alembic commands ###
