#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestGetIPNSRecord(unittest.TestCase):

    def test_get_ipns_records(self):
        """test get_ipns_records function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getAllKeys()
        self.assertIsInstance(res, dict, "result is a dict")
        self.assertIsInstance(res.get("data"), list , "data is a dict")
        self.assertIsInstance(res.get("data")[0].get("ipnsName"), str , "ipnsName is a str")
        self.assertIsInstance(res.get("data")[0].get("ipnsId"), str , "ipnsId is a str")
        self.assertIsInstance(res.get("data")[0].get("publicKey"), str , "publicKey is a str")
        self.assertIsInstance(res.get("data")[0].get("cid"), str , "cid is a str")
        self.assertIsInstance(res.get("data")[0].get("lastUpdate"), int , "lastUpdate is a int")
    
    def test_get_ipns_records_invalid_token(self):
        """test get_ipns_records with invalid token"""
        parse_env()
        l = Lighthouse("invalid_token")
        with self.assertRaises(Exception) as context:
            l.generateKey()
            self.assertIn("authentication failed", str(context.exception).lower())