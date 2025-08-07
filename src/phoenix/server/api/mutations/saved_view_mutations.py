from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
import strawberry
from strawberry import UNSET
from strawberry.relay import GlobalID
from strawberry.types import Info

from phoenix.server.api.auth import IsLocked, IsNotReadOnly
from phoenix.server.api.context import Context
from phoenix.server.api.exceptions import BadRequest, NotFound, Unauthorized
from phoenix.server.api.types.Project import Project
from phoenix.server.api.types.SavedView import SavedView, to_gql_saved_view
from phoenix.server.api.types.ValidationResult import ValidationResult
from phoenix.server.api.types.node import from_global_id_with_expected_type
from phoenix.db import models


@strawberry.input
class SavedViewPayloadInput:
    filter_condition: Optional[str] = UNSET
    time_range_key: Optional[str] = UNSET
    time_range_start: Optional[str] = UNSET  # ISO string
    time_range_end: Optional[str] = UNSET
    treat_orphans_as_roots: Optional[bool] = UNSET


def _build_payload(input: SavedViewPayloadInput) -> dict[str, object]:
    payload: dict[str, object] = {}
    if isinstance(input.filter_condition, str):
        payload["filterCondition"] = input.filter_condition
    if isinstance(input.time_range_key, str):
        payload["timeRangeKey"] = input.time_range_key
    if isinstance(input.time_range_start, str) or isinstance(input.time_range_end, str):
        payload["timeRange"] = {
            "start": input.time_range_start,
            "end": input.time_range_end,
        }
    if isinstance(input.treat_orphans_as_roots, bool):
        payload["options"] = {"treatOrphansAsRoots": input.treat_orphans_as_roots}
    return payload


@strawberry.input
class CreateSavedViewInput:
    project_id: GlobalID
    name: str
    payload: SavedViewPayloadInput

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise BadRequest("Name cannot be empty")


@strawberry.input
class PatchSavedViewInput:
    id: GlobalID
    name: Optional[str] = UNSET
    payload: Optional[SavedViewPayloadInput] = UNSET


@strawberry.input
class DeleteSavedViewsInput:
    ids: list[GlobalID]


@strawberry.type
class SavedViewMutationPayload:
    node: SavedView


@strawberry.type
class SavedViewMutationMixin:
    @strawberry.mutation(permission_classes=[IsNotReadOnly, IsLocked])  # type: ignore
    async def create_saved_view(
        self,
        info: Info[Context, None],
        input: CreateSavedViewInput,
    ) -> SavedViewMutationPayload:
        assert (request := info.context.request)
        user = getattr(request, "user", None)
        if not user or not isinstance(user.identity, (str, int)):
            raise Unauthorized("Authentication required")
        owner_id = int(user.identity)
        project_rowid = from_global_id_with_expected_type(input.project_id, Project.__name__)
        # Validate filter condition if provided
        if isinstance(input.payload.filter_condition, str) and input.payload.filter_condition:
            # Reuse Project.validate_span_filter_condition
            validation: ValidationResult = await Project(project_rowid).validate_span_filter_condition(
                info, input.payload.filter_condition
            )
            if not validation.is_valid:
                raise BadRequest(validation.error_message or "Invalid filter condition")
        payload = _build_payload(input.payload)
        view = models.SavedView(
            name=input.name.strip(),
            project_id=project_rowid,
            owner_user_id=owner_id,
            payload=payload,
        )
        async with info.context.db() as session:
            session.add(view)
            try:
                await session.flush()
            except Exception as e:  # uniqueness violations
                raise BadRequest("A view with this name already exists")
        return SavedViewMutationPayload(node=to_gql_saved_view(view))

    @strawberry.mutation(permission_classes=[IsNotReadOnly, IsLocked])  # type: ignore
    async def patch_saved_view(
        self,
        info: Info[Context, None],
        input: PatchSavedViewInput,
    ) -> SavedViewMutationPayload:
        assert (request := info.context.request)
        user = getattr(request, "user", None)
        if not user or not isinstance(user.identity, (str, int)):
            raise Unauthorized("Authentication required")
        owner_id = int(user.identity)
        id_ = from_global_id_with_expected_type(input.id, SavedView.__name__)
        async with info.context.db() as session:
            view = await session.get(models.SavedView, id_)
            if not view:
                raise NotFound("SavedView not found")
            if view.owner_user_id != owner_id:
                raise Unauthorized("Not allowed to modify this view")
            if isinstance(input.name, str):
                if not input.name.strip():
                    raise BadRequest("Name cannot be empty")
                view.name = input.name.strip()
            if isinstance(input.payload, SavedViewPayloadInput):
                if isinstance(input.payload.filter_condition, str) and input.payload.filter_condition:
                    validation: ValidationResult = await Project(view.project_id).validate_span_filter_condition(
                        info, input.payload.filter_condition
                    )
                    if not validation.is_valid:
                        raise BadRequest(validation.error_message or "Invalid filter condition")
                # merge payload keys
                updated = view.payload.copy() if view.payload else {}
                updated.update(_build_payload(input.payload))
                view.payload = updated
            if view is session.dirty:
                await session.flush()
        return SavedViewMutationPayload(node=to_gql_saved_view(view))

    @strawberry.mutation(permission_classes=[IsNotReadOnly])  # type: ignore
    async def delete_saved_views(
        self,
        info: Info[Context, None],
        input: DeleteSavedViewsInput,
    ) -> bool:
        assert (request := info.context.request)
        user = getattr(request, "user", None)
        if not user or not isinstance(user.identity, (str, int)):
            raise Unauthorized("Authentication required")
        owner_id = int(user.identity)
        ids = [from_global_id_with_expected_type(gid, SavedView.__name__) for gid in input.ids]
        stmt = sa.delete(models.SavedView).where(
            models.SavedView.id.in_(ids), models.SavedView.owner_user_id == owner_id
        )
        async with info.context.db() as session:
            await session.execute(stmt)
        return True
