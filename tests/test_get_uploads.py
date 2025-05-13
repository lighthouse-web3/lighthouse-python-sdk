#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestGetUploads(unittest.TestCase):

    def test_get_upload(self):
        """test get_upload function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getUploads()
        self.assertIsInstance(res.get("fileList"), list, "data is a list")

        
