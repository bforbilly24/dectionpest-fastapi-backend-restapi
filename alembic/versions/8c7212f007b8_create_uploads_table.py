"""create uploads table

Revision ID: 8c7212f007b8
Revises: 
Create Date: 2025-04-05 19:09:47.641224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c7212f007b8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        "uploads",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("original_image", sa.String, nullable=False),
        sa.Column("detected_image", sa.String, nullable=False),
        sa.Column("detection_result", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table("uploads")