"""add indexes to audit_events

Revision ID: 452c4b457d8e
Revises: <PREVIOUS_REVISION_ID>
Create Date: 2026-02-07 12:15:16.683078
"""

from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision = "452c4b457d8e"
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_index(
        "ix_audit_events_event_type",
        "audit_events",
        ["event_type"],
    )

    op.create_index(
        "ix_audit_events_actor",
        "audit_events",
        ["actor"],
    )

    op.create_index(
        "ix_audit_events_timestamp",
        "audit_events",
        ["timestamp"],
    )


def downgrade():
    op.drop_index("ix_audit_events_timestamp", table_name="audit_events")
    op.drop_index("ix_audit_events_actor", table_name="audit_events")
    op.drop_index("ix_audit_events_event_type", table_name="audit_events")
