#!/usr/bin/env python3

import os
from . import deploy as dt


def parse_env():
    """parse .env file"""
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            key, value = line.split("=")
            os.environ[key] = value.strip()


def run_test():
    """setup test environment and run tests"""
    parse_env()
    dt.test_deploy()


if __name__ == "__main__":
    run_test()
