import json
import time
from typing import Any, Dict, List

from .utils import (
  api_node_handler, 
  is_cid_reg, is_equal
)

def save_shards(
    address: str,
    cid: str,
    auth_token: str,
    key_shards: List[dict],
    share_to: List[str] = None
) -> Dict[str, Any]:
    """
    Save key shards to multiple nodes.
    """
    if share_to is None:
        share_to = []

    # Validate CID
    if not is_cid_reg(cid):
        return {
            "isSuccess": False,
            "error": "Invalid CID"
        }

    # Validate key_shards
    if not isinstance(key_shards, list) or len(key_shards) != 5:
        return {
            "isSuccess": False,
            "error": "keyShards must be an array of 5 objects"
        }

    try:
        node_ids = [1, 2, 3, 4, 5]
        node_urls = [f"/api/setSharedKey/{node_id}" for node_id in node_ids]

        def request_data(url: str, index: int) -> Dict[str, Any]:
            try:
                body = {
                    "address": address,
                    "cid": cid,
                    "payload": key_shards[index]  
                }
                if share_to:
                    body["sharedTo"] = share_to

                response = api_node_handler(
                    url,
                    "POST",
                    auth_token,
                    body
                )
                return response
            except Exception as error:
                return {"error": str(error)}

        data = []
        for index, url in enumerate(node_urls):
            response = request_data(url, index)
            if "error" in response:
                try:
                    error_message = json.loads(response["error"])
                except json.JSONDecodeError:
                    error_message = response["error"]
                return {
                    "isSuccess": False,
                    "error": error_message
                }
            data.append(response)
            time.sleep(1)  

        temp = [{"data": None, **{k: v for k, v in elem.items() if k != "data"}} for elem in data]
        is_success = is_equal(*temp) and data[0].get("message") == "success"

        return {
            "isSuccess": is_success,
            "error": None
        }

    except Exception as err:
        return {
            "isSuccess": False,
            "error": str(err)
        } 