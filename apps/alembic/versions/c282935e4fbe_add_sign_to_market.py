"""Add sign to market subscriptions

Revision ID: c282935e4fbe
Revises: f0a24a55a727
Create Date: 2025-12-25 15:21:08.389921

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c282935e4fbe"
down_revision = "f0a24a55a727"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "market_subscriptions",
        sa.Column("sign", sa.Text(), nullable=True, default="gt", server_default="gt"),
    )


def downgrade() -> None:
    op.drop_column("market_subscriptions", "sign")
