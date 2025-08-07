from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import strawberry
from strawberry.relay import Node, NodeID
from strawberry.types import Info

from phoenix.db import models
from phoenix.server.api.context import Context
from phoenix.server.api.types.User import User, to_gql_user


@strawberry.type
class SavedView(Node):
    id_attr: NodeID[int]
    name: str
    created_at: datetime
    updated_at: datetime
    project_id: strawberry.Private[int]
    owner_user_id: strawberry.Private[int]
    payload: strawberry.Private[dict[str, object]]

    @strawberry.field
    async def owner(self, info: Info[Context, None]) -> User:
        async with info.context.db() as session:
            user = await session.get(models.User, self.owner_user_id)
        assert user
        return to_gql_user(user)

    @strawberry.field
    def filter_condition(self) -> Optional[str]:
        return str(self.payload.get("filterCondition")) if self.payload else None

    @strawberry.field
    def time_range_key(self) -> Optional[str]:
        return str(self.payload.get("timeRangeKey")) if self.payload else None

    @strawberry.field
    def time_range_start(self) -> Optional[datetime]:
        v = self.payload.get("timeRange", {}).get("start") if self.payload else None
        return None if v in (None, "") else datetime.fromisoformat(v)

    @strawberry.field
    def time_range_end(self) -> Optional[datetime]:
        v = self.payload.get("timeRange", {}).get("end") if self.payload else None
        return None if v in (None, "") else datetime.fromisoformat(v)

    @strawberry.field
    def treat_orphans_as_roots(self) -> Optional[bool]:
        opts = self.payload.get("options") if self.payload else None
        if isinstance(opts, dict):
            v = opts.get("treatOrphansAsRoots")
            return bool(v) if v is not None else None
        return None


def to_gql_saved_view(view: models.SavedView) -> SavedView:
    return SavedView(
        id_attr=view.id,
        name=view.name,
        created_at=view.created_at,
        updated_at=view.updated_at,
        project_id=view.project_id,
        owner_user_id=view.owner_user_id,
        payload=view.payload or {},
    )
