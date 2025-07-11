from typing import Any
from .util import api_node_handler


async def get_auth_message(address: str) -> dict[str, Any]:
  try:
    response = await api_node_handler(f"/api/message/{address}", "GET")
    return {'message': response[0]['message'], 'error': None}
  except Exception as e:
    return {'message': None, 'error':str(e)}