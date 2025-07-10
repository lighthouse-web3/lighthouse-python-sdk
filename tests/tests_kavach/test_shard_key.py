import unittest
import asyncio
import logging
from src.lighthouseweb3 import Kavach

logger = logging.getLogger(__name__)

class TestShardKey(unittest.TestCase):
    """Test cases for the shardKey function."""

    def test_shardKey_valid_32_byte_key(self):
        """Test shardKey with valid 32-byte keys."""
        async def run_test():
            valid_key = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            result = await Kavach.shardKey(valid_key, threshold=2, keyCount=3)
            
            self.assertTrue(result['isShardable'])
            self.assertIn('keyShards', result)
            self.assertEqual(len(result['keyShards']), 3)
            
            for shard in result['keyShards']:
                self.assertIn('key', shard)
                self.assertIn('index', shard)
                self.assertTrue(shard['key'].startswith('0x'))
                self.assertTrue(shard['index'].startswith('0x'))
                self.assertTrue(all(c in '0123456789abcdef' for c in shard['key'][2:]))
                self.assertTrue(all(c in '0123456789abcdef' for c in shard['index'][2:]))
            
            valid_key_with_prefix = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            result2 = await Kavach.shardKey(valid_key_with_prefix, threshold=2, keyCount=3)
            
            self.assertTrue(result2['isShardable'])
            self.assertEqual(len(result2['keyShards']), 3)
            
            return result
            
        return asyncio.run(run_test())

    def test_shardKey_invalid_keys(self):
        """Test shardKey with invalid keys."""
        async def run_test():
            short_key = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd"
            with self.assertRaises(ValueError) as context:
                await Kavach.shardKey(short_key, threshold=2, keyCount=3)
            self.assertIn("Invalid key format", str(context.exception))
            
            long_key = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef12"
            with self.assertRaises(ValueError) as context:
                await Kavach.shardKey(long_key, threshold=2, keyCount=3)
            self.assertIn("Invalid key format", str(context.exception))
            
            malformed_key = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdefg"
            with self.assertRaises(ValueError) as context:
                await Kavach.shardKey(malformed_key, threshold=2, keyCount=3)
            self.assertIn("Invalid key format", str(context.exception))
            
            with self.assertRaises(ValueError) as context:
                await Kavach.shardKey("", threshold=2, keyCount=3)
            self.assertIn("Invalid key format", str(context.exception))
            
            invalid_hex = "xyz4567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            with self.assertRaises(ValueError) as context:
                await Kavach.shardKey(invalid_hex, threshold=2, keyCount=3)
            self.assertIn("Invalid key format", str(context.exception))
            
        return asyncio.run(run_test())

    def test_shardKey_threshold_keyCount_combinations(self):
        """Test various threshold and keyCount combinations."""
        async def run_test():
            valid_key = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            
            result1 = await Kavach.shardKey(valid_key, threshold=1, keyCount=1)
            self.assertTrue(result1['isShardable'])
            self.assertEqual(len(result1['keyShards']), 1)
            
            result2 = await Kavach.shardKey(valid_key, threshold=2, keyCount=3)
            self.assertTrue(result2['isShardable'])
            self.assertEqual(len(result2['keyShards']), 3)
            
            result3 = await Kavach.shardKey(valid_key, threshold=3, keyCount=5)
            self.assertTrue(result3['isShardable'])
            self.assertEqual(len(result3['keyShards']), 5)
            
            result4 = await Kavach.shardKey(valid_key, threshold=4, keyCount=4)
            self.assertTrue(result4['isShardable'])
            self.assertEqual(len(result4['keyShards']), 4)
            
            result5 = await Kavach.shardKey(valid_key, threshold=5, keyCount=10)
            self.assertTrue(result5['isShardable'])
            self.assertEqual(len(result5['keyShards']), 10)
            
            indices = [shard['index'] for shard in result5['keyShards']]
            self.assertEqual(len(set(indices)), 10)
            
            return result5
            
        return asyncio.run(run_test())


    def test_shardKey_index_uniqueness(self):
        """Test that all generated indices are unique and non-zero."""
        async def run_test():
            valid_key = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            

            result = await Kavach.shardKey(valid_key, threshold=3, keyCount=20)
            
            self.assertTrue(result['isShardable'])
            self.assertEqual(len(result['keyShards']), 20)
            
            indices = [shard['index'] for shard in result['keyShards']]
            self.assertEqual(len(set(indices)), 20)
       
            for index in indices:
                self.assertNotEqual(index, '0x0')
         
                self.assertNotEqual(int(index, 16), 0)
            
            return result
            
        return asyncio.run(run_test())

    def test_shardKey_hex_format_consistency(self):
        """Test that all returned values are properly formatted hex strings."""
        async def run_test():
            valid_key = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            
            result = await Kavach.shardKey(valid_key, threshold=2, keyCount=4)
            
            self.assertTrue(result['isShardable'])
            
            for shard in result['keyShards']:
                key = shard['key']
                index = shard['index']
                

                self.assertTrue(key.startswith('0x'))
                self.assertTrue(index.startswith('0x'))
                

                self.assertTrue(all(c in '0123456789abcdef' for c in key[2:]))
                self.assertTrue(all(c in '0123456789abcdef' for c in index[2:]))
                
                try:
                    int(key, 16)
                    int(index, 16)
                except ValueError:
                    self.fail(f"Invalid hex format: key={key}, index={index}")
            
            return result
            
        return asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main(verbosity=2)