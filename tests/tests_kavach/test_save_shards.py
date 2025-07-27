import unittest
import logging
from src.lighthouseweb3 import Kavach
from web3 import Web3
from eth_account.messages import encode_defunct
import os


logger = logging.getLogger(__name__)


class TestSaveShards(unittest.IsolatedAsyncioTestCase):
   """Test cases for the saveShards function."""


   def setUp(self):
       self.cid = os.environ.get("CID")
       self.private_key = os.environ.get("PRIVATE_KEY")
       self.signer_address = Web3().eth.account.from_key(self.private_key).address

      
   async def test_invalid_signature(self):
       """Test saveShards with invalid signature."""
       result = await Kavach.saveShards(
           address=self.signer_address,
           cid=self.cid,
           auth_token="signature",
           key_shards=[
               {"key": "1", "index": "1"},
               {"key": "2", "index": "2"},
               {"key": "3", "index": "3"},
               {"key": "4", "index": "4"},
               {"key": "5", "index": "5"},
           ]
       )
      
       self.assertFalse(result['isSuccess'])
       self.assertTrue(result['error'] is None or isinstance(result['error'], str))


   async def test_save_key_success(self):
       """Test successful key saving."""
       auth_message_result = await Kavach.getAuthMessage(address=self.signer_address)
       self.assertIsNone(auth_message_result['error'])
       message = auth_message_result['message']
       signature = f"0x{Web3().eth.account.sign_message(
           encode_defunct(text=message),
           private_key=self.private_key
       ).signature.hex()}"
       print(signature)
       result = await Kavach.saveShards(
           address=self.signer_address,
           cid=self.cid,
           auth_token=signature,
           key_shards=[
               {"key": "1", "index": "1"},
               {"key": "2", "index": "2"},
               {"key": "3", "index": "3"},
               {"key": "4", "index": "4"},
               {"key": "5", "index": "5"},
           ]
       )
       print(result)
       self.assertTrue(result['isSuccess'])
       self.assertIsNone(result['error'])


   async def test_save_key_insufficient_shards(self):
       """Test saving key with insufficient shards (should fail)."""
       auth_message_result = await Kavach.getAuthMessage(address=self.signer_address)
       self.assertIsNone(auth_message_result['error'])
       auth_message = auth_message_result['message']
       signature = "0x" + Web3().eth.account.sign_message(encode_defunct(text=auth_message), private_key=self.private_key).signature.hex()
      
       result = await Kavach.saveShards(
           address=self.signer_address,
           cid=self.cid,
           auth_token=signature,
           key_shards=[
               {"key": "1", "index": "1"},
               {"key": "2", "index": "2"},
               {"key": "3", "index": "3"},
           ]
       )
      
       self.assertFalse(result['isSuccess'])
       self.assertRegex(str(result['error']).lower(), r'keyshards must be an array of 5 objects')


   async def test_invalid_cid(self):
       """Test saving key with invalid CID."""
       auth_message_result = await Kavach.getAuthMessage(address=self.signer_address)
       self.assertIsNone(auth_message_result['error'])
       auth_message = auth_message_result['message']
       signature = "0x" + Web3().eth.account.sign_message(encode_defunct(text=auth_message), private_key=self.private_key).signature.hex()
      
       result = await Kavach.saveShards(
           address=self.signer_address,
           cid=self.cid,
           auth_token=signature,
           key_shards=[
               {"key": "1", "index": "1"},
               {"key": "2", "index": "2"},
               {"key": "3", "index": "3"},
               {"key": "4", "index": "4"},
               {"key": "5", "index": "5"},
           ]
       )
      
       self.assertFalse(result['isSuccess'])
       self.assertRegex(str(result['error']).lower(), r'invalid cid')


if __name__ == '__main__':
   unittest.main(verbosity=2)

