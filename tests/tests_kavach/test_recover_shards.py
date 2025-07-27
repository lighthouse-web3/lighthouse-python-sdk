import unittest
import logging
from eth_account import Account
from web3 import Web3
from src.lighthouseweb3 import Kavach

class TestRecoverShards(unittest.IsolatedAsyncioTestCase):
    """Test cases for the recoverShards function."""
    
    async def asyncSetUp(self):
        """Set up test fixtures before each test method."""
        private_key = "0x8218aa5dbf4dbec243142286b93e26af521b3e91219583595a06a7765abc9c8b"
        self.signer = Account.from_key(private_key)
        self.kavach = Kavach()
        
    async def test_invalid_signature(self):
        """Test recovery with invalid signature."""
        result = await self.kavach.recoverShards(
            self.signer.address,
            "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQA",
            "signature",
            5
        )
        
        self.assertIsNotNone(result.get('error'))
        self.assertEqual(result['error']['message'], "Invalid Signature")
    
    async def test_save_key(self):
        """Test saving shards successfully."""
        auth_message = await self.kavach.getAuthMessage(self.signer.address)
        
        signed_message = self.signer.sign_message(auth_message['message'])
        
        result = await self.kavach.saveShards(
            self.signer.address,
            "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQA",
            signed_message.signature.hex(),
            [
                {"key": "1", "index": "1"},
                {"key": "2", "index": "2"},
                {"key": "3", "index": "3"},
                {"key": "4", "index": "4"},
                {"key": "5", "index": "5"},
            ]
        )
        
        self.assertTrue(result['is_success'])
        self.assertIsNone(result['error'])
    
    async def test_recover_key_authorized(self):
        """Test authorized shard recovery."""
        auth_message = await self.kavach.getAuthMessage(self.signer.address)
        signed_message = self.signer.sign_message(auth_message['message'])
        
        result = await self.kavach.recoverShards(
            self.signer.address,
            "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQA",
            signed_message.signature.hex(),
            5
        )
        
        self.assertIsNone(result['error'])
        expected_shards = [
            {"index": "1", "key": "1"},
            {"index": "2", "key": "2"},
            {"index": "3", "key": "3"},
            {"index": "4", "key": "4"},
            {"index": "5", "key": "5"},
        ]
        self.assertEqual(result['shards'], expected_shards)
    
    async def test_missing_cid(self):
        """Test recovery with missing CID."""
        auth_message = await self.kavach.getAuthMessage(self.signer.address)
        signed_message = self.signer.sign_message(auth_message['message'])
        
        result = await self.kavach.recoverShards(
            self.signer.address,
            "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQZ",  # Different CID
            signed_message.signature.hex()
        )
        
        self.assertIsNotNone(result['error'])
        self.assertRegex(result['error'].lower(), r'cid not found')
        self.assertEqual(result['shards'], [])
    
    async def test_recover_key_unauthorized(self):
        """Test unauthorized shard recovery."""
        # Create a different signer
        private_key2 = "0x8218aa5dbf4dbec243142286b93e26af521b3e91219583595a06a7765abc9c8f"
        signer2 = Account.from_key(private_key2)
        
        auth_message = await self.kavach.getAuthMessage(signer2.address)
        signed_message2 = signer2.sign_message(auth_message.get('message', ''))
        
        result = await self.kavach.recoverShards(
            signer2.address,
            "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQA",
            signed_message2.signature.hex(),
            5
        )
        
        self.assertEqual(result['shards'], [])
        # Handle nested error structure (adjust based on actual implementation)
        error_message = result.get('error', {}).get('message', {}).get('message', {}).get('message')
        self.assertEqual(error_message, "Access Denied")


if __name__ == '__main__':
    # Set up logging if needed
    logging.basicConfig(level=logging.INFO)
    
    # Run the tests
    unittest.main()