"""Executable data and file-boundary expectations."""

from __future__ import annotations

import unittest

from fixture_app import Session, StoredObject, Upload, read_object, secure_upload, unsafe_upload


class DataFilesFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.objects: dict[str, StoredObject] = {}
        self.session_a = Session("user-a", "tenant-a")
        self.session_b = Session("user-b", "tenant-b")
        self.png = Upload("avatar.png", "image/png", b"\x89PNG\r\n\x1a\nfixture")

    def test_unsafe_upload_publishes_object(self) -> None:
        object_id = unsafe_upload(self.png, self.objects)
        self.assertEqual(read_object(None, object_id, self.objects), (200, self.png.content))

    def test_secure_upload_is_private_and_owner_can_read(self) -> None:
        status, object_id = secure_upload(self.session_a, self.png, self.objects)
        self.assertEqual(status, 201)
        assert object_id is not None
        self.assertEqual(read_object(self.session_a, object_id, self.objects), (200, self.png.content))
        self.assertEqual(read_object(None, object_id, self.objects), (404, None))

    def test_cross_tenant_read_is_denied(self) -> None:
        _, object_id = secure_upload(self.session_a, self.png, self.objects)
        assert object_id is not None
        self.assertEqual(read_object(self.session_b, object_id, self.objects), (404, None))

    def test_oversized_upload_is_rejected(self) -> None:
        oversized = Upload("large.txt", "text/plain", b"x" * 1025)
        self.assertEqual(secure_upload(self.session_a, oversized, self.objects), (413, None))

    def test_declared_type_must_match_content(self) -> None:
        executable = Upload("run.txt", "text/plain", b"#!/bin/sh\nrm -rf data")
        self.assertEqual(secure_upload(self.session_a, executable, self.objects), (415, None))

    def test_generated_object_key_does_not_use_traversal_filename(self) -> None:
        path_name = Upload("../../private/secret.txt", "text/plain", b"safe text")
        status, object_id = secure_upload(self.session_a, path_name, self.objects)
        self.assertEqual(status, 201)
        assert object_id is not None
        self.assertNotIn("..", object_id)
        self.assertNotIn("secret.txt", object_id)


if __name__ == "__main__":
    unittest.main()
