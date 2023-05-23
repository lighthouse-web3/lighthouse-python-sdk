import requests
import warnings
import io
from .axios import Axios
from .config import Config


# 10MB chunks by default
def download_file_into_writable(cid: str, writable_object: io.BufferedWriter, chunk_size=1024*1024*10):
    url = f"{Config.lighthouse_gateway}/{cid}"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:  # filter out keep-alive new chunks
                writable_object.write(chunk)
    return {"data": {"Hash": cid, "Size": writable_object.tell()}}


def get_url_body(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    return response.content, response.headers


def get_file(cid: str) -> (bytes, str):
    try:
        url = f"{Config.lighthouse_gateway}/{cid}"

        (body, headers) = get_url_body(url)

        # show a warning if the file is greater then 2GB
        if (int(headers['Content-Length']) > 1024*1024*1024*2):
            warnings.warn(
                "This content of the file is grater then 2GB, use `downloadBlob` instead", UserWarning)
        return (body, headers['Content-Type'])
    except requests.HTTPError as error:
        raise Exception(error.response.text)


def getTaggedCid(tag: str, token: str):

    _axios = Axios(
        f"{Config.lighthouse_api}/api/user/get_tag_details?tag={tag}")
    data = _axios.get({
        "Authorization": f"Bearer {token}"
    })
    return data

    # return {"data": {"Hash": cid, "Size": writable_object.tell()}}
