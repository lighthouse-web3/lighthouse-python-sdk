import unittest
import os
from eth_account.messages import encode_defunct
from web3 import Web3
from src.lighthouseweb3 import Kavach
from src.lighthouseweb3.functions.encryption.utils import api_node_handler


def get_auth_message(public_key: str) -> dict:
    response = api_node_handler(f"/api/message/{public_key}", "GET")
    return response[0]['message']


class TestKavachRevokeAcess(unittest.TestCase):
    def test_revoke_access(self):
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

      result = Kavach.revokeAccess(
        address=public_key,
        cid = "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
        auth_token=f"0x{auth_token}",
        revoke_to=["0x344b0b6C1C5b8f4519db43dFb388b65ecA667243",]
      )

      self.assertTrue(result["isSuccess"])
      self.assertIsNone(result["error"])
    
    def test_revoke_access_invalid_cid(self):
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

      result = Kavach.revokeAccess(
        address=public_key,
        cid = "cid",
        auth_token=f"0x{auth_token}",
        revoke_to=["0x344b0b6C1C5b8f4519db43dFb388b65ecA667243",]
      )

      self.assertFalse(result["isSuccess"])
      self.assertIsNotNone(result["error"])
      self.assertIn(result["error"], "Invalid CID")
    
    def test_revoke_access_invalid_access(self):
      public_key = "0x344b0b6C1C5b8f4519db43dFb388b65ecA667243"

      verification_message = get_auth_message(public_key)
      self.assertIn(
        "Please sign this message to prove you are owner of this account", 
        verification_message, 
        "Owner response should come"
      )

      auth_token = Web3().eth.account.sign_message(
        encode_defunct(text=verification_message), 
        private_key="0x8218aa5dbf4dbec243142286b93e26af521b3e91219583595a06a7765abc9c8a"
      ).signature.hex()

      result = Kavach.revokeAccess(
        address=public_key,
        cid = "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
        auth_token=f"0x{auth_token}",
        revoke_to=["0xEaF4E24ffC1A2f53c07839a74966A6611b8Cb8A1",]
      )

      self.assertFalse(result["isSuccess"])
      self.assertIsNotNone(result["error"])
