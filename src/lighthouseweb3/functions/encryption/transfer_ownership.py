import json
import time
from typing import Any
from .utils import api_node_handler, is_cid_reg, is_equal  

def transfer_ownership(address: str, cid: str, new_owner: str, auth_token: str, reset_shared_to: bool = True) -> dict[str, Any]:
    if not is_cid_reg(cid):
        return {
            "isSuccess": False,
            "error": "Invalid CID"
        }
    
    try:
        node_index_selected = [1, 2, 3, 4, 5]
        node_urls = [f"/api/transferOwnership/{elem}" for elem in node_index_selected]
        
        def request_data(url: str) -> dict:
            try:
                response = api_node_handler(url, "POST", auth_token, {
                    "address": address,
                    "cid": cid,
                    "newOwner": new_owner,
                    "resetSharedTo": reset_shared_to
                })
                return response
            except Exception as error:
                return {"error": str(error)}
        
        data = []
        for url in node_urls:
            response = request_data(url)
            if "error" in response:
                try:
                    error_message = json.loads(response.get("error", "{}"))
                except json.JSONDecodeError:
                    error_message = response.get("error")
                return {
                    "isSuccess": False,
                    "error": error_message
                }
            time.sleep(1)  # Delay between requests
            data.append(response)
        
        return {
            "isSuccess": is_equal(*data) and data[0].get("message") == "success",
            "error": None
        }
    
    except Exception as err:
        return {
            "isSuccess": False,
            "error": str(err)
        }