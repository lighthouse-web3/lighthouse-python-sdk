#!/usr/bin/env python3
import os
import io
import unittest
from src.lighthouseweb3 import Lighthouse
from src.lighthouseweb3.functions.utils import NamedBufferedReader
from .setup import parse_env


class TestDealStatus(unittest.TestCase):

    def test_get_upload(self):
        """test static test_get_upload function"""
        res = Lighthouse.getUploads(
            "0xB23809427cFc9B3346AEC5Bb70E7e574696cAF80")
        self.assertIsInstance(res.get("fileList"), list, "data is a list")

    def test_get_upload_init(self):
        """test get_upload function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = Lighthouse.getUploads(
            "0xB23809427cFc9B3346AEC5Bb70E7e574696cAF80")
        self.assertIsInstance(res.get("fileList"), list, "data is a list")
