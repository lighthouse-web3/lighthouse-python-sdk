import unittest
import asyncio
import logging
from src.lighthouseweb3 import EncryptionManager

logger = logging.getLogger(__name__)

class TestGenerate(unittest.TestCase):
    """Test cases for the generate module."""
    
    def test_generate_basic(self):
        """Test basic key generation with default parameters."""
        async def run_test():
            result = await EncryptionManager.generate(threshold=2, keyCount=3)
            
            self.assertIn('masterKey', result)
            self.assertIn('keyShards', result)
            
            self.assertIsInstance(result['masterKey'], str)
            self.assertTrue(result['masterKey'].startswith('0x'))
            hex_str = result['masterKey'][2:]  
            if len(hex_str) % 2 != 0:
                hex_str = '0' + hex_str
            try:
                bytes.fromhex(hex_str)
            except ValueError:
                self.fail(f"Invalid hex string: {result['masterKey']}")
            
            self.assertEqual(len(result['keyShards']), 3)
            for shard in result['keyShards']:
                self.assertIn('key', shard)
                self.assertIn('index', shard)
                
                self.assertTrue(shard['key'].startswith('0x'))
                hex_str = shard['key'][2:]  
                if len(hex_str) % 2 != 0:
                    hex_str = '0' + hex_str
                try:
                    bytes.fromhex(hex_str)
                except ValueError:
                    self.fail(f"Invalid hex string in key: {shard['key']}")
                
                self.assertTrue(shard['index'].startswith('0x'))
                try:
                    int(shard['index'], 16)
                except ValueError:
                    self.fail(f"Invalid index format (not a valid hex number): {shard['index']}")
            
            return result
        
        return asyncio.run(run_test())
    
    def test_generate_custom_parameters(self):
        """Test key generation with custom parameters."""
        async def run_test():
            threshold = 3
            key_count = 5
            
            result = await EncryptionManager.generate(threshold=threshold, keyCount=key_count)
            
            self.assertEqual(len(result['keyShards']), key_count)
            
            indices = [shard['index'] for shard in result['keyShards']]
            self.assertEqual(len(set(indices)), key_count)  
            
            for shard in result['keyShards']:
                self.assertTrue(shard['key'].startswith('0x'))
                key_hex = shard['key'][2:]  
                if len(key_hex) % 2 != 0:
                    key_hex = '0' + key_hex
                try:
                    bytes.fromhex(key_hex)
                except ValueError:
                    self.fail(f"Invalid hex string in key: {shard['key']}")
                
                
                index = shard['index']
                self.assertTrue(index.startswith('0x'))
                try:
                    int(index, 16) 
                except ValueError:
                    self.fail(f"Invalid index format (not a valid hex number): {index}")
            
            return result
        
        return asyncio.run(run_test())
    
    def test_invalid_threshold(self):
        """Test that invalid threshold raises an error."""
        async def run_test():
            with self.assertRaises(ValueError) as context:
                await EncryptionManager.generate(threshold=0, keyCount=3)
            self.assertIn("must be positive integers", str(context.exception))
            
            with self.assertRaises(ValueError) as context:
                await EncryptionManager.generate(threshold=4, keyCount=3)
            self.assertIn("must be greater than or equal to threshold", str(context.exception))
        
        return asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main(verbosity=2)
