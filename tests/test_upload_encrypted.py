#!/usr/bin/env python3
import os
import io
import unittest
from src.lighthouseweb3 import Lighthouse
from eth_account.messages import encode_defunct
from web3 import Web3
from src.lighthouseweb3 import Kavach

class TestUploadEncrypted(unittest.TestCase):

  def get_auth_token(self,public_key, private_key):
      verification_message = Kavach.getAuthMessage(public_key)['message']

      auth_token = Web3().eth.account.sign_message(
        encode_defunct(text=verification_message), 
        private_key=private_key
      ).signature.hex()

      jwt = Kavach.getJWT(
         address=public_key,
         payload=f"0x{auth_token}"
      )

      return jwt["JWT"]


  def test_upload_encrypted(self):
    public_key = os.environ.get("PUBLIC_KEY")
    private_key = os.environ.get("PRIVATE_KEY")


    l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))

    r = l.uploadEncrypted("tests/testdir/testfile.txt", public_key, self.get_auth_token(public_key, private_key))

    self.assertIsInstance(r, dict, "data is a dict")
    self.assertIsInstance(r.get("data"), list, "data is a dict")
    self.assertIsInstance(r.get("data")[0], dict, "data is a dict")
    self.assertIsInstance(r.get("data")[0].get("Name"), str, "data is a dict")
    self.assertIsInstance(r.get("data")[0].get("Hash"), str, "data is a dict")
    self.assertIsInstance(r.get("data")[0].get("Size"), str, "data is a dict")
  
  def test_upload_encrypted_invalid_token(self):
    """test upload encrypted file with invalid auth token"""
    public_key = os.environ.get('PUBLIC_KEY')

    l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))

    with self.assertRaises(Exception) as e:
        l.uploadEncrypted(
            "tests/testdir/testfile.txt",
            public_key,
            "invalid_auth_token"
        )
    self.assertEqual(str(e.exception), 'Error encrypting file')

  def test_upload_encrypted_invalid_api_key(self):
    """test upload encrypted file with invalid api key"""
    public_key = os.environ.get("PUBLIC_KEY")
    private_key = os.environ.get("PRIVATE_KEY")

    l = Lighthouse('invalid_api_key')
    auth_token = self.get_auth_token(public_key, private_key)

    with self.assertRaises(Exception):
        l.uploadEncrypted(
            "tests/testdir/testfile.txt",
            public_key,
            auth_token
        )