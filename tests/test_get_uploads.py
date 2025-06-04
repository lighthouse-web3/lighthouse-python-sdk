#!/usr/bin/env python3
import os
import io
import unittest
from src.lighthouseweb3 import Lighthouse
from src.lighthouseweb3.functions.utils import NamedBufferedReader
from .setup import parse_env


class TestGetUploads(unittest.TestCase):

    def test_get_upload(self):
        """test get_upload function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getUploads()
        self.assertIsInstance(res.get("fileList"), list, "data is a list")
        self.assertIsInstance(res.get('totalFiles'), int, "totalFiles is an int")
    
    def test_get_upload_with_last_key(self):
        """test get_upload function with lastKey"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getUploads('b5f60ba0-b708-41a3-b0f2-5c808ce63b48')
        self.assertIsInstance(res.get("fileList"), list, "data is a list")
        self.assertIsInstance(res.get('totalFiles'), int, "totalFiles is an int")