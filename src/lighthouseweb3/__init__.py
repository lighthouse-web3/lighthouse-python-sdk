#!/usr/bin/env python3

import os
import io
from .functions import upload as d,deal_status, get_uploads as getUploads, download as _download


class Lighthouse:
    def __init__(self, token: str = ""):
        self.token = token or os.environ.get("LIGHTHOUSE_TOKEN", "")
        if not self.token:
            raise Exception(
                "No token provided: Please provide a token or set the LIGHTHOUSE_TOKEN environment variable"
            )

    def upload(self, source: str, tag: str = ''):
        """
        Upload a file or directory to the Lighthouse.

        :param source: str, path to file or directory
        :param tag: str, optional tag for the upload
        :return: t.Upload, the upload result
        :raises ValueError: If source path is invalid or doesn't exist
        :raises Exception: If upload fails
        """
        if not source or not isinstance(source, str):
            raise ValueError("Source path must be a non-empty string")

        if not os.path.exists(source):
            raise ValueError(f"Source path does not exist: {source}")

        try:
            return d.upload(source, self.token, tag)
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def uploadBlob(self, source: io.BufferedReader, filename: str, tag: str = ''):
        """
        Upload Blob a file or directory to the Lighthouse.

        :param source: io.BufferedReader, file-like object to upload
        :param filename: str, name of the file to be uploaded
        :param tag: str, optional tag for the upload
        :return: t.Upload, the upload result
        :raises TypeError: If source is not a proper file-like object
        :raises ValueError: If filename is invalid
        """
        if not isinstance(source, io.BufferedReader):
            raise TypeError("source must be an instance of io.BufferedReader")

        if not filename or not isinstance(filename, str):
            raise ValueError("filename must be a non-empty string")

        if not (hasattr(source, 'read') and hasattr(source, 'close')):
            raise TypeError("source must have 'read' and 'close' methods")

        try:
            return d.uploadBlob(source, filename, self.token, tag)
        except Exception as e:
            raise Exception(f"Failed to upload blob: {str(e)}")

    @staticmethod
    def downloadBlob(dist: io.BufferedWriter, cid: str, chunk_size=1024*1024*10):
        """
        Download a Blob (file or directory) from the Lighthouse.

        :param dist: BufferedWriter, destination to write the downloaded data
        :param cid: str, Content Identifier for the data to be downloaded
        :param chunk_size: int, size of chunks in which the file will be downloaded (default: 10MB)
        :return: t.Upload, the download result
        :raises TypeError: If dist doesn't have required write and close methods
        :raises ValueError: If cid is empty or invalid
        """
        if not (hasattr(dist, 'write') and hasattr(dist, 'close')):
            raise TypeError("dist must have 'write' and 'close' methods")
        
        if not cid or not isinstance(cid, str):
            raise ValueError("Invalid CID provided")

        try:
            return _download.download_file_into_writable(cid, dist, chunk_size)
        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")
            
    @staticmethod
    def getDealStatus(cid: str):
        """
        Get deal status from the Lighthouse.

        :param cid: str, content identifier
        :return: List[t.DealData], list of deal data
        :raises ValueError: If CID is invalid
        :raises Exception: If fetching deal status fails
        """
        if not cid or not isinstance(cid, str):
            raise ValueError("CID must be a non-empty string")

        try:
            return deal_status.get_deal_status(cid)
        except Exception as e:
            raise Exception(f"Failed to get deal status: {str(e)}")

    @staticmethod
    def getUploads(publicKey: str, pageNo: int = 1):
        """
        Get uploads from the Lighthouse.

        :param publicKey: str, public key
        :param pageNo: int, page number (default: 1)
        :return: List[t.DealData], list of deal data
        :raises ValueError: If publicKey is invalid or pageNo is less than 1
        :raises Exception: If fetching uploads fails
        """
        if not publicKey or not isinstance(publicKey, str):
            raise ValueError("Public key must be a non-empty string")

        if not isinstance(pageNo, int) or pageNo < 1:
            raise ValueError("Page number must be a positive integer")

        try:
            return getUploads.get_uploads(publicKey, pageNo)
        except Exception as e:
            raise Exception(f"Failed to get uploads: {str(e)}")

    @staticmethod
    def download(cid: str):
        """
        Download content from the Lighthouse using its Content Identifier (CID).

        :param cid: str, Content Identifier for the data to be downloaded
        :param useCidAsTag: bool, flag to use CID as a tag (default: False)
        :return: bytes, the downloaded content
        """
        try:
            return _download.get_file(cid)
        except Exception as e:
            raise e

    def getTagged(self, tag: str):
        """
        Retrieve an upload from the Lighthouse using its tag.

        :param tag: str, tag associated with the file or directory
        :return: t.Upload, the upload result
        """
        try:
            return _download.getTaggedCid(tag, self.token)
        except Exception as e:
            raise e

