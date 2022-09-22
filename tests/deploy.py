#!/usr/bin/env python3

import os
from main import Lighthouse


def test_deploy():
    """test deploy function"""
    l = Lighthouse(os.environ["LH_TOKEN"])
    assert l.deploy("tests/testfile.txt") == {"data": {}}
