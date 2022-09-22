#!/usr/bin/env python3

import lighthouse.deploy as d
from lighthouse import types as t


class Lighthouse:
    def __init__(self, token: str):
        self.token = token

    def deploy(self, source: str) -> t.Deploy:
        """
        Deploy a file or directory to the lighthouse network
        @params {source}: str, path to file or directory
        """
        try:
            return d.deploy(source, self.token)
        except Exception as e:
            raise e
