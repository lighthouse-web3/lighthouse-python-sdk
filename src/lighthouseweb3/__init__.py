#!/usr/bin/env python3

import os
import io
from typing import List
from .functions import upload as d, types as t, deal_status, get_uploads as getUploads, download as _download


class Lighthouse:
    def __init__(self, token: str = ""):
        self.token = token or os.environ.get("LIGHTHOUSE_TOKEN", "")
        if not self.token:
            raise Exception(
                "No token provided: Please provide a token or set the LIGHTHOUSE_TOKEN environment variable"
            )

    def upload(self, source: str) -> t.Upload:
        """
        Upload a file or directory to the Lighthouse.

        :param source: str, path to file or directory
        :return: t.Upload, the upload result
        """
        try:
            return d.upload(source, self.token)
        except Exception as e:
            raise e

    def uploadBlob(self, source: io.BufferedReader, filename: str) -> t.Upload:
        """
        Upload Blob a file or directory to the Lighthouse.

        :param source: str, path to file or directory
        :return: t.Upload, the upload result
        """
        if not (hasattr(source, 'read') and hasattr(source, 'close')):
            raise TypeError("source must have 'read' and 'close' methods")
        try:
            return d.uploadBlob(source, filename, self.token)
        except Exception as e:
            raise e

    @staticmethod
    def downloadBlob(dist: io.BufferedWriter, cid: str, chunk_size=1024*1024*10) -> t.Upload:
        """
        Download Blob a file or directory to the Lighthouse.

        :param source: str, path to file or directory
        :return: t.Upload, the upload result
        """
        if not (hasattr(dist, 'read') and hasattr(dist, 'close')):
            raise TypeError("source must have 'read' and 'close' methods")
        try:
            return _download.download_file_into_writable(cid, dist, chunk_size)
        except Exception as e:
            raise e

    @staticmethod
    def getDealStatus(cid: str) -> List[t.DealData]:
        """
        Get deal status from the Lighthouse.

        :param cid: str, content identifier
        :return: List[t.DealData], list of deal data
        """
        try:
            return deal_status.get_deal_status(cid)
        except Exception as e:
            raise e

    @staticmethod
    def getUploads(publicKey: str, pageNo: int = 1) -> List[t.DealData]:
        """
        Get uploads from the Lighthouse.

        :param publicKey: str, public key
        :param pageNo: int, page number (default: 1)
        :return: List[t.DealData], list of deal data
        """
        try:
            return getUploads.get_uploads(publicKey, pageNo)
        except Exception as e:
            raise e

    @staticmethod
    def download(cid: str) -> bytes:
        """
        Get uploads from the Lighthouse.

        :param publicKey: str, public key
        :param pageNo: int, page number (default: 1)
        :return: List[t.DealData], list of deal data
        """
        try:
            return _download.get_file(cid)
        except Exception as e:
            raise e
