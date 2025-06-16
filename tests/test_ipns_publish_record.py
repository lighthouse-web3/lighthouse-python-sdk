#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env


class TestIPNSPublishRecord(unittest.TestCase):

    def test_ipns_publish_record(self):
      """test ipns_publish_record function"""
      parse_env()

      l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
      res = l.generateKey()

      self.assertIsInstance(res, dict, "result is a dict")
      self.assertIsInstance(res.get("data"), dict , "data is a dict")
      self.assertIsInstance(res.get("data").get("ipnsName"), str , "ipnsName is a str")
      self.assertIsInstance(res.get("data").get("ipnsId"), str , "ipnsId is a dict")

      record = l.publishRecord(
        'QmeMsykMDyD76zpAbinCy1cjb1KL6CVNBfB44am15U1XHh', 
        res.get('data').get('ipnsName')
      )

      self.assertIsInstance(record, dict, "record is a dict")
      self.assertIsInstance(record.get("data"), dict, "data is a dict")
      self.assertIsInstance(record.get("data").get("Name"), str, "name is a str")
      self.assertIsInstance(record.get("data").get("Value"), str, "value is a str")
      self.assertEqual(record.get("data").get("Value"), "/ipfs/QmeMsykMDyD76zpAbinCy1cjb1KL6CVNBfB44am15U1XHh")
    
    def test_ipns_publish_record_invalid_token(self):
      """test ipns_generate_key with invalid token"""
      parse_env()
      l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
      res = l.generateKey()

      self.assertIsInstance(res, dict, "result is a dict")
      self.assertIsInstance(res.get("data"), dict , "data is a dict")
      self.assertIsInstance(res.get("data").get("ipnsName"), str , "ipnsName is a str")
      self.assertIsInstance(res.get("data").get("ipnsId"), str , "ipnsId is a dict")

      l = Lighthouse("invalid_token")
      with self.assertRaises(Exception) as context:
        l.publishRecord(
          'QmeMsykMDyD76zpAbinCy1cjb1KL6CVNBfB44am15U1XHh', 
          res.get('data').get('ipnsName')
        )
        self.assertIn("authentication failed", str(context.exception).lower())
    
    def test_ipns_publish_record_invalid_cid(self):
      """test ipns_generate_key with invalid cid"""
      l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
      res = l.generateKey()

      self.assertIsInstance(res, dict, "result is a dict")
      self.assertIsInstance(res.get("data"), dict , "data is a dict")
      self.assertIsInstance(res.get("data").get("ipnsName"), str , "ipnsName is a str")
      self.assertIsInstance(res.get("data").get("ipnsId"), str , "ipnsId is a dict")

      record = l.publishRecord(
        'invalid_cid', 
        res.get('data').get('ipnsName')
      )
      self.assertIsInstance(record, dict, "record is a dict")
      self.assertIsInstance(record.get("error"), list, "error is a list")
      self.assertEqual(record.get("error")[0]['message'], 'Something went wrong.' )
    
    def test_ipns_publish_record_invalid_key_name(self):
      """test ipns_generate_key with invalid key name"""
      parse_env()

      l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
      res = l.generateKey()

      self.assertIsInstance(res, dict, "result is a dict")
      self.assertIsInstance(res.get("data"), dict , "data is a dict")
      self.assertIsInstance(res.get("data").get("ipnsName"), str , "ipnsName is a str")
      self.assertIsInstance(res.get("data").get("ipnsId"), str , "ipnsId is a dict")

      record = l.publishRecord(
        'QmeMsykMDyD76zpAbinCy1cjb1KL6CVNBfB44am15U1XHh', 
        'invalid_key_name'
      )
      self.assertIsInstance(record, dict, "record is a dict")
      self.assertIsInstance(record.get("error"), list, "error is a list")
      self.assertEqual(record.get("error")[0]['message'], 'Something went wrong.' )