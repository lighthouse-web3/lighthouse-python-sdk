#!/usr/bin/env python3
import os
import io
import unittest
from src.lighthouseweb3 import Lighthouse
from src.lighthouseweb3.functions.utils import NamedBufferedReader
from .setup import parse_env


class TestDealStatus(unittest.TestCase):

    def test_deal_status(self):
        """test static test_deal_status function"""
        res = Lighthouse.getDealStatus(
            "QmT9shXpKcn4HRbJhXJ1ZywzwjEo2QWbxAx4SVgW4eYKjG")
        self.assertIsInstance(res, list, "data is a list")
        self.assertIsInstance(res[0].get(
            "dealId"), int, "dealId is Int")

    def test_deal_status_init(self):
        """test deal_status function"""
        parse_env()
        l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
        res = l.getDealStatus(
            "QmT9shXpKcn4HRbJhXJ1ZywzwjEo2QWbxAx4SVgW4eYKjG")
        self.assertIsInstance(res, list, "data is a list")
        self.assertIsInstance(res[0].get(
            "dealId"), int, "dealId is Int")
