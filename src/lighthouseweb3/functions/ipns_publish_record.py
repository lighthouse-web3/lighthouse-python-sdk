from .config import Config
import requests as req

def ipns_publish_record(token: str, cid: str, keyName: str):
  headers = {
    "Authorization": f"Bearer {token}",
  }
  url = f"{Config.lighthouse_api}/api/ipns/publish_record?cid={cid}&keyName={keyName}"
  try:
    response = req.get(url, headers=headers)
  except Exception as e:
    raise Exception("Failed to ipns generate key")

  if response.status_code != 200:
    return response.json()

  return {
    "data": response.json()
  }