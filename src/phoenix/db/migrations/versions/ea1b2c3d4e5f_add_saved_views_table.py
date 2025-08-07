"""
Add saved views table

Revision ID: ea1b2c3d4e5f
Revises: bb8139330879
Create Date: 2025-08-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ea1b2c3d4e5f"
down_revision: Union[str, None] = "bb8139330879"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "saved_views",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("owner_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("payload", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    op.create_unique_constraint(
        "uq_saved_views_project_owner_name",
        "saved_views",
        ["project_id", "owner_user_id", "name"],
    )
    op.create_index("ix_saved_views_project_id", "saved_views", ["project_id"]) 
    op.create_index("ix_saved_views_owner_user_id", "saved_views", ["owner_user_id"]) 


def downgrade() -> None:
    op.drop_index("ix_saved_views_owner_user_id", table_name="saved_views")
    op.drop_index("ix_saved_views_project_id", table_name="saved_views")
    op.drop_constraint("uq_saved_views_project_owner_name", "saved_views", type_="unique")
    op.drop_table("saved_views")
