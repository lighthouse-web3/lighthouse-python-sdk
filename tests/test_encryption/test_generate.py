
import unittest
from src.lighthouseweb3 import Kavach
from unittest.mock import patch

class TestGenerateKey(unittest.TestCase):
  def test_generate_key_success(self):
    result = Kavach.generate()
    self.assertIsInstance(result["masterKey"], str, "masterKey should be a string")
    self.assertEqual(len(result["keyShards"]), 5, "keyShards should have length 5")

  def test_threshold_greater_than_key_count(self):
    with self.assertRaises(ValueError) as context:
        Kavach.generate(threshold=6, key_count=5)
    self.assertEqual(
        str(context.exception),
        "threshold must be less than or equal to key_count",
        "Expected ValueError for threshold > key_count"
    )