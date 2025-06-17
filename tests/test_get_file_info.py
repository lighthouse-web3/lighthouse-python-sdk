#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestGetFileInfo(unittest.TestCase):

    def test_get_file_info(self):
        """test get_file_info function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getFileInfo("Qmd5MBBScDUV3Ly8qahXtZFqyRRfYSmUwEcxpYcV4hzKfW")
        self.assertIsInstance(res, dict, "data is a dict")
        self.assertEqual(res.get("cid"),"Qmd5MBBScDUV3Ly8qahXtZFqyRRfYSmUwEcxpYcV4hzKfW", "cid is matching")
    
    def test_get_file_info_invalid_token(self):
        """test get_upload with invalid token"""
        with self.assertRaises(Exception) as context:
            l = Lighthouse("invalid_token")
            l.getFileInfo("Qmd5MBBScDUV3Ly8qahXtZFqyRRfYSmUwEcxpYcV4hzKfW")
            self.assertIn("authentication failed", str(context.exception).lower())
    
    def test_get_file_info_invalid_cid(self):
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getFileInfo("invalid_cid")
        self.assertIsInstance(res, dict, "res is dict")
        self.assertIsInstance(res.get('error'), dict, "error is dict")
        self.assertEqual(res.get("error").get('message'), 'Not Found', 'cid not found')