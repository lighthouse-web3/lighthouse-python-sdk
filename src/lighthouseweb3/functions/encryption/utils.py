import re
import json
import time
import requests
from typing import Dict, Any
from dataclasses import dataclass
from src.lighthouseweb3.functions.config import Config


def is_cid_reg(cid: str) -> bool:

    pattern = r'Qm[1-9A-HJ-NP-Za-km-z]{44}|b[A-Za-z2-7]{58}|B[A-Z2-7]{58}|z[1-9A-HJ-NP-Za-km-z]{48}|F[0-9A-F]{50}'
    return bool(re.match(pattern, cid))

def is_equal(*objects: Any) -> bool:

    if not objects:
        return True
    first = json.dumps(objects[0], sort_keys=True)
    return all(json.dumps(obj, sort_keys=True) == first for obj in objects)

def api_node_handler(
    endpoint: str,
    verb: str,
    auth_token: str = "",
    body: Any = None,
    retry_count: int = 3
) -> Dict[str, Any]:

    url = f"{Config.is_dev and Config.lighthouse_bls_node_dev or Config.lighthouse_bls_node}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}" if auth_token else ""
    }

    for attempt in range(retry_count):
        try:
            if verb in ["POST", "PUT", "DELETE"] and body is not None:
                response = requests.request(
                    method=verb,
                    url=url,
                    headers=headers,
                    json=body
                )
            else:
                response = requests.request(
                    method=verb,
                    url=url,
                    headers=headers
                )

            if not response.ok:
                if response.status_code == 404:
                    raise Exception(json.dumps({
                        "message": "fetch Error",
                        "statusCode": response.status_code
                    }))
                error_body = response.json()
                raise Exception(json.dumps({
                    **error_body,
                    "statusCode": response.status_code
                }))
            return response.json()
        except Exception as error:
            if "fetch" not in str(error):
                raise
            if attempt == retry_count - 1:
                raise
            time.sleep(1)  