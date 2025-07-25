from .utils import api_node_handler

def get_jwt(address: str, payload: str, use_as_refresh_token: bool = False, chain: str = "ALL") -> dict:
    try:
        if not use_as_refresh_token:
            data = api_node_handler(
                "/api/message/get-jwt", "POST", "",
                {"address": address, "signature": payload, "chain": chain}
            )
        else:
            data = api_node_handler(
                "/api/message/get-jwt", "PUT", "",
                {"address": address, "refreshToken": payload}
            )
        return {"JWT": data["token"], "refreshToken": data["refreshToken"], "error": None}
    except Exception as e:
        return {"JWT": None, "error": "Invalid Signature"}