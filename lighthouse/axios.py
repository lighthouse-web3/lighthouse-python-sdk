#!/usr/bin/env python3

from io import BufferedReader
from typing import Dict, List, Tuple
import requests as req
from . import types as t
from . import utils


class Axios:
    """It's not axios, it's just a custom extensible wrapper for requests"""

    def __init__(self, url: str):
        self.url = url

    def parse_url_query(self, query: Dict[str, str]):
        try:
            if query is not None and isinstance(query, dict):
                for key, value in query.items():
                    self.url += f"&{key}={value}"
        except Exception as e:
            raise e

    def get(self, headers: Dict[str, str] = None, **kwargs) -> dict | Exception:
        try:
            self.parse_url_query(kwargs.get("query", None))
            r = req.get(self.url, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise e

    def post(
        self, body=None, headers: Dict[str, str] = None, **kwargs
    ) -> dict | Exception:
        try:
            self.parse_url_query(kwargs.get("query", None))
            r = req.post(self.url, data=body, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise e

    def post_files(
        self, file: t.FileDict, headers: Dict[str, str] = None, **kwargs
    ) -> dict | Exception:
        try:
            self.parse_url_query(kwargs.get("query", None))
            files = utils.read_files_for_upload(file)
            r = req.post(self.url, headers=headers, files=files)
            r.raise_for_status()
            utils.close_files_after_upload(files)
            try:
                return r.json()
            except Exception:
                return r.text
        except Exception as e:
            utils.close_files_after_upload(files)
            raise e
