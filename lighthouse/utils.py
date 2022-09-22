#!/usr/bin/env python3

from io import BufferedReader
import os
from typing import List, Tuple
from . import types as t

# walk path and return list of file paths
def walk_dir_tree(path: str) -> List[str]:
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# check if file is a directory
def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def extract_file_name(file: str) -> str:
    return file.split("/")[-1]


def extract_file_name_with_source(file: str, source: str) -> str:
    base = source.split("/")[-1]
    return base + file.split(base)[-1]


def read_files_for_upload(files: t.FileDict) -> List[Tuple[BufferedReader]]:
    file_list = []
    for file in files["files"]:
        if files["is_dir"]:
            file_list.append(
                (
                    "file",
                    (
                        extract_file_name_with_source(file, files["path"]),
                        open(file, "rb"),
                        "application/octet-stream",
                    ),
                )
            )
        else:
            file_list.append(
                (
                    "file",
                    (
                        extract_file_name(file),
                        open(file, "rb"),
                        "application/octet-stream",
                    ),
                ),
            )
    return file_list
