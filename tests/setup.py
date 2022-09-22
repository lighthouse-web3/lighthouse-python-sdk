#!/usr/bin/env python3

import os
from . import deploy as dt


def parse_env():
    """parse .env file"""
    try:
        with open(".env", "r") as f:
            for line in f.readlines():
                if line.startswith("#"):
                    continue
                key, value = line.split("=")
                os.environ[key] = value.strip()
    except FileNotFoundError:
        print("No .env file found")
        print("Defaulting to preset environment variables...")


def run_test():
    """setup test environment and run tests"""
    parse_env()
    # dt.test_deploy_file()
    dt.test_deploy_dir()


if __name__ == "__main__":
    run_test()
