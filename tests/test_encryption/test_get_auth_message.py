import unittest
import os
from src.lighthouseweb3 import Kavach

class TestGetAuthMessage(unittest.TestCase):

  def test_get_auth_message(self):
    auth_message = Kavach.getAuthMessage(address=os.environ.get("PUBLIC_KEY"))
    self.assertIn("Please sign this message to prove you are owner of this account", auth_message['message'], "Owner response should come")
    self.assertEqual(None, auth_message['error'])

  def test_get_auth_message_invalid_address(self):

    auth_message = Kavach.getAuthMessage(address="0x9a40b8EE3B8Fe7eB621cd142a651560Fa7")
    self.assertEqual(None, auth_message['message'])
    self.assertNotEqual(None, auth_message['error'])
    self.assertIn("invalid address", str(auth_message["error"]).lower())