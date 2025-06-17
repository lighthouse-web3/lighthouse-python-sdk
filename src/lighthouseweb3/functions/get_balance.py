from .config import Config
import requests as req

def get_balance(token:str):
  headers = {
        "Authorization": f"Bearer {token}",
    }
  url = f"{Config.lighthouse_api}/api/user/user_data_usage"
  try:
    response = req.get(url, headers=headers)
  except Exception as e:
    raise Exception("Failed to get account balance")

  return response.json()