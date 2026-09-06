"""Executable OpenAI implementation expectations."""

from __future__ import annotations

import unittest

from fixture_app import (
    Resource,
    Session,
    ToolRequest,
    insecure_browser_config,
    insecure_dispatch,
    secure_dispatch,
    secure_browser_config,
)


class OpenaiFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.session_a = Session("user-a", "tenant-a")
        self.resources = {
            "resource-a": Resource("resource-a", "tenant-a", "user-a", "A"),
            "resource-b": Resource("resource-b", "tenant-b", "user-b", "B"),
        }
        self.calls: list[object] = []

    def test_api_key_stays_on_server(self) -> None:
        config = {"OPENAI_API_KEY": "server-secret", "OPENAI_MODEL": "fixture-model"}
        self.assertEqual(insecure_browser_config(config), config)
        self.assertNotIn("OPENAI_API_KEY", secure_browser_config(config))

    def test_arbitrary_model_tool_is_executable_at_unsafe_boundary(self) -> None:
        tools = {"delete_account": lambda arguments: self.calls.append(arguments) or "deleted"}
        request = ToolRequest("delete_account", {"account_id": "victim"})
        self.assertEqual(insecure_dispatch(request, tools), "deleted")
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(secure_dispatch(self.session_a, request, self.resources, tools), (403, None))

    def test_cross_tenant_resource_request_is_denied_after_server_reload(self) -> None:
        tools = {"read_resource": lambda resource: resource.content}
        request = ToolRequest("read_resource", {"resource_id": "resource-b"})
        self.assertEqual(insecure_dispatch(request, {"read_resource": lambda _: "B"}), "B")
        self.assertEqual(secure_dispatch(self.session_a, request, self.resources, tools), (404, None))

    def test_allowed_resource_read_uses_trusted_resource(self) -> None:
        tools = {"read_resource": lambda resource: resource.content}
        request = ToolRequest("read_resource", {"resource_id": "resource-a"})
        self.assertEqual(secure_dispatch(self.session_a, request, self.resources, tools), (200, "A"))

    def test_tool_arguments_are_schema_checked(self) -> None:
        tools = {"create_note": lambda arguments: arguments}
        invalid = ToolRequest("create_note", {"title": ["not", "text"]})
        self.assertEqual(secure_dispatch(self.session_a, invalid, self.resources, tools), (422, None))
        valid = ToolRequest("create_note", {"title": "hello"})
        self.assertEqual(
            secure_dispatch(self.session_a, valid, self.resources, tools),
            (200, {"title": "hello", "tenant_id": "tenant-a"}),
        )

    def test_unauthenticated_tool_request_is_denied(self) -> None:
        anonymous = Session("anonymous", "tenant-a", authenticated=False)
        request = ToolRequest("read_resource", {"resource_id": "resource-a"})
        self.assertEqual(
            secure_dispatch(anonymous, request, self.resources, {"read_resource": lambda _: "A"}),
            (401, None),
        )


if __name__ == "__main__":
    unittest.main()
