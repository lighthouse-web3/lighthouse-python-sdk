#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestGetFileInfo(unittest.TestCase):

    def test_get_file_info(self):
        """test get_upload function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getFileInfo("Qmd5MBBScDUV3Ly8qahXtZFqyRRfYSmUwEcxpYcV4hzKfW")
        self.assertIsInstance(res, dict, "data is a dict")
        self.assertEqual(res.get("cid"),"Qmd5MBBScDUV3Ly8qahXtZFqyRRfYSmUwEcxpYcV4hzKfW", "cid is matching")

        
