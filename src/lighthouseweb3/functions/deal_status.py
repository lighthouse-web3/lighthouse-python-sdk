import requests
from typing import List
from .config import Config
from . import types as t


def get_deal_status(cid: str) -> List[t.DealData]:
    try:
        url = f"{Config.lighthouse_api_v2}/api/lighthouse/deal_status?cid={cid}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as error:
        raise Exception(error.response.text)
