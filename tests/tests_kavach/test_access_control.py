import unittest
import asyncio
from eth_account import Account
from eth_account.messages import encode_defunct
from src.lighthouseweb3 import Kavach


class TestAccessControl(unittest.IsolatedAsyncioTestCase):
    """Test class for AccessControl functionality"""
    
    async def asyncSetUp(self):
        """Setup test environment"""
        # Create signer with the same private key as in JS test
        self.private_key = "0x8218aa5dbf4dbec243142286b93e26af521b3e91219583595a06a7765abc9c8b"
        self.signer = Account.from_key(self.private_key)
        self.address = self.signer.address

    async def test_invalid_condition(self):
        """Test invalid condition validation"""
        result = await Kavach.accessControl(
            address=self.address,
            cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
            auth_token="swrwwr",
            conditions=[
                {
                    "id": 1,
                    "chain": "FantomTes",  # Invalid chain name
                    "method": "balanceOf",
                    "standardContractType": "ERC20",
                    "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
                    "returnValueTest": {"comparator": ">=", "value": "0"},
                    "parameters": [":userAddress"],
                },
                {
                    "id": 1,  # Duplicate ID
                    "chain": "FantomTest",
                    "method": "balanceOf",
                    "standardContractType": "ERC20",
                    "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
                    "returnValueTest": {"comparator": ">=", "value": "0"},
                    "parameters": [":userAddress"],
                },
            ],
            aggregator="([2] and [1])"
        )
        
        self.assertIsInstance(result["error"], str)
        self.assertIn("Condition validation error:", result["error"])

    # async def test_invalid_signature(self):
    #     """Test invalid signature handling"""
    #     result = await Kavach.accessControl(
    #         address=self.address, 
    #         cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
    #         auth_token="swrwwr",  # Invalid signature
    #         conditions=[
    #             {
    #                 "id": 1,
    #                 "chain": "FantomTest",
    #                 "method": "balanceOf",
    #                 "standardContractType": "ERC20",
    #                 "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
    #                 "returnValueTest": {"comparator": ">=", "value": "0"},
    #                 "parameters": [":userAddress"],
    #             },
    #             {
    #                 "id": 2,
    #                 "chain": "FantomTest",
    #                 "method": "balanceOf",
    #                 "standardContractType": "ERC20",
    #                 "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
    #                 "returnValueTest": {"comparator": ">=", "value": "0"},
    #                 "parameters": [":userAddress"],
    #             },
    #         ],
    #         aggregator="([2] and [1])"
    #     )
        
    #     self.assertIsInstance(result["error"], dict)
    #     self.assertIn("invalid signature", result["error"]["message"].lower())

    # async def test_data_conditions(self):
    #     """Test valid data conditions"""
    #     # Get auth message and sign it
    #     auth_message = await Kavach.getAuthMessage(address=self.address)
    #     message_to_sign = encode_defunct(text=auth_message["message"])
    #     signed_message = self.signer.sign_message(message_to_sign)
        
    #     result = await Kavach.accessControl(
    #         address=self.address,
    #         cid="QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
    #         auth_token=signed_message.signature.hex(),
    #         conditions=[
    #             {
    #                 "id": 1,
    #                 "chain": "FantomTest",
    #                 "method": "balanceOf",
    #                 "standardContractType": "ERC20",
    #                 "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
    #                 "returnValueTest": {"comparator": ">=", "value": "0"},
    #                 "parameters": [":userAddress"],
    #             },
    #             {
    #                 "id": 2,
    #                 "chain": "FantomTest",
    #                 "method": "balanceOf",
    #                 "standardContractType": "ERC20",
    #                 "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
    #                 "returnValueTest": {"comparator": ">=", "value": "0"},
    #                 "parameters": [":userAddress"],
    #             },
    #         ],
    #         aggregator="([2] and [1])"
    #     )
        
    #     self.assertIsNone(result["error"])
    #     self.assertTrue(result["isSuccess"])

    # async def test_add_new_cid_access_conditions(self):
    #     """Test adding new CID access conditions with key shards"""
    #     # Get auth message and sign it
    #     auth_message = await Kavach.getAuthMessage(address=self.address)
    #     message_to_sign = encode_defunct(text=auth_message["message"])
    #     signed_message = self.signer.sign_message(message_to_sign)
        
    #     # Generate key shards (adjust according to your actual generate function)
    #     key_generation_result = await Kavach.generate(3, 5)
    #     master_key = key_generation_result["masterKey"]
    #     key_shards = key_generation_result["keyShards"]
        
    #     result = await Kavach.accessControl(
    #         address=self.address,
    #         cid="QmPzhJDbMgoxXH7JoRc1roXqkLGtngLiGVhegiDEmmTnbM",
    #         auth_token=signed_message.signature.hex(),
    #         conditions=[
    #             {
    #                 "id": 1,
    #                 "chain": "FantomTest",
    #                 "method": "balanceOf",
    #                 "standardContractType": "ERC20",
    #                 "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
    #                 "returnValueTest": {"comparator": ">=", "value": "0"},
    #                 "parameters": [":userAddress"],
    #             },
    #             {
    #                 "id": 2,
    #                 "chain": "FantomTest",
    #                 "method": "balanceOf",
    #                 "standardContractType": "ERC20",
    #                 "contractAddress": "0xF0Bc72fA04aea04d04b1fA80B359Adb566E1c8B1",
    #                 "returnValueTest": {"comparator": ">=", "value": "0"},
    #                 "parameters": [":userAddress"],
    #             },
    #         ],
    #         aggregator="([2] and [1])",
    #         chain_type="EVM",
    #         key_shards=key_shards,
    #         decryption_type="ADDRESS"
    #     )
        
    #     self.assertIsNone(result["error"])
    #     self.assertTrue(result["isSuccess"])


# Additional test runner for individual test execution
if __name__ == "__main__":
    unittest.main(verbosity=2)