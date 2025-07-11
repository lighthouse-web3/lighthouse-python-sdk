import unittest
import asyncio
import logging
from src.lighthouseweb3 import Kavach
from eth_account.messages import encode_defunct
from web3 import Web3


logger = logging.getLogger(__name__)


class TestAccessControl(unittest.IsolatedAsyncioTestCase):
   """Test cases for the access control module."""
  
   def setUp(self):
       # Use the private key that corresponds to the CID owner address
       # The CID QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH is owned by 0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1
       # We'll use a placeholder private key since we don't have the actual one
       self.private_key = "0x8218aa5dbf4dbec243142286b93e26af521b3e91219583595a06a7765abc9c8b"
       # Use the actual owner address from the API response
       self.signer_address = Web3().eth.account.from_key(self.private_key).address
  
   async def test_invalid_condition(self):
       conditions = [
           {
               "id": 1,
               "chain": "FantomTes",  # Invalid chain name
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           },
           {
               "id": 1,  # Duplicate ID
               "chain": "FantomTest",
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           }
       ]
       result = await Kavach.accessControl(
           address=self.signer_address,
           cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
           auth_token="swrwwr",
           conditions=conditions,
           aggregator="([2] and [1])",
           chain_type="EVM"
       )
       self.assertFalse(result['isSuccess'])
       self.assertIsInstance(result['error'], str)
       self.assertIn("Condition validation error:", result['error'])
  
   async def test_invalid_signature(self):
       conditions = [
           {
               "id": 1,
               "chain": "FantomTest",
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           },
           {
               "id": 2,
               "chain": "FantomTest",
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           }
       ]
       # Use an obviously invalid signature
       invalid_signature = "0xdeadbeef"
       result = await Kavach.accessControl(
           address=self.signer_address,
           cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
           auth_token=invalid_signature,
           conditions=conditions,
           aggregator="([2] and [1])",
           chain_type="EVM"
       )
       self.assertFalse(result['isSuccess'])
       # Accept error as None or str
       self.assertTrue(result['error'] is None or isinstance(result['error'], str))
  
   async def test_data_conditions(self):
       auth_message_result = await Kavach.getAuthMessage(address=self.signer_address)
       self.assertIsNone(auth_message_result['error'])
       message = auth_message_result['message']
       signed_message = "0x" + Web3().eth.account.sign_message(encode_defunct(text=message), private_key=self.private_key).signature.hex()
       conditions = [
           {
               "id": 1,
               "chain": "FantomTest",
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           },
           {
               "id": 2,
               "chain": "FantomTest",
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xf0bc72fa04aea04d04b1fa80b359adb566e1c8b1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           }
       ]
       result = await Kavach.accessControl(
           address=self.signer_address,
           cid="QmPzhJDbMgoxXH7JoRc1roXqkLGtngLiGVhegiDEmmTnbM",
           auth_token=signed_message,
           conditions=conditions,
           aggregator="([2] and [1])",
           chain_type="EVM"
       )
       self.assertIsNone(result['error'])
       self.assertTrue(result['isSuccess'])
  
   async def test_add_new_cid_access_conditions(self):
       auth_message_result = await Kavach.getAuthMessage(address=self.signer_address)
       self.assertIsNone(auth_message_result['error'])
       message = auth_message_result['message']
       signed_message = "0x" + Web3().eth.account.sign_message(encode_defunct(text=message), private_key=self.private_key).signature.hex()
       generate_result = await Kavach.generate(threshold=3, keyCount=5)
       self.assertIn('masterKey', generate_result)
       self.assertIn('keyShards', generate_result)
       conditions = [
           {
               "id": 1,
               "chain": "FantomTest",
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           },
           {
               "id": 2,
               "chain": "FantomTest",
               "method": "balanceOf",
               "standardContractType": "ERC20",
               "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
               "returnValueTest": {"comparator": ">=", "value": "0"},
               "parameters": [":userAddress"],
               "inputArrayType": [],
               "outputType": "uint256"
           }
       ]
       result = await Kavach.accessControl(
           address=self.signer_address,
           cid="QmPzhJDbMgoxXH7JoRc1roXqkLGtngLiGVhegiDEmmTnbM",
           auth_token=signed_message,
           conditions=conditions,
           aggregator="([2] and [1])",
           chain_type="EVM",
           key_shards=generate_result['keyShards'],
           decryption_type="ADDRESS"
       )
       self.assertIsNone(result['error'])
       self.assertTrue(result['isSuccess'])


if __name__ == '__main__':
   unittest.main(verbosity=2)