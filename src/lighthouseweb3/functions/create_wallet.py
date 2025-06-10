import requests as req
from .config import Config

from eth_account import Account

def create_wallet(password: str):
  wallet = Account.create()

  url = f"{Config.lighthouse_api}/api/auth/get_auth_message?publicKey={wallet.address}"

  try:
    response = req.get(url)
  except Exception as e:
    raise Exception("Failed to create wallet")

  if response.status_code != 200:
    return response.json()
  
  encrypted_wallet = wallet.encrypt(password)

  del wallet

  return encrypted_wallet