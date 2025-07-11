import re
import json
import asyncio
import aiohttp
from typing import Any, Optional, Union
from urllib.parse import urljoin
from src.lighthouseweb3.functions.config import Config

def is_cid_reg(cid: str) -> bool:
    """Check if string is a valid CID (Content Identifier)"""
    pattern = r'Qm[1-9A-HJ-NP-Za-km-z]{44}|b[A-Za-z2-7]{58}|B[A-Z2-7]{58}|z[1-9A-HJ-NP-Za-km-z]{48}|F[0-9A-F]{50}'
    return bool(re.match(pattern, cid))

def is_equal(*objects: Any) -> bool:
    """Check if all objects are equal by comparing their JSON representations"""
    if not objects:
        return True
    
    first_obj_json = json.dumps(objects[0], sort_keys=True)
    return all(json.dumps(obj, sort_keys=True) == first_obj_json for obj in objects)

async def api_node_handler(
    endpoint: str,
    verb: str,
    auth_token: str = "",
    body: Any = None,
    retry_count: int = 3
) -> Any:
    """
    Handle API requests to node with retry logic
    
    Args:
        endpoint: API endpoint path
        verb: HTTP method (GET, POST, DELETE, PUT)
        auth_token: Bearer token for authentication
        body: Request body for POST/PUT/DELETE requests
        retry_count: Number of retry attempts
    
    Returns:
        JSON response from API
    
    Raises:
        Exception: If request fails after all retries
    """
    verb = verb.upper()
    
    
    base_url = Config.lighthouse_bls_node_dev if Config.is_dev else Config.lighthouse_auth_node
    url = urljoin(base_url, endpoint)
    
        
    headers = {
        "Content-Type": "application/json"
    }
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
 
    json_data = None
    if verb in ["POST", "PUT", "DELETE"] and body is not None:
        json_data = body
    
 
    for i in range(retry_count):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=verb,
                    url=url,
                    headers=headers,
                    json=json_data
                ) as response:
                    
                    if not response.ok:
                        if response.status == 404:
                            raise Exception(json.dumps({
                                "message": "fetch Error",
                                "statusCode": response.status
                            }))
                        
                        try:
                            error_body = await response.json()
                        except:
                            error_body = {"message": "Unknown error"}
                        
                        raise Exception(json.dumps({
                            **error_body,
                            "statusCode": response.status
                        }))
                    
                    return await response.json()
                    
        except Exception as error:
            error_str = str(error)
            if "fetch" not in error_str:
                raise error
            
            if i == retry_count - 1:  # Last attempt
                raise error
                
            # Wait 1 second before retry
            await asyncio.sleep(1)