from py_ecc.bls import G2ProofOfPossession as BLS
from py_ecc.optimized_bls12_381 import curve_order
import random
from typing import Dict, List

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes(32, byteorder="big")

def eval_poly(poly: List[int], x: int) -> int:
    """Evaluate polynomial at a given point x."""
    result = 0
    for i, coeff in enumerate(poly):
        result = (result + coeff * pow(x, i, curve_order)) % curve_order
    return result

def generate(threshold: int = 3, key_count: int = 5) -> Dict[str, any]:
    if threshold > key_count:
        raise ValueError("threshold must be less than or equal to key_count")

    # Generate random polynomial coefficients (secret is constant term)
    poly = [random.randint(1, curve_order - 1) for _ in range(threshold)]
    master_sk = poly[0]  # constant term is master key

    shares = []
    # Generate random vector IDs, ensuring uniqueness
    id_vec = set()
    while len(id_vec) < key_count:
        id_vec.add(random.randint(1, curve_order - 1))
    id_vec = list(id_vec)

    for x in id_vec:
        y = eval_poly(poly, x)
        # Convert index to hex string without '0x' prefix to match JS output
        index_hex = hex(x)[2:].zfill(64)  # Ensure 64-character hex string
        shares.append({
            "index": index_hex,
            "key": int_to_bytes(y).hex()
        })

    return {
        "masterKey": int_to_bytes(master_sk).hex(),
        "keyShards": shares
    } 