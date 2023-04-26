#!/usr/bin/env python3

from typing import List, Dict, Tuple, NewType, TypedDict
from dataclasses import dataclass


@dataclass
class Upload(TypedDict):
    """typings for upload function"""

    data: dict | str


class FileDict(TypedDict):
    """typings for file dict"""

    files: List[str]
    is_dir: bool
    path: str


class DealData(TypedDict):
    """typings for deal Status"""
    chainDealID: str
    endEpoch: str
    publishCID: str
    storageProvider: str
    dealStatus: str
    bundleId: str
    dealUUID: str
    startEpoch: str
    providerCollateral: str
    lastUpdate: int
    dealId: int
    miner: str
    content: int


class FileObject(TypedDict):
    publicKey: str
    fileName: str
    mimeType: str
    txHash: str
    status: str
    createdAt: int
    fileSizeInBytes: str
    cid: str
    id: str
    lastUpdate: int
    encryption: bool


class UploadsResponseType(TypedDict):
    fileList: List[FileObject]
    totalFiles: int
