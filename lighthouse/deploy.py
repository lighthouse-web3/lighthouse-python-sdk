#!/usr/bin/env python3

from typing import List
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
        file_list: List[str] = []
        # check if source is a directory
        if is_dir(source):
            # walk directory tree and add files to list
            walk_dir_tree(source, file_list)
        else:
            # add file to list
            file_list.append(source)

        # create headers
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "multipart/form-data",
            "Encryption": "false",
            "Mime-Type": "application/octet-stream",
        }
        # upload files
        return axios.post_files(file_list, headers)
    except Exception as e:
        raise e
