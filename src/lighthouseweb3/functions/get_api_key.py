from .config import Config
import requests as req

def get_api_key(publicKey: str, signedMessage: str):
  url = f"{Config.lighthouse_api}/api/auth/create_api_key"

  data = {
    "publicKey": publicKey,
    "signedMessage": signedMessage
  }

  try:
    response = req.post(url, data=data)
  except Exception as e:
    raise Exception("Failed to create api key")

  if response.status_code != 200:
    return response.json()

  apiKey = response.json()

  result = {
    "data": {
      "apiKey" : apiKey
    }
  }

  return result