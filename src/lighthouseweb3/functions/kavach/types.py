from typing import List, Dict, Union, Optional, Any, Literal
from dataclasses import dataclass
from enum import Enum

ErrorValue = Union[str, List[str], int, bool, None, Dict[str, Any], Any]
SignedMessage = str
JWT = str 
AuthToken = Union[SignedMessage, JWT]

class ChainType(str, Enum):
    EVM = "EVM"
    EVM_LOWER = "evm"
    SOLANA = "SOLANA"
    SOLANA_LOWER = "solana"

class DecryptionType(str, Enum):
    ADDRESS = "ADDRESS"
    ACCESS_CONDITIONS = "ACCESS_CONDITIONS"

class StandardContractType(str, Enum):
    ERC20 = "ERC20"
    ERC721 = "ERC721"
    ERC1155 = "ERC1155"
    CUSTOM = "Custom"
    EMPTY = ""

class SolanaContractType(str, Enum):
    SPL_TOKEN = "spl-token"
    EMPTY = ""

class Comparator(str, Enum):
    EQUAL = "=="
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    NOT_EQUAL = "!="
    GREATER = ">"
    LESS = "<"

# Data Classes
@dataclass
class KeyShard:
    key: str
    index: str

@dataclass
class GeneratedKey:
    master_key: Optional[str]
    key_shards: List[KeyShard]

@dataclass
class GenerateInput:
    threshold: Optional[int] = None
    key_count: Optional[int] = None

@dataclass
class AuthMessage:
    message: Optional[str]
    error: Optional[ErrorValue]

@dataclass
class RecoveredKey:
    master_key: Optional[str]
    error: Optional[ErrorValue]

@dataclass
class RecoverShards:
    shards: List[KeyShard]
    error: ErrorValue

@dataclass
class LightHouseSDKResponse:
    is_success: bool
    error: ErrorValue

@dataclass
class ReturnValueTest:
    comparator: Comparator
    value: Union[int, str, List[Any]]

@dataclass
class PDAInterface:
    offset: Optional[int] = None
    selector: Optional[str] = None

@dataclass
class EVMCondition:
    id: int
    standard_contract_type: StandardContractType
    chain: str
    method: str
    return_value_test: ReturnValueTest
    contract_address: Optional[str] = None
    parameters: Optional[List[Any]] = None
    input_array_type: Optional[List[str]] = None
    output_type: Optional[str] = None

@dataclass
class SolanaCondition:
    id: int
    chain: str
    method: str
    standard_contract_type: SolanaContractType
    pda_interface: PDAInterface
    return_value_test: ReturnValueTest
    contract_address: Optional[str] = None
    parameters: Optional[List[Any]] = None

# Union Type for Conditions
Condition = Union[EVMCondition, SolanaCondition]

@dataclass
class UpdateConditionSchema:
    chain_type: Literal["EVM", "SOLANA"]
    conditions: List[Condition]
    decryption_type: Literal["ADDRESS", "ACCESS_CONDITIONS"]
    address: str
    cid: str
    aggregator: Optional[str] = None

@dataclass
class AccessConditionSchema:
    chain_type: Literal["EVM", "SOLANA"]
    conditions: List[Condition]
    decryption_type: Literal["ADDRESS", "ACCESS_CONDITIONS"]
    address: str
    cid: str
    key_shards: List[Any]
    aggregator: Optional[str] = None

@dataclass
class IGetAccessCondition:
    aggregator: str
    owner: str
    cid: str
    conditions: Optional[List[Condition]] = None
    conditions_solana: Optional[List[Any]] = None
    shared_to: Optional[List[Any]] = None

def is_jwt(token: str) -> bool:
    """Check if token is a JWT (starts with 'jwt:')"""
    return token.startswith('jwt:')

def create_jwt(token: str) -> JWT:
    """Create a JWT token with proper prefix"""
    if not token.startswith('jwt:'):
        return f'jwt:{token}'
    return token

# Type Guards
def is_evm_condition(condition: Condition) -> bool:
    """Check if condition is an EVM condition"""
    return isinstance(condition, EVMCondition)

def is_solana_condition(condition: Condition) -> bool:
    """Check if condition is a Solana condition"""
    return isinstance(condition, SolanaCondition)