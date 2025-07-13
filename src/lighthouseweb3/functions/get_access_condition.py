import httpx
from typing import Any, Dict
from .config import Config

async def get_access_condition(cid: str) -> Dict[str, Any]:
    url = f"{Config.lighthouse_api}/api/fileAccessConditions/get/{cid}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            conditions = response.json()
            return {"data": conditions}
    except httpx.HTTPError as exc:
        raise Exception(f"HTTP error occurred: {exc}") from exc
