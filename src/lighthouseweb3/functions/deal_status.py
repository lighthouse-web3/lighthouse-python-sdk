import requests
from .config import Config
from .exceptions import LighthouseAPIError


def get_deal_status(cid: str):
    try:
        url = f"{Config.lighthouse_api}/api/lighthouse/deal_status?cid={cid}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as error:
        raise LighthouseAPIError(error.response.text)
