#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestIPNSGenerateKey(unittest.TestCase):

    def test_ipns_generate_key(self):
        """test ipns_generate_key function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.generateKey()
        self.assertIsInstance(res, dict, "result is a dict")
        self.assertIsInstance(res.get("data"), dict , "data is a dict")
        self.assertIsInstance(res.get("data").get("ipnsName"), str , "ipnsName is a str")
        self.assertIsInstance(res.get("data").get("ipnsId"), str , "ipnsId is a dict")
    
    def test_ipns_generate_key_invalid_token(self):
        """test ipns_generate_key with invalid token"""
        parse_env()
        l = Lighthouse("invalid_token")
        with self.assertRaises(Exception) as context:
            l.generateKey()
            self.assertIn("authentication failed", str(context.exception).lower())
        
    