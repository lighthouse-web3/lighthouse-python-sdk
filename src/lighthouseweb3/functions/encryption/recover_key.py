from typing import List, Dict
from py_ecc.optimized_bls12_381.optimized_curve import curve_order

def recover_key(shards: List[Dict[str, str]]) -> Dict[str, str]:

    try:
        # Convert hex strings to integers
        x_coords = [int(shard['index'], 16) for shard in shards]
        y_coords = [int(shard['key'], 16) for shard in shards]

        # Lagrange interpolation to recover the constant term (secret)
        def lagrange_interpolate(x: int, x_s: List[int], y_s: List[int], p: int) -> int:
            total = 0
            for i in range(len(x_s)):
                numerator = denominator = 1
                for j in range(len(x_s)):
                    if i != j:
                        numerator = (numerator * (x - x_s[j])) % p
                        denominator = (denominator * (x_s[i] - x_s[j])) % p
                l = (y_s[i] * numerator * pow(denominator, -1, p)) % p
                total = (total + l) % p
            return total

        # Recover the master key at x=0
        master_key = lagrange_interpolate(0, x_coords, y_coords, curve_order)

        return {"masterKey": hex(master_key)[2:].zfill(64), "error": None}
    except Exception as e:
        return {"masterKey": None, "error":e}