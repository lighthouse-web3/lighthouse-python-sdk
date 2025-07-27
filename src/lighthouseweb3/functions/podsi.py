import requests
from typing import TypedDict, List
from .config import Config

class VerifierData(TypedDict):
    commPc: str
    sizePc: str

class ProofIndex(TypedDict):
    index: str
    path: List[str]

class ProofSubtree(TypedDict):
    index: str
    path: List[str]

class IndexRecord(TypedDict):
    checksum: str
    proofIndex: str
    proofSubtree: int
    size: int

class InclusionProof(TypedDict):
    proofIndex: ProofIndex
    proofSubtree: ProofSubtree
    indexRecord: IndexRecord

class Proof(TypedDict):
    verifierData: VerifierData
    inclusionProof: InclusionProof

class DealInfo(TypedDict):
    dealId: int
    storageProvider: str
    proof: Proof

class PODSIData(TypedDict):
    pieceCID: str
    dealInfo: List[DealInfo]

def get_proof(cid: str) -> PODSIData:
    try:
        response = requests.get(f"{Config.lighthouse_api}/api/lighthouse/get_proof?cid={cid}")
        
        if not response.ok:
            if response.status_code == 400:
                raise Exception("Proof Doesn't exist yet")
            raise Exception(f"Request failed with status code {response.status_code}")
        
        data = response.json()
        return data
        
    except requests.RequestException as error:
        if hasattr(error, 'response') and error.response and error.response.status_code == 400:
            raise Exception("Proof Doesn't exist yet")
        raise Exception(str(error))