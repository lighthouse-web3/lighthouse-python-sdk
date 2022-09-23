#!/usr/bin/env python3

import os
import unittest
from main import Lighthouse
from .setup import parse_env


class TestDeploy(unittest.TestCase):
    def setUp(self) -> None:
        """setup test environment"""
        parse_env()

    def test_deploy_file(self):
        """test deploy function"""
        l = Lighthouse(os.environ.get("LH_TOKEN", ""))
        res = l.deploy("tests/testdir/testfile.txt")
        self.assertNotEqual(res.get("data"), None, "data is None")
        self.assertNotEqual(res.get("data").get("Hash"), None, "data is None")

    def test_deploy_dir(self):
        """test deploy function"""
        l = Lighthouse(os.environ["LH_TOKEN"])
        res = l.deploy("tests/testdir/")
        self.assertNotEqual(res.get("data"), None, "data is None")
        self.assertIsInstance(res.get("data"), dict, "data is a dict")
        self.assertNotEqual(res.get("data").get("Hash"), None, "data is None")


if __name__ == "__main__":
    unittest.main()
