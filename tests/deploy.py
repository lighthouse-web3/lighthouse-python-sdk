#!/usr/bin/env python3

import os
from main import Lighthouse


def test_deploy_file():
    """test deploy function"""
    l = Lighthouse(os.environ["LH_TOKEN"])
    res = l.deploy("tests/testdir/testfile.txt")
    assert res.get("data") != None
    assert res.get("data").get("Hash") != None


def test_deploy_dir():
    """test deploy function"""
    l = Lighthouse(os.environ["LH_TOKEN"])
    res = l.deploy("tests/testdir")
    assert res.get("data") != None
    assert isinstance(res.get("data"), str) == True
    assert "Hash" in res.get("data")
