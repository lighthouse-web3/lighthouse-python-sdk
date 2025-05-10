#!/usr/bin/env python3

from io import BufferedReader
import json
from typing import Optional, Dict, Any, Union
import requests as req
from requests.exceptions import RequestException
from . import utils


class Axios:
    """
    A custom extensible wrapper for requests library.
    Provides simplified HTTP client functionality with proper error handling.
    """

    def __init__(self, url: str):
        """
        Initialize Axios instance.
        
        :param url: Base URL for requests
        :raises ValueError: If URL is empty or invalid
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")
        self.url = url

    def parse_url_query(self, query: Optional[Dict[str, Any]]) -> None:
        """
        Parse and append query parameters to URL.
        
        :param query: Dictionary of query parameters
        :raises ValueError: If query parameters are invalid
        """
        try:
            if query is not None:
                if not isinstance(query, dict):
                    raise ValueError("Query must be a dictionary")
                for key, value in query.items():
                    self.url += f"&{key}={value}"
        except Exception as e:
            raise ValueError(f"Failed to parse query parameters: {str(e)}")

    def get(self, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform GET request.
        
        :param headers: Request headers
        :param kwargs: Additional parameters including query
        :return: JSON response
        :raises RequestException: If request fails
        """
        try:
            self.parse_url_query(kwargs.get("query"))
            r = req.get(self.url, headers=headers, timeout=30)  # Added timeout
            r.raise_for_status()
            return r.json()
        except req.exceptions.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON response: {str(e)}")
        except RequestException as e:
            raise RequestException(f"GET request failed: {str(e)}")

    def post(self, body: Optional[Any] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Perform POST request.
        
        :param body: Request body
        :param headers: Request headers
        :param kwargs: Additional parameters including query
        :return: JSON response
        :raises RequestException: If request fails
        """
        try:
            self.parse_url_query(kwargs.get("query"))
            r = req.post(self.url, data=body, headers=headers, timeout=30)  # Added timeout
            r.raise_for_status()
            return r.json()
        except req.exceptions.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON response: {str(e)}")
        except RequestException as e:
            raise RequestException(f"POST request failed: {str(e)}")

    def post_files(self, file: Dict[str, Any], headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Upload files via POST request.
        
        :param file: File information dictionary
        :param headers: Request headers
        :param kwargs: Additional parameters including query
        :return: JSON response
        :raises RequestException: If request fails
        """
        files = None
        try:
            self.parse_url_query(kwargs.get("query"))
            files = utils.read_files_for_upload(file)
            r = req.post(self.url, headers=headers, files=files, timeout=30)  # Added timeout
            r.raise_for_status()
            
            # Always ensure files are closed
            if files:
                utils.close_files_after_upload(files)
            
            try:
                return r.json()
            except req.exceptions.JSONDecodeError:
                # Handle special case where response contains multiple lines
                temp = r.text.split("\n")
                return json.loads(temp[-2])  # Use -2 index instead of len(temp) - 2
        except Exception as e:
            # Ensure files are closed even if an error occurs
            if files:
                utils.close_files_after_upload(files)
            raise RequestException(f"File upload failed: {str(e)}")

    def post_blob(self, file: BufferedReader, filename: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Upload blob data via POST request.
        
        :param file: BufferedReader instance containing file data
        :param filename: Name of the file
        :param headers: Request headers
        :param kwargs: Additional parameters including query
        :return: JSON response
        :raises RequestException: If request fails
        :raises ValueError: If file or filename is invalid
        """
        if not isinstance(file, BufferedReader):
            raise ValueError("file must be a BufferedReader instance")
        if not filename or not isinstance(filename, str):
            raise ValueError("filename must be a non-empty string")

        try:
            self.parse_url_query(kwargs.get("query"))
            files = [(
                "file",
                (
                    utils.extract_file_name(filename),
                    file.read(),
                    "application/octet-stream",
                ),
            )]
            
            r = req.post(self.url, headers=headers, files=files, timeout=30)  # Added timeout
            r.raise_for_status()
            
            try:
                return r.json()
            except req.exceptions.JSONDecodeError:
                # Handle special case where response contains multiple lines
                temp = r.text.split("\n")
                return json.loads(temp[-2])  # Use -2 index instead of len(temp) - 2
        except Exception as e:
            raise RequestException(f"Blob upload failed: {str(e)}")
        finally:
            # Always ensure file is closed
            file.close()
