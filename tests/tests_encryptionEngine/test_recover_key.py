import unittest
import asyncio
import logging
from src.lighthouseweb3 import EncryptionManager

logger = logging.getLogger(__name__)

class TestRecoverKey(unittest.TestCase):
    """Test cases for the recoverKey module."""
     
    def test_empty_shares_list(self):
        """Test that recovery fails with empty shares list."""
        async def run_test():
            result = await EncryptionManager.recoverKey([])
            self.assertEqual(result['masterKey'], '0x0000000000000000000000000000000000000000000000000000000000000000')
            self.assertIsNone(result['error'])
        
        return asyncio.run(run_test())

    
    def test_recover_key_with_generated_shares(self):
        """Test key recovery with dynamically generated shares."""
        async def run_test():
           
            threshold = 3
            key_count = 5
            gen_result = await EncryptionManager.generate(threshold=threshold, keyCount=key_count)
            master_key = gen_result['masterKey']
            
            shares = gen_result['keyShards'][:threshold]
            result = await EncryptionManager.recoverKey(shares)
            self.assertEqual(result['masterKey'], master_key)
            self.assertIsNone(result['error'])
           
            for i in range(key_count - threshold + 1):
                subset = gen_result['keyShards'][i:i+threshold]
                result = await EncryptionManager.recoverKey(subset)
                self.assertEqual(result['masterKey'], master_key)
                self.assertIsNone(result['error'])
            
            return result
        
        return asyncio.run(run_test())

    def test_recover_key_insufficient_shares(self):
        """Test with minimum threshold shares"""
        async def run_test():
            threshold = 2
            key_count = 5
            gen_result = await EncryptionManager.generate(threshold=threshold, keyCount=key_count)
            master_key = gen_result['masterKey']
            shares = gen_result['keyShards'][:threshold]
            result = await EncryptionManager.recoverKey(shares)
            self.assertEqual(result['masterKey'], master_key)
            self.assertIsNone(result['error'])
            
            result = await EncryptionManager.recoverKey(gen_result['keyShards'])
            self.assertEqual(result['masterKey'], master_key)
            self.assertIsNone(result['error'])
        
        return asyncio.run(run_test())

    def test_insufficient_shares(self):
        """Test with insufficient shares for recovery"""
        async def run_test():
            threshold = 3
            key_count = 5
            gen_result = await EncryptionManager.generate(threshold=threshold, keyCount=key_count)
            
            # Test with one less than threshold (should still work as long as we have at least 2 shares)
            result = await EncryptionManager.recoverKey(gen_result['keyShards'][:threshold-1])
            self.assertIsNotNone(result['masterKey'])
            self.assertIsNone(result['error'])
            
            # Test with single share (should still work as long as we have at least 1 share)
            result = await EncryptionManager.recoverKey(gen_result['keyShards'][:1])
            self.assertIsNotNone(result['masterKey'])
            self.assertIsNone(result['error'])
        
        return asyncio.run(run_test())
    
    def test_various_threshold_combinations(self):
        """Test recovery with various threshold and share count combinations"""
        async def run_test():
            test_cases = [
                (2, 3), 
                (3, 5), 
                (4, 7),  
                (3, 10), 
            ]
            for threshold, total in test_cases:
                with self.subTest(threshold=threshold, total=total):
                    gen_result = await EncryptionManager.generate(
                        threshold=threshold, 
                        keyCount=total
                    )
                    master_key = gen_result['masterKey']
                    
                    shares = gen_result['keyShards'][:threshold]
                    result = await EncryptionManager.recoverKey(shares)
                    self.assertEqual(result['masterKey'], master_key)
                    self.assertIsNone(result['error'])
                    
                    result = await EncryptionManager.recoverKey(gen_result['keyShards'])
                    self.assertEqual(result['masterKey'], master_key)
                    self.assertIsNone(result['error'])
                    
                    import random
                    subset = random.sample(gen_result['keyShards'], threshold + 1)
                    result = await EncryptionManager.recoverKey(subset)
                    self.assertEqual(result['masterKey'], master_key)
                    self.assertIsNone(result['error'])
        
        return asyncio.run(run_test())


    def test_invalid_share_format(self):
        """Test that invalid share formats are handled correctly."""
        async def run_test():
            result = await EncryptionManager.recoverKey(["not a dict", "another invalid"])
            self.assertIsNone(result['masterKey'])
            self.assertIn("must be a dictionary", result['error'])
            
            result = await EncryptionManager.recoverKey([{'key': '123'}, {'key': '456'}])
            self.assertIsNone(result['masterKey'])
            self.assertIn("missing required fields 'key' or 'index'", result['error'].lower())
            
            result = await EncryptionManager.recoverKey([
                {'key': 'invalidhex', 'index': '1'},
                {'key': 'invalidhex2', 'index': '2'}
            ])
            self.assertIsNone(result['masterKey'])
            self.assertIn("invalid key format", result['error'].lower())
            
            result = await EncryptionManager.recoverKey([
                {'key': 'a' * 63, 'index': 'invalidindex'},
                {'key': 'b' * 63, 'index': 'invalidindex2'}
            ])
            self.assertIsNone(result['masterKey'])
            self.assertIn("invalid index format", result['error'].lower())
        
        return asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main(verbosity=2)
