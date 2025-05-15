from .config import Config
import requests as req

def create_api_key(publicKey: str, signedMessage: str):
  url = f"{Config.lighthouse_api}/api/auth/create_api_key"

  data = {
    "publicKey": publicKey,
    "signedMessage": signedMessage
  }

  try:
    response = req.post(url, data=data)
  except Exception as e:
    raise Exception("Failed to create api key")

  return response.json()