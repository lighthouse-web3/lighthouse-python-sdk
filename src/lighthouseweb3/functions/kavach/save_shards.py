import asyncio
from typing import List, Dict, Any, Union
from .util import api_node_handler, is_cid_reg, is_equal
from .types import AuthToken, KeyShard  

async def save_shards(
    address: str,
    cid: str,
    auth_token: AuthToken,
    key_shards: List[KeyShard],
    share_to: List[str] = []
) -> Dict[str, Union[bool, str, None]]:
    
    if not is_cid_reg(cid):
        return {
            "isSuccess": False,
            "error": "Invalid CID"
        }

    if not isinstance(key_shards, list) or len(key_shards) != 5:
        return {
            "isSuccess": False,
            "error": "keyShards must be an array of 5 objects"
        }

    try:
        node_ids = [1, 2, 3, 4, 5]
        node_urls = [f"/api/setSharedKey/{i}" for i in node_ids]

        async def request_data(url: str, index: int) -> Dict[str, Any]:
            try:
                payload = {
                    "address": address,
                    "cid": cid,
                    "payload": key_shards[index]
                }
                if share_to:
                    payload["sharedTo"] = share_to

                response = await api_node_handler(url, "POST", auth_token, payload)
                return response

            except Exception as error:
                return {
                    "error": error
                }

        data = []
        for index, url in enumerate(node_urls):
            response = await request_data(url, index)
            if "error" in response:
                try:
                    return {
                        "isSuccess": False,
                        "error": str(response["error"])
                    }
                except Exception:
                    return {
                        "isSuccess": False,
                        "error": "Unknown error"
                    }
            await asyncio.sleep(1)
            data.append(response)

        temp = [{**elem, "data": None} for elem in data]
        return {
            "isSuccess": is_equal(*temp) and data[0].get("message") == "success",
            "error": None
        }

    except Exception as err:
        return {
            "isSuccess": False,
            "error": str(err)
        }
