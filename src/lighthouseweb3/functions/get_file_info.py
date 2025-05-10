from .config import Config
import requests as req

def get_file_info(cid: str):
  url = f"{Config.lighthouse_api}/api/lighthouse/file_info?cid={cid}"
  try:
    response = req.get(url)
  except Exception as e:
    raise Exception("Failed to get file metadata")

  return response.json()