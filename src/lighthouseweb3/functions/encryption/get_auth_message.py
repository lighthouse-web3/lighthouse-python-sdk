from typing import Any
from .utils import api_node_handler


def get_auth_message(address: str) -> dict[str, Any]:
  try:
    response = api_node_handler(f"/api/message/{address}", "GET")
    return {'message': response[0]['message'], 'error': None}
  except Exception as e:
    return {'message': None, 'error':str(e)}