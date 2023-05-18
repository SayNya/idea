"""empty message

Revision ID: 531db309b308
Revises: 589495d40206
Create Date: 2023-05-17 17:32:25.859995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "531db309b308"
down_revision = "589495d40206"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "idea_roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("code", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_idea_roles_id"), "idea_roles", ["id"], unique=False)
    op.create_table(
        "user_idea",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("idea_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("idea_role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["idea_id"],
            ["ideas.id"],
        ),
        sa.ForeignKeyConstraint(
            ["idea_role_id"],
            ["idea_roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "idea_id", "user_id", "idea_role_id", name=op.f("uq_user_idea_idea_id")
        ),
    )
    op.create_index(op.f("ix_user_idea_id"), "user_idea", ["id"], unique=False)
    op.add_column(
        "user_system_role", sa.Column("user_id", sa.Integer(), nullable=False)
    )
    op.add_column(
        "user_system_role", sa.Column("system_role_id", sa.Integer(), nullable=False)
    )
    op.drop_constraint(
        "user_system_role_employee_id_fkey", "user_system_role", type_="foreignkey"
    )
    op.drop_constraint(
        "user_system_role_role_id_fkey", "user_system_role", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "user_system_role", "system_roles", ["system_role_id"], ["id"]
    )
    op.create_foreign_key(None, "user_system_role", "users", ["user_id"], ["id"])
    op.drop_column("user_system_role", "employee_id")
    op.drop_column("user_system_role", "role_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_system_role",
        sa.Column("role_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "user_system_role",
        sa.Column("employee_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "user_system_role", type_="foreignkey")
    op.drop_constraint(None, "user_system_role", type_="foreignkey")
    op.create_foreign_key(
        "user_system_role_role_id_fkey",
        "user_system_role",
        "system_roles",
        ["role_id"],
        ["id"],
    )
    op.create_foreign_key(
        "user_system_role_employee_id_fkey",
        "user_system_role",
        "users",
        ["employee_id"],
        ["id"],
    )
    op.drop_column("user_system_role", "system_role_id")
    op.drop_column("user_system_role", "user_id")
    op.drop_index(op.f("ix_user_idea_id"), table_name="user_idea")
    op.drop_table("user_idea")
    op.drop_index(op.f("ix_idea_roles_id"), table_name="idea_roles")
    op.drop_table("idea_roles")
    # ### end Alembic commands ###
