#!/usr/bin/env python3

import os
from main import Lighthouse


def run_test():
    """setup test environment and run tests"""
    parse_env()
    test_deploy()


def test_deploy():
    """test deploy function"""
    l = Lighthouse(os.environ["LH_TOKEN"])
    assert l.deploy("tests/upload_test.txt") == {"data": {}}


def parse_env():
    """parse .env file"""
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            key, value = line.split("=")
            os.environ[key] = value.strip()


if __name__ == "__main__":
    run_test()
