#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestRemoveIPNSRecord(unittest.TestCase):

    def test_ipns_generate_key(self):
        """test ipns_generate_key function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))

        key = l.generateKey()

        self.assertIsInstance(key, dict, "result is a dict")
        self.assertIsInstance(key.get("data"), dict , "data is a dict")
        self.assertIsInstance(key.get("data").get("ipnsName"), str , "ipnsName is a str")
        self.assertIsInstance(key.get("data").get("ipnsId"), str , "ipnsId is a dict")

    
        res = l.removeKey(key.get('data').get('ipnsName'))
        self.assertIsInstance(res, dict, "result is a dict")
        self.assertIsInstance(res.get("data"), dict , "data is a dict")
        self.assertIsInstance(res.get("data").get("Keys"), list , "Keys is a list")
        self.assertEqual(res.get("data").get("Keys")[0].get('Name'), key.get('data').get('ipnsName'))
        self.assertEqual(res.get("data").get("Keys")[0].get('Id'), key.get('data').get('ipnsId'))