import unittest
import asyncio
import logging
from src.lighthouseweb3 import Kavach

logger = logging.getLogger(__name__)

class TestGenerate(unittest.TestCase):
    """Test cases for the generate module."""
    
    def test_generate_basic(self):
        """Test basic key generation with default parameters."""
        async def run_test():
            result = await Kavach.generate(threshold=2, keyCount=3)
            
            self.assertIn('masterKey', result)
            self.assertIn('keyShards', result)
            
            # Check master key format (hex string with 0x prefix)
            self.assertIsInstance(result['masterKey'], str)
            self.assertTrue(result['masterKey'].startswith('0x'))
            self.assertTrue(all(c in '0123456789abcdef' for c in result['masterKey'][2:]))
            
            # Check key shards
            self.assertEqual(len(result['keyShards']), 3)
            for shard in result['keyShards']:
                self.assertIn('key', shard)
                self.assertIn('index', shard)
                
                # Check key format (hex string with 0x prefix)
                self.assertTrue(shard['key'].startswith('0x'))
                self.assertTrue(all(c in '0123456789abcdef' for c in shard['key'][2:]))
                
                # Check index format (hex string with 0x prefix)
                self.assertTrue(shard['index'].startswith('0x'))
                self.assertTrue(all(c in '0123456789abcdef' for c in shard['index'][2:]))
            
            return result
        
        return asyncio.run(run_test())
    
    def test_generate_custom_parameters(self):
        """Test key generation with custom parameters."""
        async def run_test():
            threshold = 3
            key_count = 5
            
            result = await Kavach.generate(threshold=threshold, keyCount=key_count)
            
            self.assertEqual(len(result['keyShards']), key_count)
            
            # Check all indices are present and unique
            indices = [shard['index'] for shard in result['keyShards']]
            self.assertEqual(len(set(indices)), key_count)  # All unique
            
            # Verify all indices are valid hex strings with 0x prefix
            for index in indices:
                self.assertTrue(index.startswith('0x'))
                self.assertTrue(all(c in '0123456789abcdef' for c in index[2:]))
            
            return result
        
        return asyncio.run(run_test())
    
    def test_invalid_threshold(self):
        """Test that invalid threshold raises an error."""
        async def run_test():
            with self.assertRaises(ValueError) as context:
                await Kavach.generate(threshold=0, keyCount=3)
            self.assertIn("must be positive integers", str(context.exception))
            
            with self.assertRaises(ValueError) as context:
                await Kavach.generate(threshold=4, keyCount=3)
            self.assertIn("must be greater than or equal to threshold", str(context.exception))
        
        return asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main(verbosity=2)
