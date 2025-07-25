import unittest
from src.lighthouseweb3 import Kavach


class TestGetAccessCondition(unittest.TestCase):
    def test_access_condition(self):
      condition = Kavach.getAccessCondition("QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH")
      self.assertIsInstance(condition, dict, "condition is a dict")
      self.assertIsInstance(condition.get('data'), dict, "data is a dict")
      self.assertIn("([2] and [1])", str(condition.get('data')))
      self.assertEqual("0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1", condition.get('data').get('owner'))

    def test_access_condition_invalid_cid(self):
      condition = Kavach.getAccessCondition("invalid_cid")
      self.assertIsInstance(condition, dict, "condition is a dict")
      self.assertIsInstance(condition.get('data'), dict, "data is a dict")
      self.assertEqual(condition.get('data').get('conditions'), [], "conditions is a list")

