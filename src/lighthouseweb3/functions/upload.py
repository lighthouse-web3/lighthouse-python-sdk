#!/usr/bin/env python3

from io import BufferedReader
from typing import Dict, List, Tuple, Union, Any
from .axios import Axios
from .utils import is_dir, walk_dir_tree, extract_file_name, NamedBufferedReader
from .config import Config


def upload(source: Union[str, BufferedReader], token: str, tag: str = "") -> Dict[str, Any]:
    """
    Deploy a file or directory to the lighthouse network.

    :param source: Path to file/directory or BufferedReader instance
    :param token: Lighthouse API token
    :param tag: Optional tag for the upload
    :return: Dictionary containing upload response data
    :raises ValueError: If source or token is invalid
    :raises Exception: If upload fails
    """
    if not token or not isinstance(token, str):
        raise ValueError("Token must be a non-empty string")

    if not source:
        raise ValueError("Source must be provided")

    # Create headers with proper typing
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "Encryption": "false",
        "Mime-Type": "application/octet-stream",
    }

    try:
        # Create HTTP object
        axios = Axios(Config.lighthouse_node + "/api/v0/add")

        if isinstance(source, str):
            file_dict: Dict[str, Union[List[str], bool, str]] = {}

            # Check if source is a directory
            if is_dir(source):
                # Walk directory tree and add files to list
                files, root = walk_dir_tree(source)
                file_dict["files"] = files
                file_dict["is_dir"] = True
                file_dict["path"] = root
            else:
                # Add single file
                file_dict["files"] = [source]
                file_dict["is_dir"] = False
                file_dict["path"] = source

            hash_data = axios.post_files(file_dict, headers)
        else:
            if not hasattr(source, 'name'):
                raise ValueError("Source object must have a 'name' attribute")
            hash_data = axios.post_blob(source, source.name, headers)

        # Create tag if provided
        if tag:
            tag_axios = Axios(Config.lighthouse_api + "/api/user/create_tag")
            tag_axios.post(
                body={
                    "tag": tag,
                    "cid": hash_data.get("Hash")
                },
                headers={"Authorization": f"Bearer {token}"}
            )

        return {"data": hash_data}
    except Exception as e:
        # Don't print the error, just raise it with context
        raise Exception(f"Upload failed: {str(e)}")


def uploadBlob(source: BufferedReader, filename: str, token: str, tag: str = "") -> Dict[str, Any]:
    """
    Upload a Buffer or readable Object to the lighthouse network.

    :param source: BufferedReader instance containing file data
    :param filename: Name of the file to be uploaded
    :param token: Lighthouse API token
    :param tag: Optional tag for the upload
    :return: Dictionary containing upload response data
    :raises ValueError: If parameters are invalid
    :raises Exception: If upload fails
    """
    if not isinstance(source, BufferedReader):
        raise ValueError("Source must be a BufferedReader instance")
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    if not token or not isinstance(token, str):
        raise ValueError("Token must be a non-empty string")

    # Create headers with proper typing
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "Encryption": "false",
        "Mime-Type": "application/octet-stream",
    }

    try:
        # Create HTTP object
        axios = Axios(Config.lighthouse_node + "/api/v0/add")
        hash_data = axios.post_blob(source, filename, headers)

        # Create tag if provided
        if tag:
            tag_axios = Axios(Config.lighthouse_api + "/api/user/create_tag")
            tag_axios.post(
                body={
                    "tag": tag,
                    "cid": hash_data.get("Hash")
                },
                headers={"Authorization": f"Bearer {token}"}
            )

        return {"data": hash_data}
    except Exception as e:
        # Don't print the error, just raise it with context
        raise Exception(f"Blob upload failed: {str(e)}")
