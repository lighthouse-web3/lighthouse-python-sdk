#!/usr/bin/env python3

import os
from .functions import upload as d
from .functions import types as t


class Lighthouse:
    def __init__(self, token: str = ""):
        self.token = token or os.environ.get("LIGHTHOUSE_TOKEN", "")
        if not self.token:
            raise Exception(
                "No token provided: Please provide a token or set the LIGHTHOUSE_TOKEN environment variable"
            )

    def upload(self, source: str) -> t.Upload:
        """
        Upload a file or directory to the lighthouse network
        @params {source}: str, path to file or directory
        """
        try:
            return d.upload(source, self.token)
        except Exception as e:
            raise e
