import secrets
import logging
from typing import Dict, List, Any
from shard_key import shard_key 
logger = logging.getLogger(__name__)

async def generate(threshold: int = 3, key_count: int = 5) -> Dict[str, Any]:
    """
    Generate threshold cryptography key shards using Shamir's Secret Sharing
    
    Args:
        threshold: Minimum number of shards needed to reconstruct the secret
        key_count: Total number of key shards to generate
        
    Returns:
        {
            "masterKey": "<master private key hex string>",
            "keyShards": [
                {
                    "key": "<shard value hex string>",
                    "index": "<shard index hex string>"
                }
            ]
        }
    """
    logger.info(f"Generating key shards with threshold={threshold}, key_count={key_count}")

    try:
        master_key = secrets.randbits(256)
        result = await shard_key(master_key, threshold, key_count)

        if not result['isShardable']:
            raise ValueError(result['error'])

        return {
            "masterKey": hex(master_key),
            "keyShards": result['keyShards']
        }

    except Exception as e:
        logger.error(f"Error during key generation: {str(e)}")
        raise e
