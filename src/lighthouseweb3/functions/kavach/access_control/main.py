from .validator import UpdateConditionSchema as update_condition_schema, AccessConditionSchema as access_condition_schema
from ..types import (AuthToken,
                     Condition,
                     DecryptionType,
                     KeyShard,
                     ChainType,
                     LightHouseSDKResponse)

from src.lighthouseweb3.functions.config import Config
from src.lighthouseweb3.functions.kavach.util import is_equal, is_cid_reg, api_node_handler
from typing import List, Optional

async def access_control(
    address: str,
    cid: str,
    auth_token: AuthToken,
    conditions: List[Condition],
    aggregator: Optional[str] = None,
    chain_type: ChainType = "evm",
    key_shards: List[KeyShard] = [],
    decryption_type: DecryptionType = "ADDRESS"
) -> LightHouseSDKResponse:
    try:
        if not isinstance(key_shards, list) or (
            len(key_shards) != 5 and len(key_shards) != 0
        ):
            raise ValueError("keyShards must be an array of 5 objects")

        if not is_cid_reg(cid):
            raise ValueError("Invalid CID")

        try:
            if len(key_shards) == 5:
                access_condition_schema.parse_obj({
                    "address": address,
                    "cid": cid,
                    "conditions": conditions,
                    "aggregator": aggregator,
                    "decryptionType": decryption_type,
                    "chainType": chain_type,
                    "keyShards": key_shards
                })
            else:
                update_condition_schema.parse_obj({
                    "address": address,
                    "cid": cid,
                    "conditions": conditions,
                    "aggregator": aggregator,
                    "chainType": chain_type
                })
        except ValueError as e:
            raise ValueError(f"Condition validation error: {str(e)}")

        node_ids = [1, 2, 3, 4, 5]
        node_urls = [
            f":900{id}/api/fileAccessConditions/{id}" if Config.is_dev else f"/api/fileAccessConditions/{id}"
            for id in node_ids
        ]

        data = []

        for index, url in enumerate(node_urls):
            try:
                if len(key_shards) == 5:
                    response = await api_node_handler(
                        url, "POST", auth_token, {
                            "address": address,
                            "cid": cid,
                            "conditions": conditions,
                            "aggregator": aggregator,
                            "decryptionType": decryption_type,
                            "chainType": chain_type,
                            "payload": key_shards[index]
                        }
                    )
                else:
                    response = await api_node_handler(
                        url, "PUT", auth_token, {
                            "address": address,
                            "cid": cid,
                            "conditions": conditions,
                            "aggregator": aggregator,
                            "chainType": chain_type
                        }
                    )
            except Exception as e:
                try:
                    error_data = json.loads(str(e))
                except Exception:
                    error_data = {"message": str(e)}
                response = {"isSuccess": False, "error": error_data}

            if response.get("error"):
                time.sleep(1)  # Wait for 1 second before retrying

            data.append(response)

        success = (
            is_equal(*(resp.get("message") for resp in data)) and
            data[0].get("message") == "success"
        )

        return {"isSuccess": success, "error": None}

    except Exception as e:
        try:
            return {"isSuccess": False, "error": json.loads(str(e))}
        except Exception:
            return {"isSuccess": False, "error": {"message": str(e)}}