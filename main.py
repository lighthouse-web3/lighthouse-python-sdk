#!/usr/bin/env python3

import os
import lighthouse.deploy as d
from lighthouse import types as t


class Lighthouse:
    def __init__(self, token: str = ""):
        self.token = token or os.environ.get("LIGHTHOUSE_TOKEN", "")
        if not self.token:
            raise Exception(
                "No token provided: Please provide a token or set the LIGHTHOUSE_TOKEN environment variable"
            )

    def deploy(self, source: str) -> t.Deploy:
        """
        Deploy a file or directory to the lighthouse network
        @params {source}: str, path to file or directory
        """
        try:
            return d.deploy(source, self.token)
        except Exception as e:
            raise e
