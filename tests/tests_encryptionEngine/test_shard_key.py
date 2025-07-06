import unittest
import asyncio
import logging
from src.lighthouseweb3 import EncryptionManager

logger = logging.getLogger(__name__)

# class TestShardKey(unittest.TestCase):
#     def test_valid_32_byte_key(self):
#         """Test with a valid 32-byte key."""

#         async def run_test():
#             key = "0xb51cde71e810430c9f657dd24d5ba30b17ec1f86e9f671c7f4cb3d888a4680dd"
#             result = await EncryptionManager.shardKey(key, threshold=3, keyCount=5)
#             self.assertTrue(result['isShardable'])
#             self.assertEqual(len(result['keyShards']), 5)
            
#             for shard in result['keyShards']:
#                 self.assertIn('key', shard)
#                 self.assertIn('index', shard)
#                 self.assertIsInstance(shard['key'], str)
#                 self.assertIsInstance(shard['index'], str)    

#         return asyncio.run(run_test())

    # def test_invalid_key(self):
    #     """Test with an invalid key."""
    #     async def run_test():
    #         key = "e810430c9f657dd24d5ba30b17ec1f86e9f671c7f4cb3d888a4680dd"
    #         result = await EncryptionManager.shardKey(key, threshold=3, keyCount=5)
    #         self.assertFalse(result['isShardable'])
    #         self.assertEqual(result['error'], "Invalid key length")

    #     return asyncio.run(run_test())