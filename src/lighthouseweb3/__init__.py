#!/usr/bin/env python3

import os
import io
from .functions import (
    upload as d,
    deal_status, 
    get_uploads as getUploads, 
    download as _download,
    get_file_info as getFileInfo,
    get_balance as getBalance,
    get_api_key as getApiKey,
    ipns_generate_key as ipnsGenerateKey,
    ipns_publish_record as ipnsPublishRecord,
    get_ipns_record as getIpnsRecord,
    remove_ipns_record as removeIpnsRecord,
    create_wallet as createWallet,
    upload_encrypted as uploadEncrypted
)

from typing import Any, Dict, List

from .functions.encryption import (
    get_jwt as getJwt,
    revoke_access as revokeAccess,
    generate as generateKey,
    transfer_ownership as transferOwnership,
    share_to_address as shareToAddress,
    save_shards as saveShards,
    get_access_condition as getAccessCondition,
    get_auth_message as getAuthMessage,
    recover_key as recoveryKey,
    shared_key as sharedKey
)
class Lighthouse:
    def __init__(self, token: str = ""):
        self.token = token or os.environ.get("LIGHTHOUSE_TOKEN", "")
        if not self.token:
            raise Exception(
                "No token provided: Please provide a token or set the LIGHTHOUSE_TOKEN environment variable"
            )

    def upload(self, source: str, tag: str = ''):
        """
        Upload a file or directory to the Lighthouse.

        :param source: str, path to file or directory
        :return: t.Upload, the upload result
        """
        try:
            return d.upload(source, self.token, tag)
        except Exception as e:
            raise e
    
    def uploadEncrypted(self, source_path: str, public_key: str, auth_token: str, cid_version: int = 1) -> Dict[str, List[Dict]]:
        """
        Upload a file or directory to the Lighthouse.

        :param source_path: str, path to file or directory
        :param public_key: str, public key of the user
        :param auth_token: str, auth token of the user
        :param cid_version: int, cid version of the user
        :return: t.Upload, the upload result
        """

        try:
            return uploadEncrypted.upload_file(source_path, self.token, public_key, auth_token, cid_version)
        except Exception as e:
            raise e


    def uploadBlob(self, source: io.BufferedReader, filename: str, tag: str = ''):
        """
        Upload Blob a file or directory to the Lighthouse.

        :param source: str, path to file or directory
        :return: t.Upload, the upload result
        """
        if not (hasattr(source, 'read') and hasattr(source, 'close')):
            raise TypeError("source must have 'read' and 'close' methods")
        try:
            return d.uploadBlob(source, filename, self.token, tag)
        except Exception as e:
            raise e
    
    def getBalance(self):
        """
        Retrieve the balance information of a user from the Lighthouse.

        :param publicKey: str, The public key of the user.
        :return: dict[str, any], A dictionary containing the data usage and data limit details.
        """
        try:
            return getBalance.get_balance(self.token)
        except Exception as e:
            raise e
    
    def generateKey(self):
        """
        Generate a new IPNS key for the authenticated user.

        :return: dict, The generated IPNS key information.
        """
        try:
            return ipnsGenerateKey.ipns_generate_key(self.token)
        except Exception as e:
            raise e

    def publishRecord(self, cid: str, keyName: str):
        """
        Publish an IPNS record for a given CID and key name.

        :param cid: str, Content Identifier to publish
        :param keyName: str, Name of the IPNS key to use
        :return: dict, The published IPNS record information
        """
        try:
            return ipnsPublishRecord.ipns_publish_record(self.token, cid, keyName)
        except Exception as e:
            raise e

    def getAllKeys(self):
        """
        Retrieves all IPNS records associated with the current token.

        :return: list A list of IPNS records retrieved using the provided token.
        """

        try:
            return getIpnsRecord.get_ipns_records(self.token)
        except Exception as e:
            raise e

    def removeKey(self, keyName: str):
        """
        Remove IPNS record of the given keyName

        :param keyName: str, Name of the IPNS key to use
        :return: dict, A dict of removed IPNS record.
        """

        try:
            return removeIpnsRecord.remove_ipns_record(self.token, keyName)
        except Exception as e:
            raise e
    
    @staticmethod
    def createWallet(password: str):
        """
        Creates a new wallet using the provided password.

        :param password: str, The password to secure the wallet.
        :return: dict, The wallet encrypted with the passowrd
        """
        try:
            return createWallet.create_wallet(password)
        except Exception as e:
            raise e

    @staticmethod
    def downloadBlob(dist: io.BufferedWriter, cid: str, chunk_size=1024*1024*10):
        """
        Download a Blob (file or directory) from the Lighthouse.

        :param dist: BufferedWriter, destination to write the downloaded data
        :param cid: str, Content Identifier for the data to be downloaded
        :param chunk_size: int, size of chunks in which the file will be downloaded (default: 10MB)
        :return: t.Upload, the download result
        """
        if not (hasattr(dist, 'read') and hasattr(dist, 'close')):
            raise TypeError("source must have 'read' and 'close' methods")
        try:
            return _download.download_file_into_writable(cid, dist, chunk_size)
        except Exception as e:
            raise e
            
    @staticmethod
    def getDealStatus(cid: str):
        """
        Get deal status from the Lighthouse.

        :param cid: str, content identifier
        :return: List[t.DealData], list of deal data
        """
        try:
            return deal_status.get_deal_status(cid)
        except Exception as e:
            raise e
    
    def getUploads(self, lastKey: str = None):
        """
        Get uploads from the Lighthouse.

        :param lastKey: To navigate to different pages of results
        :return: List[t.DealData], list of deal data
        """
        try:
            return getUploads.get_uploads(self.token, lastKey)
        except Exception as e:
            raise e

    @staticmethod
    def download(cid: str):
        """
        Download content from the Lighthouse using its Content Identifier (CID).

        :param cid: str, Content Identifier for the data to be downloaded
        :param useCidAsTag: bool, flag to use CID as a tag (default: False)
        :return: bytes, the downloaded content
        """
        try:
            return _download.get_file(cid)
        except Exception as e:
            raise e
    
    @staticmethod
    def getFileInfo(cid: str):
        """
        Retrieves information about a file using its CID (Content Identifier).

        :param cid: str, Content Identifier for the data to be downloaded
        :return: dict, A dictionary containing file information.
        """

        try:
            return getFileInfo.get_file_info(cid)
        except Exception as e:
            raise e
    
    @staticmethod
    def getApiKey(publicKey: str, signedMessage: str):
        """
        Generates and returns an API key for the given public key and signed message.

        :param publicKey: str, The public key associated with the user.
        :param signedMessage: str, The message signed by the user's private key.
        :return: dict, A dict with generated API key.
        """


        try:
            return getApiKey.get_api_key(publicKey, signedMessage)
        except Exception as e:
            raise e

    def getTagged(self, tag: str):
        """
        Retrieve an upload from the Lighthouse using its tag.

        :param tag: str, tag associated with the file or directory
        :return: t.Upload, the upload result
        """
        try:
            return _download.getTaggedCid(tag, self.token)
        except Exception as e:
            raise e

