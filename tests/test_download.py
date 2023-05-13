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


class TestDownload(unittest.TestCase):
    def setUp(self) -> None:
        """setup test environment"""
        parse_env()

    def test_env(self):
        """test env var"""
        self.assertNotEqual(
            os.environ.get("LIGHTHOUSE_TOKEN"), None, "token is not None"
        )

    def test_download_file(self):
        """test Upload function"""
        l = Lighthouse()  # will use env var
        res, _ = l.download(
            "Qmd5MBBScDUV3Ly8qahXtZFqyRRfYSmUwEcxpYcV4hzKfW")
        self.assertIsInstance(res, bytes, "type doesn't match")
        self.assertEqual(res, b'tests/testdir/', "data doesn't match")

    # def test_download_blob(self):
    #     """test Upload function"""
    #     l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
    #     res = l.uploadBlob(
    #         io.BytesIO(b"tests/testdir/"), f"{generate_random_string(16)}.txt")
    #     self.assertNotEqual(res.get("data"), None, "data is None")
    #     self.assertIsInstance(res.get("data"), dict, "data is a dict")
    #     self.assertNotEqual(res.get("data").get("Hash"), None, "data is None")

    def test_download_blob_file(self):
        """test download_blob function"""
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        with open("./image.png", "wb") as file:
            res = l.downloadBlob(
                file, "QmPT11PFFQQD3mT6BdwfSHQGHRdF8ngmRmcvxtSBiddWEa", chunk_size=1024*100)
            self.assertEqual(file.tell(), 123939, "File Size dont match")
            self.assertEqual(res, True, "data doesn't match")


if __name__ == "__main__":
    unittest.main()
