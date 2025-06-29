import secrets
import logging
from typing import Dict, List, Any
from .config import PRIME
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
        The result of the polynomial evaluation modulo prime
    """
    result = 0
    x_power = 1 # x^0 = 1

    for coefficient in coefficients:
        result = (result + coefficient * x_power) % prime
        x_power = (x_power * x) % prime
    
    return result

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

    msk=[]
    idVec=[]
    secVec=[]

    if threshold > key_count:
        raise ValueError("key_count must be greater than or equal to threshold")
    if threshold < 1 or key_count < 1:
        raise ValueError("threshold and key_count must be positive integers")


    msk = [secrets.randbits(256) for _ in range(threshold)]
    master_key = msk[0]

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
        "masterKey": hex(master_key),
        "keyShards": [{"key": hex(secVec[i]), "index": hex(idVec[i])} for i in range(key_count)]
    }
    return result
