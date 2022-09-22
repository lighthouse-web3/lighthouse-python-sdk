#!/usr/bin/env python3

import os
from typing import List

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
