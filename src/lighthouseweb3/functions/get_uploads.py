import requests
from .config import Config
from . import types as t


def bytes_to_size(bytes_size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while bytes_size >= 1024 and index < len(units) - 1:
        bytes_size /= 1024
        index += 1
    return f"{round(bytes_size, 2)} {units[index]}"


def get_uploads(publicKey: str, pageNo: int = 1) -> t.UploadsResponseType:
    try:
        url = f"{Config.lighthouse_api}/api/user/files_uploaded?publicKey={publicKey}&pageNo={pageNo}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as error:
        raise Exception(error.response.text)
