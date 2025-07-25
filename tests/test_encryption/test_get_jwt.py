import unittest
import os
from eth_account.messages import encode_defunct
from web3 import Web3
from src.lighthouseweb3 import Kavach


class TestKavachGetJWT(unittest.TestCase):
    def test_get_jwt(self):
      public_key = os.environ.get("PUBLIC_KEY")

      verification_message = Kavach.getAuthMessage(public_key)['message']
      self.assertIn(
        "Please sign this message to prove you are owner of this account", 
        verification_message, 
        "Owner response should come"
      )

      auth_token = Web3().eth.account.sign_message(
        encode_defunct(text=verification_message), 
        private_key='0x8218aa5dbf4dbec243142286b93e26af521b3e91219583595a06a7765abc9c8b'
      ).signature.hex()

      jwt = Kavach.getJWT(
        address=public_key,
        payload=f"0x{auth_token}"
      )

      self.assertIsNotNone(jwt["JWT"])
      self.assertIsNotNone(jwt["refreshToken"])
        
    def test_get_jwt_invalid_signature(self):
      public_key = os.environ.get("PUBLIC_KEY")

      jwt = Kavach.getJWT(
        address=public_key,
        payload="invalid_signature"
      )

      self.assertIsNone(jwt["JWT"])
      self.assertIsNotNone(jwt["error"])


     