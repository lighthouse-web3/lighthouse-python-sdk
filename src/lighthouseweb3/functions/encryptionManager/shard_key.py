import secrets
import logging
from typing import Dict, List, Any
from config import PRIME
logger = logging.getLogger(__name__)


def evaluate_polynomial(coefficients: List[int], x: int, prime: int) -> int:
    """
    Evaluate a polynomial with given coefficients at point x.
    msk[0] is constant term (the secret), msk[1] is x coefficient, etc.
    
    Args:
        coefficients: List of coefficients where coefficients[0] is the constant term
        x: Point at which to evaluate the polynomial
        prime: Prime number for the finite field
        
    Returns:
        {
            "isShardable": true,
            "keyShards": [
                { "key": "<shard key string>", "index": "<index string>" }
            ]
        }
    """
    result = 0
    x_power = 1 # x^0 = 1

    for coefficient in coefficients:
        result = (result + coefficient * x_power) % prime
        x_power = (x_power * x) % prime
    
    return result

def validate_key(key: str) -> bool:
    """
    Validate that the given key is a valid 32-byte (64 hex char) string.
    """
    try:
        bytes.fromhex(key)
        return len(key) == 64
    except ValueError:
        return False

async def shard_key(key: str, threshold: int = 3, key_count: int = 5) -> Dict[str, Any]:
    """
    Generate threshold cryptography key shards using Shamir's Secret Sharing
    
    Args:
        key: The key to be shared
        threshold: Minimum number of shards needed to reconstruct the secret
        key_count: Total number of key shards to generate
        
    Returns:
        {
            "isShardable": true,
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
        msk=[]
        idVec=[]
        secVec=[]

        if threshold > key_count:
            raise ValueError("key_count must be greater than or equal to threshold")
        if threshold < 1 or key_count < 1:
            raise ValueError("threshold and key_count must be positive integers")


        msk.append(key)

        used_ids = set()
        
        for i in range(key_count):
            while True:
                id_vec = secrets.randbits(32)
                if id_vec != 0 and id_vec not in used_ids:
                    idVec.append(id_vec)
                    used_ids.add(id_vec)
                    break
        
        for i in range(key_count):
            y = evaluate_polynomial(msk, idVec[i], PRIME)
            secVec.append(y)

        result = {
            "isShardable": True,
            "keyShards": [{"key": hex(secVec[i]), "index": hex(idVec[i])} for i in range(key_count)]
        }
    except Exception as e:
        logger.error(f"Error generating key shards: {str(e)}")
        result = {
            "isShardable": False,
            "error": str(e)
        }

    return result
