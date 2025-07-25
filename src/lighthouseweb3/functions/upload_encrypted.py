import os
import requests
from pathlib import Path
from typing import List, Dict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import secrets
from .config import Config
from .encryption import generate as generateKey, save_shards as saveShards



def fetch_with_timeout(
    endpoint_url: str,
    method: str = 'GET',
    files: Dict = None,
    timeout: int = 8000,
    headers: Dict = None
) -> requests.Response:
    try:
        # Convert timeout to seconds (from milliseconds)
        timeout_seconds = timeout / 1000

        # Make HTTP request
        response = requests.request(
            method=method,
            url=endpoint_url,
            headers=headers,
            files=files,
            timeout=timeout_seconds
        )
        return response
    except requests.Timeout:
        raise Exception('Request timed out')
    except requests.RequestException as e:
        raise Exception(f'Network error: {str(e)}')

def walk(dir: str) -> List[str]:
    results = []
    for root, _, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            results.append(file_path)
    return results

def encrypt_file(file_data: bytes, password: str) -> bytes:
    try:
        # Convert password to bytes
        password_bytes = password.encode('utf-8')

        # Generate random salt and IV
        salt = secrets.token_bytes(16)
        iv = secrets.token_bytes(12)

        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key for AES-GCM
            salt=salt,
            iterations=250000,
            backend=default_backend()
        )
        aes_key = kdf.derive(password_bytes)

        # Encrypt the file data using AES-GCM
        aesgcm = AESGCM(aes_key)
        cipher_bytes = aesgcm.encrypt(iv, file_data, None)

        # Combine salt, IV, and cipher bytes
        result_bytes = salt + iv + cipher_bytes

        return result_bytes
    except Exception as e:
        raise e

def upload_file(
    source_path: str,
    api_key: str,
    public_key: str,
    auth_token: str,
    cid_version: int = 1,
) -> Dict[str, List[Dict]]:
    token = f"Bearer {api_key}"
    endpoint = f"{Config.lighthouse_node}/api/v0/add?wrap-with-directory=false&cid-version={cid_version}"

    if os.path.isfile(source_path):
        try:
            # Generate encryption key and shards
            key = generateKey.generate()

            # Read and encrypt file
            with open(source_path, 'rb') as f:
                file_data = f.read()
            encrypted_data = encrypt_file(file_data, key['masterKey'])

            # Prepare file for upload
            filename = os.path.basename(source_path)
            files = {'file': (filename, encrypted_data)}

            # Make HTTP request
            response = fetch_with_timeout(
                endpoint,
                method='POST',
                files=files,
                timeout=7200000,
                headers={
                    'Encryption': 'true',
                    'Authorization': token
                }
            )

            if response.status_code != 200:
                res = response.json()
                raise Exception(res.get('error', 'Unknown error'))

            response_data = response.json()

            # Save encryption key shards
            error = saveShards.save_shards(public_key, response_data[0]['Hash'], auth_token, key['keyShards'])
            if error["error"]:
                raise Exception('Error encrypting file')

            return {'data': response_data}
        except Exception as e:
            raise Exception(str(e))
    else:
        files_list = walk(source_path)
        if len(files_list) > 1 and auth_token.startswith('0x'):
            raise Exception('auth_token must be a JWT')

        key_map = {}
        files = {}

        for file_path in files_list:
            key = generateKey.generate()
            with open(file_path, 'rb') as f:
                file_data = f.read()
            encrypted_data = encrypt_file(file_data, key['masterKey'])
            filename = str(Path(file_path).relative_to(source_path)).replace(os.sep, '-')
            files[filename] = (filename, encrypted_data)
            key_map[filename] = key['keyShards']


        # Make HTTP request with multiple files
        response = fetch_with_timeout(
            endpoint,
            method='POST',
            files=files,
            timeout=7200000,
            headers={
                'Encryption': 'true',
                'Authorization': token
            }
        )

        if response.status_code != 200:
            res = response.json()
            raise Exception(res.get('error', 'Unknown error'))

        response_text = response.text
        import re
        match = re.search(r'\[.*\]$', response_text, re.DOTALL)
        if not match:
            raise Exception('No JSON array found in response')

        json_data = response.json()

        # Save key shards for each file
        for data in json_data:
            result = saveShards.save_shards(public_key, data['Hash'], auth_token, key_map[data['Name']])
            if not result.get('isSuccess', False):
                raise Exception(str(result))

        return {'data': json_data}
