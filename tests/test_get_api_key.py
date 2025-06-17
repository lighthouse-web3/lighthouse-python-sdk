#!/usr/bin/env python3
import os
import unittest
from src.lighthouseweb3 import Lighthouse
from .setup import parse_env
import requests as req
from src.lighthouseweb3.functions.config import Config
from web3 import Web3
from eth_account.messages import encode_defunct


class TestGetApiKey(unittest.TestCase):

    def test_get_api_key(self):
        """test getApiKey using valid signed message and public key"""
        parse_env()
        publicKey = os.environ.get("PUBLIC_KEY")
        response = req.get(
          f"{Config.lighthouse_api}/api/auth/get_auth_message?publicKey={publicKey}"
        )

        if(response.status_code != 200):
            raise Exception("Failed to get authentication message")
        
        verificationMessage = response.json()

        self.assertIn("Please prove you are the owner", verificationMessage, "Owner response should come")

        encodedMessage = encode_defunct(text=verificationMessage)

      
        signedMessage = Web3().eth.account.sign_message(
            encodedMessage, 
            private_key=os.environ.get("PRIVATE_KEY")
        ).signature.hex()

        res = Lighthouse.getApiKey(publicKey, f"0x{signedMessage}")

        self.assertIsInstance(res, dict, "res is a dict")
        self.assertIsInstance(res.get("data"), dict, "data is a dict")
        self.assertIsInstance(res.get('data').get('apiKey'), str, "apiKey is a string")
    
    def test_get_api_key_with_invalid_message(self):
        """test getApiKey using signed invalid message and public key"""
        parse_env()
        publicKey = os.environ.get("PUBLIC_KEY")
        encodedMessage = encode_defunct(text='random_message')

      
        signedMessage = Web3().eth.account.sign_message(
            encodedMessage, 
            private_key=os.environ.get("PRIVATE_KEY")
        ).signature.hex()

        res = Lighthouse.getApiKey(publicKey, f"0x{signedMessage}")
        self.assertIsInstance(res, dict, "res is a dict")
        self.assertIsInstance(res.get("error"), dict, "data is a dict")
    
    def test_get_api_key_with_random_private_key(self):
        """test getApiKey using signed message with invalid private key and public key"""

        parse_env()
        publicKey = os.environ.get("PUBLIC_KEY")
        response = req.get(
          f"{Config.lighthouse_api}/api/auth/get_auth_message?publicKey={publicKey}"
        )

        if(response.status_code != 200):
            raise Exception("Failed to get authentication message")
        
        verificationMessage = response.json()

        self.assertIn("Please prove you are the owner", verificationMessage, "Owner response should come")

        encodedMessage = encode_defunct(text=verificationMessage)

      
        signedMessage = Web3().eth.account.sign_message(
            encodedMessage, 
            private_key='0x8218aa5dbf4dbec243142286b93e26af521b3e91219583595a06a7765abc9c8b'
        ).signature.hex()

        res = Lighthouse.getApiKey(publicKey, f"0x{signedMessage}")

        self.assertIsInstance(res, dict, "res is a dict")
        self.assertIsInstance(res.get("error"), dict, "data is a dict")