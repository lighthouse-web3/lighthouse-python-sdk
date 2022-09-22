#!/usr/bin/env python3

from io import BufferedReader
from typing import Dict, List, Tuple
import requests as req
from . import types as t


class Axios:
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

    def extract_file_name(self, file: str) -> str:
        return file.split("/")[-1]

    def extract_file_last_dir(self, file: str) -> str:
        return file.split("/")[-2]

    def read_files(self, files: t.FileDict) -> List[Tuple[BufferedReader]]:
        file_list = []
        for file in files["files"]:
            if files["is_dir"]:
                file_list.append(
                    (
                        "file",
                        (
                            file,
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
                            self.extract_file_name(file),
                            open(file, "rb"),
                            "application/octet-stream",
                        ),
                    ),
                )
        return file_list

    def post_files(
        self, file: t.FileDict, headers: Dict[str, str] = None, **kwargs
    ) -> dict | Exception:
        try:
            self.parse_url_query(kwargs.get("query", None))
            files = self.read_files(file)
            r = req.post(self.url, headers=headers, files=files)
            r.raise_for_status()
            try:
                return r.json()
            except Exception:
                return r.text
        except Exception as e:
            raise e
