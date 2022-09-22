#!/usr/bin/env python3

from typing import Dict, List, Tuple
from .axios import Axios
from .utils import is_dir, walk_dir_tree
from .config import Config
from . import types as t


def deploy(source: str, token: str) -> t.Deploy:
    """
    Deploy a file or directory to the lighthouse network
    @params {source}: str, path to file or directory
    @params {token}: str, lighthouse api token
    """
    try:
        # create http object
        axios = Axios(Config.lighthouse_node + "/api/v0/add")
        # create list of files to upload
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

        # create headers
        headers = {
            "Authorization": f"Bearer {token}",
            # "Content-Type": "multipart/form-data",
            "Encryption": "false",
            "Mime-Type": "application/octet-stream",
        }
        # upload files
        return {"data": axios.post_files(file_dict, headers)}
    except Exception as e:
        raise e
