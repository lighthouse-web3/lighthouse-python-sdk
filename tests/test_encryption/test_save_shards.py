import unittest
import requests
import os
from eth_account.messages import encode_defunct
from web3 import Web3
from src.lighthouseweb3.functions.config import Config
from src.lighthouseweb3 import Kavach


class TestSaveShards(unittest.TestCase):

    def test_save_shards_successful(self):
        """test save shards for successful key saving"""
        public_key = os.environ.get("PUBLIC_KEY")

        verification_message = Kavach.getAuthMessage(public_key)['message']
        self.assertIn("Please sign this message to prove you are owner of this account", verification_message, "Owner response should come")

        signed_message = Web3().eth.account.sign_message(
            encode_defunct(text=verification_message), 
            private_key=os.environ.get("PRIVATE_KEY")
        ).signature.hex()

        result = Kavach.saveShards(
            address=public_key,
            cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
            auth_token=f"0x{signed_message}",
            key_shards=[
                {"key": "1", "index": "1"},
                {"key": "2", "index": "2"},
                {"key": "3", "index": "3"},
                {"key": "4", "index": "4"},
                {"key": "5", "index": "5"},
            ]
        )

        self.assertTrue(result["isSuccess"])
        self.assertIsNone(result["error"])

    def test_save_shards_invalid_signature(self):
        """test save shards for invalid signature"""
        public_key = os.environ.get("PUBLIC_KEY")


        result = Kavach.saveShards(
            address=public_key,
            cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
            auth_token="signature",
            key_shards=[
                {"key": "1", "index": "1"},
                {"key": "2", "index": "2"},
                {"key": "3", "index": "3"},
                {"key": "4", "index": "4"},
                {"key": "5", "index": "5"},
            ]
        )
        self.assertIsInstance(result["error"], dict)
        self.assertEqual(result["error"].get("message"), "Invalid Signature")

    def test_save_shards_invalid_key_shards_length(self):
        """test save shards for invalid key shards length"""

        public_key = os.environ.get("PUBLIC_KEY")


        verification_message = Kavach.getAuthMessage(public_key)['message']
        self.assertIn("Please sign this message to prove you are owner of this account", verification_message, "Owner response should come")

        signed_message = Web3().eth.account.sign_message(
            encode_defunct(text=verification_message), 
            private_key=os.environ.get("PRIVATE_KEY")
        ).signature.hex()

        result = Kavach.saveShards(
            address=public_key,
            cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQJ",
            auth_token=f"0x{signed_message}",
            key_shards=[
                {"key": "1", "index": "1"},
                {"key": "2", "index": "2"},
                {"key": "3", "index": "3"},
            ]
        )
        self.assertFalse(result["isSuccess"])
        self.assertRegex(result["error"], r"keyShards must be an array of 5 objects")

    def test_save_shards_invalid_cid(self):
        """test save shards for invalid CID"""

        public_key = os.environ.get("PUBLIC_KEY")

        verification_message = Kavach.getAuthMessage(public_key)['message']
        self.assertIn("Please sign this message to prove you are owner of this account", verification_message, "Owner response should come")

        signed_message = Web3().eth.account.sign_message(
            encode_defunct(text=verification_message), 
            private_key=os.environ.get("PRIVATE_KEY")
        ).signature.hex()


        result = Kavach.saveShards(
            address=public_key,
            cid="cid",
            auth_token=f"0x{signed_message}",
            key_shards=[
                {"key": "1", "index": "1"},
                {"key": "2", "index": "2"},
                {"key": "3", "index": "3"},
                {"key": "4", "index": "4"},
                {"key": "5", "index": "5"},
            ]
        )
        self.assertFalse(result["isSuccess"])
        self.assertRegex(result["error"], r"Invalid CID")