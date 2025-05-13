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
        res = l.getBalance("0x1FB9Be96d228De94F4C57962675433Ae55a6c4a5")
        self.assertIsInstance(res, dict, "data is a dict")
        self.assertIsInstance(res.get("dataLimit"), int, "data limit is a integer")
        self.assertIsInstance(res.get("dataUsed"), int, "data used is a integer")

       
        
