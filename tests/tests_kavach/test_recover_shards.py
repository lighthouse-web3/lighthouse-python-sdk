import unittest
import logging
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
from src.lighthouseweb3 import Kavach
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestRecoverShards(unittest.IsolatedAsyncioTestCase):
    """Test cases for the recoverShards function."""

    def setUp(self):
        self.private_key=os.environ.get("PRIVATE_KEY")
        self.cid=os.environ.get("CID")

    
    async def asyncSetUp(self):
        """Set up test fixtures before each test method."""
        private_key = self.private_key
        self.signer = Account.from_key(private_key)
        self.kavach = Kavach()
        
    async def test_invalid_signature(self):
        """Test recovery with invalid signature."""
        result = await self.kavach.recoverShards(
            self.signer.address,
            self.cid,
            "signature",
            5
        )
        
        self.assertIsNotNone(result.error)
        self.assertIsInstance(result.error, dict)
        self.assertEqual(result.error.get('message'), "Invalid Signature")
    
    async def test_save_key(self):
        """Test saving shards successfully."""
        # Test CID validation
        from src.lighthouseweb3.functions.kavach.util import is_cid_reg        
        auth_message = await self.kavach.getAuthMessage(self.signer.address)
        
        message = auth_message['message']
        signature = f"0x{Web3().eth.account.sign_message(
            encode_defunct(text=message),
            private_key=self.private_key
        ).signature.hex()}"
        
        result = await self.kavach.saveShards(
            self.signer.address,
            self.cid,
            signature, 
            [
                {"key": "1", "index": "1"},
                {"key": "2", "index": "2"},
                {"key": "3", "index": "3"},
                {"key": "4", "index": "4"},
                {"key": "5", "index": "5"},
            ]
        )
        
        
        
        self.assertTrue(result['isSuccess'])
        self.assertIsNone(result['error'])
    
    async def test_recover_key_authorized(self):
        """Test authorized shard recovery."""
        auth_message = await self.kavach.getAuthMessage(self.signer.address)
        
        message = auth_message['message']
        signature = f"0x{Web3().eth.account.sign_message(
            encode_defunct(text=message),
            private_key=self.private_key
        ).signature.hex()}"
        
        result = await self.kavach.recoverShards(
            self.signer.address,
            self.cid,
            signature, 
            5
        )
        
        self.assertIsNone(result.error)
        expected_shards = [
            {"index": "1", "key": "1"},
            {"index": "2", "key": "2"},
            {"index": "3", "key": "3"},
            {"index": "4", "key": "4"},
            {"index": "5", "key": "5"},
        ]
        self.assertEqual(result.shards, expected_shards)
    
    async def test_missing_cid(self):
        """Test recovery with missing CID."""
        auth_message = await self.kavach.getAuthMessage(self.signer.address)
        
        message = auth_message['message']
        signature = f"0x{Web3().eth.account.sign_message(
            encode_defunct(text=message),
            private_key=self.private_key
        ).signature.hex()}"
        
        result = await self.kavach.recoverShards(
            self.signer.address,
            "bafkreiebj4d3f6e6abuxhsrcevhgkypr54335hjucryj3zvivq7hv2nwiqZ",  # Non-existent CID
            signature, 
            3
        )
        
        self.assertIsNotNone(result.error)
        self.assertIsInstance(result.error, dict)
        self.assertIn("message", result.error)
        self.assertEqual(result.shards, [])
    
    async def test_recover_key_unauthorized(self):
        """Test unauthorized shard recovery."""
        private_key2 = "0xbca24fceb5f6c412e401b9ba68b351d811cc0735b059771dfc4e878adb0373ef"
        
        auth_message = await self.kavach.getAuthMessage(self.signer.address)
        
        message = auth_message['message']
        signature2 = f"0x{Web3().eth.account.sign_message(
            encode_defunct(text=message),
            private_key=private_key2
        ).signature.hex()}"
        
        result = await self.kavach.recoverShards(
            self.signer.address,
            self.cid,
            signature2, 
            5
        )
        
        
        self.assertEqual(result.shards, [])
        self.assertIsInstance(result.error, dict)
        self.assertIn("===", result.error.get('message', ''))
        self.assertEqual(result.error.get('statusCode'), 406)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()