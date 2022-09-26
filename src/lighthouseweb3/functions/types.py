#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, NewType, List, Tuple, TypedDict


@dataclass
class Deploy(TypedDict):
    """typings for deploy function"""

    data: dict | str


class FileDict(TypedDict):
    """typings for file dict"""

    files: List[str]
    is_dir: bool
    path: str
