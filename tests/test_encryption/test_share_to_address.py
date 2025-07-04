import unittest
import os
from eth_account.messages import encode_defunct
from web3 import Web3
from src.lighthouseweb3.functions.config import Config
from src.lighthouseweb3 import Kavach
from src.lighthouseweb3.functions.encryption.utils import api_node_handler


def get_auth_message(public_key: str) -> dict:
    response = api_node_handler(f"/api/message/{public_key}", "GET")
    return response[0]['message']

class TestKavach(unittest.TestCase):
    def test_share_to_address(self):
      public_key = os.environ.get("PUBLIC_KEY")

      verification_message = get_auth_message(public_key)
      self.assertIn(
        "Please sign this message to prove you are owner of this account", 
        verification_message, 
        "Owner response should come"
      )
      
      auth_token = Web3().eth.account.sign_message(
        encode_defunct(text=verification_message), 
        private_key=os.environ.get("PRIVATE_KEY")
      ).signature.hex()

      result = Kavach.shareToAddress(
        address=public_key,
        cid = "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
        auth_token=f"0x{auth_token}",
        share_to=["0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1"]
      )

      self.assertIsNone(result["error"])
      self.assertTrue(result["isSuccess"])
    
    def test_share_to_address_invalid_address(self):
      public_key = os.environ.get("PUBLIC_KEY")

      verification_message = get_auth_message(public_key)
      self.assertIn(
        "Please sign this message to prove you are owner of this account", 
        verification_message, 
        "Owner response should come"
      )

      auth_token = Web3().eth.account.sign_message(
        encode_defunct(text=verification_message), 
        private_key=os.environ.get("PRIVATE_KEY")
      ).signature.hex()


      result = Kavach.shareToAddress(
        address='0x344b0b6C1C5b8f4519db43dFb388b65ecA667243',
        cid = "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
        auth_token=f"0x{auth_token}",
        share_to=["0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1"]
      )

      self.assertFalse(result["isSuccess"])
      self.assertIsNotNone(result["error"])

      


      
        