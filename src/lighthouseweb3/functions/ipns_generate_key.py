from .config import Config
import requests as req

def ipns_generate_key(token: str):
  headers = {
    "Authorization": f"Bearer {token}",
  }
  url = f"{Config.lighthouse_api}/api/ipns/generate_key"
  try:
    response = req.get(url, headers=headers)
  except Exception as e:
    raise Exception("Failed to ipns generate key")

  if response.status_code != 200:
    return response.json()

  return {
    "data": response.json()
  }