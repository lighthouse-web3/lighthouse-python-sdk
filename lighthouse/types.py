from dataclasses import dataclass
from typing import Dict, NewType, List, Tuple, TypedDict


@dataclass
class Deploy(TypedDict):
    """typings for deploy function
    """
    data: dict