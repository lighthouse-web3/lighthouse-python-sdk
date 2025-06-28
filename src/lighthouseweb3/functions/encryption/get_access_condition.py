from typing import Any
from .utils import api_node_handler

def get_access_condition(cid: str) -> dict[str, Any]:
  try:
    conditions = api_node_handler(f"/api/fileAccessConditions/get/{cid}", "GET")
    return {'data': conditions}
  except Exception as error:
    raise error