#!/usr/bin/env python3


class Config:
    """Config class for lighthouse"""

    # lighthouse_api = "http://13.234.35.183:5050"  # "https://api.lighthouse.storage"
    lighthouse_api = 'https://api.lighthouse.storage'
    lighthouse_node = "https://node.lighthouse.storage"
    lighthouse_bls_node = "https://encryption.lighthouse.storage"
    lighthouse_gateway = "https://gateway.lighthouse.storage/ipfs"


    is_dev = False
    lighthouse_bls_node_dev = "http://enctest.lighthouse.storage" 