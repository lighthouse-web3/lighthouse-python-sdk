from .config import Config
import requests as req

def get_ipns_records(token: str):
  headers = {
    "Authorization": f"Bearer {token}",
  }
  url = f"{Config.lighthouse_api}/api/ipns/get_ipns_records"
  try:
    response = req.get(url, headers=headers)
  except Exception as e:
    raise Exception("Failed to get ipns records")

  if response.status_code != 200:
    return response.json()

  return {
    "data": response.json()
  }