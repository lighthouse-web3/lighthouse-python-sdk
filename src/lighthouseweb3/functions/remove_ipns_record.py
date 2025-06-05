from .config import Config
import requests as req

def remove_ipns_record(token: str,  keyName: str):
  headers = {
    "Authorization": f"Bearer {token}",
  }
  url = f"{Config.lighthouse_api}/api/ipns/remove_key?keyName={keyName}"
  try:
    response = req.delete(url, headers=headers)
  except Exception as e:
    raise Exception("Failed to remove ipns record")

  if response.status_code != 200:
    return response.json()

  return {
    "data": response.json()
  }