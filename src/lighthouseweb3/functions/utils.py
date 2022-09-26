#!/usr/bin/env python3

from io import BufferedReader
import os
from typing import List, Tuple
from . import types as t

# walk path and return list of file paths
def walk_dir_tree(path: str) -> Tuple[List[str], str]:
    file_list = []
    roots = []
    for root, dirs, files in os.walk(path):
        roots.append(root)
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list, roots[0]


# check if file is a directory
def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def extract_file_name(file: str) -> str:
    return file.split("/")[-1]


def extract_file_name_with_source(file: str, source: str) -> str:
    if source.endswith("/"):
        source = source[: len(source) - 1]
    base = source.split("/")[-1]
    return base + file.split(base)[-1]


def read_files_for_upload(
    files: t.FileDict,
) -> List[Tuple[str, Tuple[str, BufferedReader, str]]]:
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


def close_files_after_upload(
    files: List[Tuple[str, Tuple[str, BufferedReader, str]]]
) -> None:
    for file in files:
        file[1][1].close()
