#!/usr/bin/env python3

from io import BufferedReader
from typing import Dict, List, Tuple
from .axios import Axios
from .utils import is_dir, walk_dir_tree, extract_file_name, NamedBufferedReader
from .config import Config
from . import types as t


def upload(source: str | BufferedReader | NamedBufferedReader, token: str) -> t.Upload:
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
            return {"data": axios.post_files(file_dict, headers)}
        else:
            return {"data": axios.post_blob(source, headers)}
    except Exception as e:
        print(e)
        raise e
