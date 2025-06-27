#!/usr/bin/env python3
import unittest
from src.lighthouseweb3 import Kavach


class TestKavachRecoverKey(unittest.TestCase):
  def test_recover_key(self):
    """test recover key with valid shards"""
    known_key = "0b2ccf87909bd1215858e5c0ec99359cadfcf918a4fac53e3e88e9ec28bec678"
    result = [{'key': '20e2fdc23015c6c78272174be8639b49275e0dbf0479dde60950832ef18bb661', 'index': '9d956693217a5443ba1823151f0924d5a59aaa009cef8cd0f97d3e1a6d279140'}, {'key': '508e1ddc5c06b7e2053d600c4c5da6627778b371784ef712cb8c96f7deae9ce4', 'index': '61a82e98b2c19d13f7edeb1c79c36c40378a5ec2df2e818c6cbd0ead5e548178'}, {'key': '0aca075033a6d257cbac7564c01637b111268f8d42974e5bd765004cc840d359', 'index': '8339e90fc50c9b6b4d650bd03187f4cb4e42e616d1acb6c77dae037764997adb'}, {'key': '4c8a56b19e66a4d533946fe3bb4929556258869f939769514c0abdf8d22d1fa2', 'index': '283985072fcb14bcaf20f5c393d4af5f49a6d2cae472fb28038507f174f7d22d'}, {'key': '2ab718fe611b09eae351a53969364df1bd754f345de87839d22bbcae6b8d091f', 'index': '107dd8993e24875227e024e3352ab7333a766b93cd646f51bc68a2ebc682c64a'}]

    recovered = Kavach.recoverKey(result)
    self.assertEqual(recovered["masterKey"], known_key, "Recovered key should match original")
  
  def test_recover_key_invalid(self):
    """test recover key with invalid shards"""
    known_key = "1b2ccf87909bd1215858e5c0ec99359cadfcf918a4fac53e3e88e9ec28bec678"
    result = [{'key': '20e2fdc23015c6c78272174be8639b49275e0dbf0479dde60950832ef18bb661', 'index': '9d956693217a5443ba1823151f0924d5a59aaa009cef8cd0f97d3e1a6d279140'}, {'key': '508e1ddc5c06b7e2053d600c4c5da6627778b371784ef712cb8c96f7deae9ce4', 'index': '61a82e98b2c19d13f7edeb1c79c36c40378a5ec2df2e818c6cbd0ead5e548178'}, {'key': '0aca075033a6d257cbac7564c01637b111268f8d42974e5bd765004cc840d359', 'index': '8339e90fc50c9b6b4d650bd03187f4cb4e42e616d1acb6c77dae037764997adb'}, {'key': '4c8a56b19e66a4d533946fe3bb4929556258869f939769514c0abdf8d22d1fa2', 'index': '283985072fcb14bcaf20f5c393d4af5f49a6d2cae472fb28038507f174f7d22d'}, {'key': '2ab718fe611b09eae351a53969364df1bd754f345de87839d22bbcae6b8d091f', 'index': '107dd8993e24875227e024e3352ab7333a766b93cd646f51bc68a2ebc682c64a'}] 
    
    recovered = Kavach.recoverKey(result)
    self.assertNotEqual(recovered["masterKey"], known_key, "Recovered key should not match original")