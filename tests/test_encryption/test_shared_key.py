#!/usr/bin/env python3
import unittest
from src.lighthouseweb3 import Kavach
from py_ecc.bls import G2ProofOfPossession as bls
from typing import List, Dict
from py_ecc.optimized_bls12_381.optimized_curve import curve_order

class TestKavachSharedKey(unittest.TestCase):

    def test_key_shardable_false(self):
        """Test if key is not shardable with invalid input"""
        result = Kavach.sharedKey("invalid_hex")
        self.assertFalse(result["isShardable"], "Key should not be shardable")

    def test_key_shardable_true(self):
        """Test if key is shardable with valid input and correct number of shards"""
        result = Kavach.sharedKey("0b2ccf87909bd1215858e5c0ec99359cadfcf918a4fac53e3e88e9ec28bec678")
        self.assertTrue(result["isShardable"], "Key should be shardable")
        self.assertEqual(len(result["keyShards"]), 5, "Should generate 5 shards")

    def test_master_key_recovery_4_of_5(self):
        """Test master key recovery with 4 out of 5 shards"""
        known_key = "0a16088df55283663f7fea6c5f315bde968024b7ac5d715af0325a5507700e5e"
        result = Kavach.sharedKey(known_key, 3, 5)
        self.assertTrue(result["isShardable"], "Key should be shardable")

        # Recover using 4 shards
        recovered = Kavach.recoverKey([
            result["keyShards"][2],
            result["keyShards"][0],
            result["keyShards"][1],
            result["keyShards"][4]
        ])
        self.assertEqual(recovered["masterKey"], known_key, "Recovered key should match original")

    def test_master_key_recovery_5_of_5(self):
        """Test master key recovery with all 5 shards"""
        known_key = "0a16088df55283663f7fea6c5f315bde968024b7ac5d715af0325a5507700e5e"
        result = Kavach.sharedKey(known_key, 3, 5)
        self.assertTrue(result["isShardable"], "Key should be shardable")

        # Recover using all 5 shards
        recovered =  Kavach.recoverKey([
            result["keyShards"][2],
            result["keyShards"][0],
            result["keyShards"][1],
            result["keyShards"][4],
            result["keyShards"][3]
        ])
        self.assertEqual(recovered["masterKey"], known_key, "Recovered key should match original")

    def test_master_key_recovery_2_of_5(self):
        """Test master key recovery fails with only 2 out of 5 shards"""
        known_key = "0a16088df55283663f7fea6c5f315bde968024b7ac5d715af0325a5507700e5e"
        result = Kavach.sharedKey(known_key, 3, 5)
        self.assertTrue(result["isShardable"], "Key should be shardable")

        # Try to recover with only 2 shards (below threshold)
        recovered =  Kavach.recoverKey([
            result["keyShards"][0],
            result["keyShards"][1]
        ])
        self.assertNotEqual(recovered["masterKey"], known_key, "Recovered key should not match with insufficient shards")