#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestRemoveIPNSRecord(unittest.TestCase):

    def test_ipns_remove_key(self):
        """test ipns_remove_key function"""
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
    
    def test_ipns_remove_key_invalid_token(self):
        """test ipns_remove_key with invalid token"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))

        key = l.generateKey()

        self.assertIsInstance(key, dict, "result is a dict")
        self.assertIsInstance(key.get("data"), dict , "data is a dict")
        self.assertIsInstance(key.get("data").get("ipnsName"), str , "ipnsName is a str")
        self.assertIsInstance(key.get("data").get("ipnsId"), str , "ipnsId is a dict")

        l = Lighthouse("invalid_token")
        key_name = key.get('data').get('ipnsName')
        with self.assertRaises(Exception) as context:
            l.removeKey(key_name)
            self.assertIn("authentication failed", str(context.exception).lower())
    
    def test_ipns_remove_key_invalid_key_name(self):
        """test ipns_remove_key with invalid key name"""
        parse_env()

        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.removeKey('invalid_key_name')
        self.assertIsInstance(res, dict, "record is a dict")
        self.assertIsInstance(res.get("error"), list, "error is a list")
        self.assertEqual(res.get("error")[0]['message'], 'Something went wrong.' )