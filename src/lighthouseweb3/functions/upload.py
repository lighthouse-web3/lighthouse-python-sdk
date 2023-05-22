#!/usr/bin/env python3

from io import BufferedReader
from typing import Dict, List, Tuple
from .axios import Axios
from .utils import is_dir, walk_dir_tree, extract_file_name, NamedBufferedReader
from .config import Config
from . import types as t


def upload(source: str | BufferedReader | NamedBufferedReader, token: str, tag: str = "") -> t.Upload:
    """
    Deploy a file or directory to the lighthouse network
    @params {source}: str, path to file or directory
    @params {token}: str, lighthouse api token
    """
    # create headers
    headers = {
        "Authorization": f"Bearer {token}",
        # "Content-Type": "multipart/form-data",
        "Encryption": "false",
        "Mime-Type": "application/octet-stream",
    }
    try:
        # create http object
        axios = Axios(Config.lighthouse_node + "/api/v0/add")
        # create list of files to upload

        if (isinstance(source, str)):
            file_dict: t.FileDict = {}

            # check if source is a directory
            if is_dir(source):
                # walk directory tree and add files to list
                file_dict["files"], root = walk_dir_tree(source)
                file_dict["is_dir"] = True
                file_dict["path"] = root
            else:
                # add file to list
                file_dict["files"] = [source]
                file_dict["is_dir"] = False
                file_dict["path"] = source
            hashData = axios.post_files(file_dict, headers)
        else:
            hashData = axios.post_blob(source, source.name, headers)

        if len(tag):
            _axios = Axios(Config.lighthouse_api_test + "/api/user/create_tag")
            data = _axios.post({
                "tag": tag,
                "cid": hashData.get("Hash")
            }, {
                "Authorization": f"Bearer {token}", })
        return {"data": hashData}
    except Exception as e:
        print(e)
        raise e


def uploadBlob(source:  BufferedReader, filename: str, token: str, tag: str = "") -> t.Upload:
    """
    Upload a Buffer or readable Object
    @params {source}: str, path to file or directory
    @params {token}: str, lighthouse api token
    """
    # create headers
    headers = {
        "Authorization": f"Bearer {token}",
        # "Content-Type": "multipart/form-data",
        "Encryption": "false",
        "Mime-Type": "application/octet-stream",
    }
    try:
        # create http object
        axios = Axios(Config.lighthouse_node + "/api/v0/add")
        # create list of files to upload

        hashData = axios.post_blob(source, filename, headers)
        if len(tag):
            _axios = Axios(Config.lighthouse_api_test + "/api/user/create_tag")
            data = _axios.post({
                "tag": tag,
                "cid": hashData.get("Hash")
            }, {
                "Authorization": f"Bearer {token}", })
        return {"data": hashData}
    except Exception as e:
        print(e)
        raise e