class Kavach:
    @staticmethod
    def sharedKey(key: str, threshold: int = 3, key_count: int = 5) -> Dict[str, Any]:
        """
        Splits a secret key into shards using Shamir's Secret Sharing on BLS12-381 curve.
        
        :param key: Hex string of the master secret key
        :param threshold: Minimum number of shards required to reconstruct the key
        :param key_count: Total number of shards to generate
        
        :return: Dict containing isShardable flag and list of key shards with their indices
        """

        try:
            return sharedKey.shard_key(key, threshold, key_count)
        except Exception as e:
            raise e
    
    @staticmethod
    def recoverKey(shards: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Recovers the master key from a list of key shards using Lagrange interpolation.
        
        :param shards: List of dictionaries containing 'key' and 'index' as hex strings
        :return: Dictionary containing the recovered master key
        """
        try:
            return recoveryKey.recover_key(shards)
        except Exception as e:
            raise e
    
    @staticmethod
    def getAuthMessage(address: str) -> dict[str, Any]:
        """
        Get Authentication message from the server

        :param address: str, The public key of the user
        :return: dict, A dict with authentication message or error
        """
        try:
            return getAuthMessage.get_auth_message(address)
        except Exception as e:
            raise e
    
    @staticmethod
    def getAccessCondition(cid: str):
        """
        Get Access Condition for cid from the node

        :param cid: str, Content Identifier for the data to be downloaded
        :return: conditions dict of access conditions
        """

        try:
            return getAccessCondition.get_access_condition(cid)
        except Exception as e:
            raise e
    
    @staticmethod
    def saveShards(
        address: str,
        cid: str,
        auth_token: str, 
        key_shards: List[dict],
        share_to: List[str] = None
    ) -> Dict[str, Any]:
        """
        Save key shards to multiple nodes.
        
        :param address: str, The Ethereum address of the user.
        :param cid: str, The Content Identifier (CID) of the file for which key shards are being saved.
        :param auth_token: str, The authentication token obtained by signing a message.
        :param key_shards: List[KeyShard], A list of KeyShard objects, each containing a key and its index.
        :param share_to: List[str], optional, A list of Ethereum addresses to which the key shards should be shared. Defaults to None.
        :return: Dict[str, Any], A dictionary indicating the success or failure of the operation, along with any error messages.
        """

        try:
            return saveShards.save_shards(address, cid, auth_token, key_shards, share_to)
        except Exception as e:
            raise e
    
    @staticmethod
    def shareToAddress(address: str, cid: str, auth_token: Dict[str, Any], share_to: List[str]) -> Dict[str, Any]:
        """
        Share an encrypted file with a list of addresses.

        :param address: str, The public address of the file owner.
        :param cid: str, The CID of the file to share.
        :param auth_token: Dict[str, Any], The authentication token.
        :param share_to: List[str], A list of public addresses to share the file with.
        :return: Dict[str, Any], A dictionary indicating the result of the share operation.
        """
        try:
            return shareToAddress.share_to_address(address, cid, auth_token, share_to)
        except Exception as e:
            raise e
    
    @staticmethod
    def transferOwnership(address: str, cid: str, new_owner: str, auth_token: str, reset_shared_to: bool = True) -> dict[str, Any]:
        """
        Transfer ownership of a file from the current owner to a new owner.

        :param address: str, The address of the current owner.
        :param cid: str, The Content Identifier (CID) of the file to transfer.
        :param new_owner: str, The address of the new owner.
        :param auth_token: str, The authentication token for the current owner.
        :param reset_shared_to: bool, Whether to reset the list of users the file is shared with (default: True).
        :return: dict, A dictionary indicating the success or failure of the operation.
        """
        try:
            return transferOwnership.transfer_ownership(address, cid, new_owner, auth_token, reset_shared_to)
        except Exception as e:
            raise e 
    
    @staticmethod
    def generate(threshold: int = 3, key_count: int = 5) -> Dict[str, any]:
        """
        Generates a set of master secret keys and corresponding key shards using BLS (Boneh-Lynn-Shacham)
        threshold cryptography.

        :param threshold: int, The minimum number of key shards required to reconstruct the master key.
        :param key_count: int, The total number of key shards to generate.
        :return: Dict[str, any], A dictionary containing the master key and a list of key shards.
        """

        try:
            return generateKey.generate(threshold, key_count)
        except Exception as e:
            raise e
    
    @staticmethod
    def revokeAccess(address: str, cid: str, auth_token: str, revoke_to: List[str]) -> Dict:
        """
        Revokes access to a shared file for specified recipients.
        
        :param address: str, The address of the user initiating the revocation.
        :param cid: str, The CID of the file for which access is being revoked.
        :param auth_token: str, The authentication token of the user.
        :param revoke_to: List[str], A list of addresses for whom access is to be revoked.
        :return: Dict, A dictionary indicating the success or failure of the revocation.
        """
        try:
            return revokeAccess.revoke_access(address, cid, auth_token, revoke_to)
        except Exception as e:
            raise e 
    
    @staticmethod
    def getJWT(address: str, payload: str, use_as_refresh_token: bool = False, chain: str = "ALL") -> Dict:
        """
        Retrieves a JSON Web Token (JWT) for authentication.

        :param address: str, The blockchain address of the user.
        :param payload: str, The signed message or refresh token.
        :param use_as_refresh_token: bool, If True, payload is treated as a refresh token.
        :param chain: str, The blockchain chain (e.g., "ALL", "ETHEREUM").
        :return: Dict, A dictionary containing the JWT and refresh token, or an error.
        """
        
        try:
            return getJwt.get_jwt(address, payload, use_as_refresh_token, chain)
        except Exception as e:
            raise e