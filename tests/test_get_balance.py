#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestGetBalance(unittest.TestCase):

    def test_get_balance(self):
        """test get_balance function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getBalance()
        self.assertIsInstance(res, dict, "data is a dict")
        self.assertIsInstance(res.get("dataLimit"), int, "data limit is a integer")
        self.assertIsInstance(res.get("dataUsed"), int, "data used is a integer")
    
    def test_get_balance_invalid_token(self):
        """test get_balance function with invalid token"""
        parse_env()
        l = Lighthouse('invalid_token')
        res = l.getBalance()
        self.assertIsInstance(res, dict, "res is a dict")
        self.assertIn("authentication failed", str(res).lower())

