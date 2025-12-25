import json
import time
from typing import List, Dict
from .utils import api_node_handler, is_cid_reg, is_equal

def revoke_access(address: str, cid: str, auth_token: str, revoke_to: List[str]) -> Dict:
    if not is_cid_reg(cid):
        return {
            "isSuccess": False,
            "error": "Invalid CID"
        }

    try:
        node_id = [1, 2, 3, 4, 5]
        node_url = [f"/api/setSharedKey/{elem}" for elem in node_id]

        def request_data(url: str) -> Dict:
            try:
                response = api_node_handler(url, "DELETE", auth_token, {
                    "address": address,
                    "cid": cid,
                    "revokeTo": revoke_to
                })
                return response
            except Exception as error:
                return {"error": error}

        data = []
        for url in node_url:
            response = request_data(url)
            if "error" in response:
                try:
                    error_message = json.loads(response["error"].message)
                except:
                    error_message = str(response["error"])
                return {
                    "isSuccess": False,
                    "error": error_message
                }
            time.sleep(1)
            data.append(response)

        temp = [{**elem, "data": None} for elem in data]
        return {
            "isSuccess": is_equal(*temp),
            "error": None
        }
    except Exception as err:
        return {
            "isSuccess": False,
            "error": str(err)
        } 