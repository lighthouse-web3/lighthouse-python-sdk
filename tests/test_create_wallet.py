#!/usr/bin/env python3
import unittest
from src.lighthouseweb3 import Lighthouse
from eth_account import Account


class TestCreateWallet(unittest.TestCase):

    def test_create_wallet(self):
        """test static create wallet function"""
        password = 'TestPassword'
        encrypted_wallet = Lighthouse.createWallet(password)
        
        private_key = Account.decrypt(encrypted_wallet, password)
        wallet = Account.from_key(private_key)
        self.assertEqual(wallet.address, f"0x{encrypted_wallet['address']}", 'Both public key must be same')
    
    def test_create_wallet_different_password(self):
        """test static create wallet function use different password for decryption"""
        encrypted_wallet = Lighthouse.createWallet('TestPassword')
        with self.assertRaises(Exception) as context:
          private_key = Account.decrypt(encrypted_wallet, 'RandomPassword')
          self.assertIn("valueerror", str(context).lower())
        