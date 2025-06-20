from py_ecc.bls import G2ProofOfPossession as bls
from py_ecc.optimized_bls12_381.optimized_curve import curve_order
from secrets import randbits
from typing import List, Tuple, Dict, Any

def shard_key(key: str, threshold: int = 3, key_count: int = 5) -> Dict[str, Any]:

    try:
        # Initialize master secret key list
        msk = []
        id_vec = []
        sec_vec = []

        # Convert input hex key to integer
        master_key = int(key, 16)
        msk.append(master_key)

        # Generate additional random coefficients for polynomial
        for _ in range(threshold - 1):
            # Generate random number for polynomial coefficient
            sk = randbits(256)  # Using 256 bits for randomness
            msk.append(sk)

        # Perform key sharing
        for i in range(key_count):
            # Create random ID (x-coordinate for polynomial evaluation)
            id_val = randbits(256)
            id_vec.append(id_val)

            # Evaluate polynomial at id_val to create shard
            # Using Shamir's secret sharing polynomial evaluation
            sk = 0
            for j, coef in enumerate(msk):
                sk += coef * pow(id_val, j, curve_order)
            sk %= curve_order
            sec_vec.append(sk)

        # Convert to hex format for output
        return {
            "isShardable": True,
            "keyShards": [
                {
                    "key": hex(sk)[2:].zfill(64),  # Remove '0x' and pad to 64 chars
                    "index": hex(id_vec[i])[2:].zfill(64)
                }
                for i, sk in enumerate(sec_vec)
            ]
        }
    except Exception as e:
        return {"isShardable": False, "keyShards": []}