import json
import time

from typing import List, Dict, Any
from .utils import is_equal, is_cid_reg, api_node_handler

def share_to_address(address: str, cid: str, auth_token: Dict[str, Any], share_to: List[str]) -> Dict[str, Any]:
    if not is_cid_reg(cid):
        return {
            "isSuccess": False,
            "error": "Invalid CID"
        }
    
    try:
        node_id = [1, 2, 3, 4, 5]
        node_url = [f"/api/setSharedKey/{elem}" for elem in node_id]
        
        def request_data(url: str) -> Dict[str, Any]:
            try:
                response = api_node_handler(url, "PUT", auth_token, {
                    "address": address,
                    "cid": cid,
                    "shareTo": share_to
                })
                return response
            except Exception as error:
                return {"error": str(error)}
        
        data = []
        for url in node_url:
            response = request_data(url)
            if "error" in response:
                try:
                    error_message = json.loads(response.get("error", {}))
                except json.JSONDecodeError:
                    error_message = response.get("error")
                return {
                    "isSuccess": False,
                    "error": error_message
                }
            time.sleep(1)  
            data.append(response)
        
        temp = [{**elem, "data": None} for elem in data]
        return {
            "isSuccess": is_equal(*temp) and temp[0].get("message") == "success",
            "error": None
        }
    
    except Exception as err:
        return {
            "isSuccess": False,
            "error": str(err)
        }