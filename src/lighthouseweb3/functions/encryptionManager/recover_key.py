from typing import List, Dict, Any
import logging
from .config import PRIME

logger = logging.getLogger(__name__)

from typing import Tuple

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean algorithm to find modular inverse.
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        A tuple (g, x, y) such that a*x + b*y = g = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a: int, m: int) -> int:
    """Find the modular inverse of a mod m."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def lagrange_interpolation(shares: List[Dict[str, str]], prime: int) -> int:
    """
    Reconstruct the secret using Lagrange interpolation.
    
    Args:
        shares: List of dictionaries with 'key' and 'index' fields
        prime: The prime number used in the finite field
        
    Returns:
        The reconstructed secret as integer
        
    Raises:
        ValueError: If there are duplicate indices
    """
        
    points = []
    seen_indices = set()
    
    for i, share in enumerate(shares):
        try:
            key_str, index_str = validate_share(share, i)
            x = int(index_str, 16)
            
            if x in seen_indices:
                raise ValueError(f"Duplicate share index found: 0x{x:x}")
            seen_indices.add(x)
            
            y = int(key_str, 16)
            points.append((x, y))
        except ValueError as e:
            raise ValueError(f"Invalid share at position {i}: {e}")
    

    secret = 0
    
    for i, (x_i, y_i) in enumerate(points):
        # Calculate the Lagrange basis polynomial L_i(0)
        # Evaluate at x=0 to get the constant term
        numerator = 1
        denominator = 1
        
        for j, (x_j, _) in enumerate(points):
            if i != j:
                numerator = (numerator * (-x_j)) % prime
                denominator = (denominator * (x_i - x_j)) % prime
    
        try:
            inv_denominator = modinv(denominator, prime)
        except ValueError as e:
            raise ValueError(f"Error in modular inverse calculation: {e}")
            
        term = (y_i * numerator * inv_denominator) % prime
        secret = (secret + term) % prime
    
    return secret

def validate_share(share: Dict[str, str], index: int) -> Tuple[str, str]:
    """Validate and normalize a single share.
    
    Args:
        share: Dictionary containing 'key' and 'index' fields
        index: Position of the share in the input list (for error messages)
        
    Returns:
        Tuple of (normalized_key, normalized_index) as strings without '0x' prefix
        
    Raises:
        ValueError: If the share is invalid
    """
    if not isinstance(share, dict):
        raise ValueError(f"Share at index {index} must be a dictionary")
        
    if 'key' not in share or 'index' not in share:
        raise ValueError(f"Share at index {index} is missing required fields 'key' or 'index'")
        
    key_str = str(share['key']).strip().lower()
    index_str = str(share['index']).strip().lower()

    if key_str.startswith('0x'):
        key_str = key_str[2:]
    if index_str.startswith('0x'):
        index_str = index_str[2:]
        
    
    if not key_str:
        raise ValueError(f"Empty key in share at index {index}")
    if not all(c in '0123456789abcdef' for c in key_str):
        raise ValueError(f"Invalid key format in share at index {index}: must be a valid hex string")
    
    if len(key_str) % 2 != 0:
        key_str = '0' + key_str
        
    if not index_str:
        raise ValueError(f"Empty index in share at index {index}")
    if not all(c in '0123456789abcdef' for c in index_str):
        raise ValueError(f"Invalid index format in share at index {index}: must be a valid hex string")
    
    index_int = int(index_str, 16)
    if not (0 <= index_int <= 0xFFFFFFFF):
        raise ValueError(f"Index out of range in share at index {index}: must be between 0 and 2^32-1")
        
    return key_str, index_str


async def recover_key(keyShards: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Recover the master key from a subset of key shares using Lagrange interpolation.
    
    Args:
        keyShards: List of dictionaries containing 'key' and 'index' fields
        
    Returns:
        {
            "masterKey": "<recovered master key hex string>",
            "error": "<error message if any>"
        }
    """
    logger.info(f"Attempting to recover master key from {len(keyShards)} shares")
    
    try:
        for i, share in enumerate(keyShards):
            validate_share(share, i)
        secret = lagrange_interpolation(keyShards, PRIME)
        return {
            "masterKey": hex(secret),
            "error": None
        }
    except ValueError as e:
        logger.error(f"Validation error during key recovery: {str(e)}")
        return {
            "masterKey": None,
            "error": f"Validation error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Error during key recovery: {str(e)}")
        return {
            "masterKey": None,
            "error": f"Recovery error: {str(e)}"
        }
