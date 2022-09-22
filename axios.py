from io import BufferedReader
from typing import Dict, List
import requests as req


class Axios:
    def __init__(self, url: str):
        self.url = url

    def parse_url_params(self, params: Dict[str, str]):
        try:
            if params is not None and isinstance(params, dict):
                for key, value in params.items():
                    self.url += f"&{key}={value}"
        except Exception as e:
            print(e)
            return e

    def get(self, headers: Dict[str, str] = None, **kwargs) -> dict | Exception:
        try:
            self.parse_url_params(kwargs.get("params", None))
            r = req.get(self.url, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(e)
            return e

    def post(
        self, body=None, headers: Dict[str, str] = None, **kwargs
    ) -> dict | Exception:
        try:
            self.parse_url_params(kwargs.get("params", None))
            r = req.post(self.url, data=body, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(e)
            return e

    def read_files(self, files: List[str]) -> List[BufferedReader]:
        file_list = []
        for file in files:
            with open(file, "rb") as f:
                file_list.append(f)
        return file_list

    def post_file(
        self, file: List[str], headers: Dict[str, str] = None, **kwargs
    ) -> dict | Exception:
        try:
            self.parse_url_params(kwargs.get("params", None))
            files = self.read_files(file)
            r = req.post(self.url, files=files, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(e)
            return e
