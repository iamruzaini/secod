"""Local model of secure OpenAI server and tool-execution boundaries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    user_id: str
    tenant_id: str
    authenticated: bool = True


@dataclass(frozen=True)
class Resource:
    resource_id: str
    tenant_id: str
    owner_id: str
    content: str


@dataclass(frozen=True)
class ToolRequest:
    name: str
    arguments: dict[str, object]


def insecure_browser_config(config: dict[str, str]) -> dict[str, str]:
    """Insecure client integration: sends API key to browser code."""
    return dict(config)


def secure_browser_config(config: dict[str, str]) -> dict[str, str]:
    return {"OPENAI_MODEL": config["OPENAI_MODEL"]} if "OPENAI_MODEL" in config else {}


def insecure_dispatch(request: ToolRequest, tools: dict[str, object]) -> object:
    """Insecure dispatch: model/user selects arbitrary callable by name."""
    tool = tools[request.name]
    return tool(request.arguments)  # type: ignore[operator]


def secure_dispatch(
    session: Session,
    request: ToolRequest,
    resources: dict[str, Resource],
    tools: dict[str, object],
) -> tuple[int, object | None]:
    if not session.authenticated:
        return 401, None
    allowed = {"read_resource", "create_note"}
    if request.name not in allowed or request.name not in tools:
        return 403, None
    if request.name == "read_resource":
        resource_id = request.arguments.get("resource_id")
        if not isinstance(resource_id, str):
            return 422, None
        resource = resources.get(resource_id)
        if resource is None or resource.tenant_id != session.tenant_id:
            return 404, None
        if resource.owner_id != session.user_id:
            return 403, None
        return 200, tools[request.name](resource)  # type: ignore[operator]
    title = request.arguments.get("title")
    if not isinstance(title, str) or not title or len(title) > 100:
        return 422, None
    return 200, tools[request.name]({"title": title, "tenant_id": session.tenant_id})  # type: ignore[operator]
