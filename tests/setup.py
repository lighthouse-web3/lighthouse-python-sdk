#!/usr/bin/env python3

import os

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
