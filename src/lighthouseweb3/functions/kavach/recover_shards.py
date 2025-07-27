import random
import asyncio
from typing import List, Dict, Any, Optional, Union, cast

from .types import AuthToken, RecoverShards, KeyShard


def shuffle_array(array: List[int]) -> List[int]:
    """Shuffle the input array in place using Fisher-Yates algorithm.
    
    Args:
        array: List of integers to be shuffled
        
    Returns:
        List[int]: The shuffled array (same reference as input)
    """
    for i in range(len(array) - 1, 0, -1):
        j = random.randint(0, i)
        array[i], array[j] = array[j], array[i]
    return array


def rand_select(k: int, n: int) -> List[int]:
    """Randomly select k unique numbers from range 1 to n (inclusive).
    
    Args:
        k: Number of unique numbers to select
        n: Upper bound of the range (inclusive)
        
    Returns:
        List[int]: Sorted list of k unique numbers
        
    Raises:
        ValueError: If k is greater than n
    """
    if k > n:
        raise ValueError("k cannot be greater than n")
    
    numbers = list(range(1, n + 1))
    shuffled_numbers = shuffle_array(numbers)
    return sorted(shuffled_numbers[:k])


async def recover_shards(
    address: str,
    cid: str,
    auth_token: AuthToken,
    num_of_shards: int = 3,
    dynamic_data: Optional[Dict[str, Any]] = None,
) -> RecoverShards:
    """Recover key shards from the Lighthouse network.
    
    Args:
        address: User's wallet address
        cid: Content ID for the encrypted content
        auth_token: Authentication token for API access
        num_of_shards: Number of shards to recover (default: 3)
        dynamic_data: Additional dynamic data for the request (default: {})
        
    Returns:
        RecoverShards: Object containing recovered shards or error information
    """
    if dynamic_data is None:
        dynamic_data = {}
        
    try:
        from ..config import API_NODE_HANDLER 
        
        # Select random nodes to recover shards from
        node_indices = rand_select(num_of_shards, 5)
        node_urls = [f"/api/retrieveSharedKey/{index}" for index in node_indices]
        
        async def request_data(url: str, index: int) -> Dict[str, Any]:
            """Helper function to make API requests to node URLs."""
            try:
                response = await API_NODE_HANDLER(
                    url, 
                    "POST", 
                    auth_token, 
                    {"address": address, "cid": cid, "dynamicData": dynamic_data}
                )
                return response
            except Exception as e:
                error_msg = str(getattr(e, 'message', 'Unknown error'))
                raise Exception(error_msg) from e
        
        # Request shards from each selected node
        recovered_shards: List[KeyShard] = []
        
        for index, url in enumerate(node_urls):
            try:
                response = await request_data(url, index)
                await asyncio.sleep(1)  # Add delay between requests
                
                # Convert response to KeyShard if needed
                if response and 'payload' in response:
                    payload = response['payload']
                    if isinstance(payload, dict) and 'key' in payload and 'index' in payload:
                        shard = KeyShard(key=payload['key'], index=str(payload['index']))
                        recovered_shards.append(shard)
                    else:
                        # Handle case where payload is just the key
                        shard = KeyShard(key=str(payload), index=str(index))
                        recovered_shards.append(shard)
                        
            except Exception as e:
                # Continue with other shards if one fails
                print(f"Error recovering shard from {url}: {str(e)}")
                continue
        
        if not recovered_shards:
            return RecoverShards(shards=[], error="Failed to recover any shards")
            
        return RecoverShards(shards=recovered_shards, error="")
        
    except Exception as err:
        error_msg = str(err)
        if "null" in error_msg or "not found" in error_msg.lower():
            return RecoverShards(shards=[], error="CID not found")
        return RecoverShards(shards=[], error=error_msg)