#!/usr/bin/env python3
import os
import io
import unittest
from src.lighthouseweb3 import Lighthouse
from src.lighthouseweb3.functions.utils import NamedBufferedReader
from .setup import parse_env
import string
import secrets


def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


class TestUpload(unittest.TestCase):
    def setUp(self) -> None:
        """setup test environment"""
        parse_env()

    def test_env(self):
        """test env var"""
        self.assertNotEqual(
            os.environ.get("LIGHTHOUSE_TOKEN"), None, "token is not None"
        )

    def test_upload_file(self):
        """test Upload function"""
        l = Lighthouse()  # will use env var
        res = l.upload("tests/testdir/testfile.txt")
        self.assertNotEqual(res.get("data"), None, "data is None")
        self.assertNotEqual(res.get("data").get("Hash"), None, "data is None")

    def test_upload_dir(self):
        """test Upload function"""
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.upload("tests/")
        self.assertNotEqual(res.get("data"), None, "data is None")
        self.assertIsInstance(res.get("data"), dict, "data is a dict")
        self.assertIsInstance(res.get("data").get(
            "Hash"), str, "Instance is not of type String")
        self.assertIsInstance(res.get("data").get(
            "Size"), str, "Instance is not of type String")

    def test_upload_Blob(self):
        """test Upload function"""
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.uploadBlob(
            io.BytesIO(b"tests/testdir/"), f"{generate_random_string(16)}.txt")
        self.assertNotEqual(res.get("data"), None, "data is None")
        self.assertIsInstance(res.get("data"), dict, "data is a dict")
        self.assertNotEqual(res.get("data").get("Hash"), None, "data is None")

    def test_upload_File(self):
        """test Upload function"""
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        with open("./.gitignore", "rb") as file:
            res = l.upload(file)
            self.assertNotEqual(res.get("data"), None, "data is None")
            self.assertIsInstance(res.get("data"), dict, "data is a dict")
            self.assertNotEqual(res.get("data").get(
                "Hash"), None, "data is None")

    def test_upload_with_tag(self):
        """test Upload with tag function"""
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        tag = generate_random_string(8)
        res = l.uploadBlob(
            io.BytesIO(b"tests/testdir/"+generate_random_string(80).encode("utf-8")), f"{generate_random_string(16)}.txt", tag)
        self.assertNotEqual(res.get("data"), None, "data is None")
        self.assertIsInstance(res.get("data"), dict, "data is a dict")
        self.assertIsInstance(res.get("data").get(
            "Hash"), str, "Hash is not of type string")

        tagData = l.getTagged(tag)
        self.assertEqual(tag, tagData.get("data").get("tag"), "Tag dont match")
        self.assertEqual(res.get("data").get("Hash"), tagData.get(
            "data").get("cid"), "Tag dont match")

        # overWrite tag
        res = l.uploadBlob(
            io.BytesIO(b"tests/testdir/"+generate_random_string(80).encode("utf-8")), f"{generate_random_string(16)}.txt", tag)
        tagData = l.getTagged(tag)
        self.assertEqual(tag, tagData.get("data").get("tag"), "Tag dont match")
        self.assertEqual(res.get("data").get("Hash"), tagData.get(
            "data").get("cid"), "Tag dont match")


if __name__ == "__main__":
    unittest.main()
