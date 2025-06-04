import requests
from .config import Config


def bytes_to_size(bytes_size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while bytes_size >= 1024 and index < len(units) - 1:
        bytes_size /= 1024
        index += 1
    return f"{round(bytes_size, 2)} {units[index]}"


def get_uploads(token: str, lastKey: int = None) :
    headers = {
        "Authorization": f"Bearer {token}",
    }

    try:
        url = f"{Config.lighthouse_api}/api/user/files_uploaded?lastKey={lastKey}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as error:
        raise Exception(error.response.text)
