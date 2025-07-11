from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum
import re

SOLIDITY_TYPES = [
    "address", "address[]", "bool", "bool[]",
    "bytes1", "bytes2", "bytes3", "bytes4", "bytes5", "bytes6", "bytes7", "bytes8", "bytes16", "bytes32",
    "bytes1[]", "bytes2[]", "bytes3[]", "bytes4[]", "bytes5[]", "bytes6[]", "bytes7[]", "bytes8[]", "bytes16[]", "bytes32[]",
    "uint8", "uint16", "uint24", "uint32", "uint40", "uint48", "uint64", "uint128", "uint192", "uint256",
    "int8", "int16", "int24", "int32", "int40", "int48", "int64", "int128", "int192", "int256",
    "uint8[]", "uint16[]", "uint24[]", "uint32[]", "uint40[]", "uint48[]", "uint64[]", "uint128[]", "uint192[]", "uint256[]",
    "int8[]", "int16[]", "int24[]", "int32[]", "int40[]", "int48[]", "int64[]", "int128[]", "int192[]", "int256[]"
]

SUPPORTED_CHAINS = {
    "EVM": [],
    "SOLANA": ["DEVNET", "TESTNET", "MAINNET"],
    "COREUM": ["Coreum_Devnet", "Coreum_Testnet", "Coreum_Mainnet"],
    "RADIX": ["Radix_Mainnet"]
}

class ChainType(str, Enum):
    EVM = "EVM"
    SOLANA = "SOLANA"
    COREUM = "COREUM"
    RADIX = "RADIX"

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

class ReturnValueTest(BaseModel):
    comparator: Comparator
    value: Union[int, float, str, List[Any]]

class PDAInterface(BaseModel):
    offset: int = Field(ge=0)
    selector: str

class EVMCondition(BaseModel):
    id: int = Field(ge=1)
    standard_contract_type: StandardContractType = Field(alias="standardContractType")
    contract_address: Optional[str] = Field(alias="contractAddress")
    chain: str
    method: str
    parameters: Optional[List[Any]] = []
    return_value_test: ReturnValueTest = Field(alias="returnValueTest")
    input_array_type: Optional[List[str]] = Field(alias="inputArrayType")
    output_type: Optional[str] = Field(alias="outputType")

    @validator('contract_address')
    def validate_contract_address(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] != "":
            if not v:
                raise ValueError('contract_address is required when standardContractType is not empty')
        return v

    @validator('method')
    def validate_method(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] == "":
            if v not in ["getBalance", "getBlockNumber"]:
                raise ValueError('method must be getBalance or getBlockNumber when standardContractType is empty')
        return v

    @validator('parameters')
    def validate_parameters(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] != "":
            if not v:
                raise ValueError('parameters is required when standardContractType is not empty')
        return v

    @validator('input_array_type')
    def validate_input_array_type(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] == "Custom":
            if not v:
                raise ValueError('input_array_type is required when standardContractType is Custom')
            for item in v:
                if item not in SOLIDITY_TYPES:
                    raise ValueError(f'Invalid solidity type: {item}')
        return v

    @validator('output_type')
    def validate_output_type(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] == "Custom":
            if not v:
                raise ValueError('output_type is required when standardContractType is Custom')
            if v not in SOLIDITY_TYPES:
                raise ValueError(f'Invalid solidity type: {v}')
        return v

    class Config:
        allow_population_by_field_name = True

class SolanaCondition(BaseModel):
    id: int = Field(ge=1)
    contract_address: Optional[str] = Field(alias="contractAddress")
    chain: str
    method: str
    standard_contract_type: SolanaContractType = Field(alias="standardContractType")
    parameters: Optional[List[Any]] = []
    pda_interface: PDAInterface = Field(alias="pdaInterface")
    return_value_test: ReturnValueTest = Field(alias="returnValueTest")

    @validator('chain')
    def validate_chain(cls, v):
        if v.upper() not in SUPPORTED_CHAINS["SOLANA"]:
            raise ValueError(f'Invalid Solana chain: {v}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] != "":
            if not v:
                raise ValueError('contract_address is required when standardContractType is not empty')
        return v

    @validator('method')
    def validate_method(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] == "":
            if v not in ["getBalance", "getLastBlockTime", "getBlockHeight"]:
                raise ValueError('method must be getBalance, getLastBlockTime, or getBlockHeight when standardContractType is empty')
        else:
            if v not in ["getTokenAccountsByOwner"]:
                raise ValueError('method must be getTokenAccountsByOwner when standardContractType is not empty')
        return v

    class Config:
        allow_population_by_field_name = True

class CoreumCondition(BaseModel):
    id: int = Field(ge=1)
    contract_address: Optional[str] = Field(alias="contractAddress")
    denom: Optional[str]
    classid: Optional[str]
    standard_contract_type: Optional[str] = Field(alias="standardContractType", default="")
    chain: str
    method: str
    parameters: Optional[List[Any]] = []
    return_value_test: ReturnValueTest = Field(alias="returnValueTest")

    @validator('chain')
    def validate_chain(cls, v):
        if v not in SUPPORTED_CHAINS["COREUM"]:
            raise ValueError(f'Invalid Coreum chain: {v}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] != "":
            if not v:
                raise ValueError('contract_address is required when standardContractType is not empty')
        return v

    @validator('parameters')
    def validate_parameters(cls, v, values):
        if 'standard_contract_type' in values and values['standard_contract_type'] != "":
            if not v:
                raise ValueError('parameters is required when standardContractType is not empty')
        return v

    class Config:
        allow_population_by_field_name = True

class RadixCondition(BaseModel):
    id: int = Field(ge=1)
    standard_contract_type: Optional[str] = Field(alias="standardContractType", default="")
    resource_address: str = Field(alias="resourceAddress")
    chain: str
    method: str
    return_value_test: ReturnValueTest = Field(alias="returnValueTest")

    @validator('chain')
    def validate_chain(cls, v):
        if v not in SUPPORTED_CHAINS["RADIX"]:
            raise ValueError(f'Invalid Radix chain: {v}')
        return v

    class Config:
        allow_population_by_field_name = True

class UpdateConditionSchema(BaseModel):
    chain_type: ChainType = Field(alias="chainType", default=ChainType.EVM)
    conditions: List[Union[EVMCondition, SolanaCondition, CoreumCondition, RadixCondition]]
    decryption_type: DecryptionType = Field(alias="decryptionType", default=DecryptionType.ADDRESS)
    address: str
    cid: str
    aggregator: Optional[str] = None

    @validator('conditions')
    def validate_conditions_uniqueness(cls, v):
        ids = [condition.id for condition in v]
        if len(ids) != len(set(ids)):
            raise ValueError('Condition IDs must be unique')
        return v

    @validator('aggregator')
    def validate_aggregator(cls, v, values):
        if 'conditions' in values and len(values['conditions']) > 1:
            if not v:
                raise ValueError('aggregator is required when there are multiple conditions')
            if not re.search(r'( and | or )', v, re.IGNORECASE):
                raise ValueError('aggregator must contain " and " or " or "')
        return v

    @root_validator
    def validate_condition_types(cls, values):
        chain_type = values.get('chain_type', ChainType.EVM)
        conditions = values.get('conditions', [])
        
        expected_type = {
            ChainType.EVM: EVMCondition,
            ChainType.SOLANA: SolanaCondition,
            ChainType.COREUM: CoreumCondition,
            ChainType.RADIX: RadixCondition
        }.get(chain_type)
        
        for condition in conditions:
            if not isinstance(condition, expected_type):
                raise ValueError(f'All conditions must be of type {expected_type.__name__} for chain type {chain_type}')
        
        return values

    class Config:
        allow_population_by_field_name = True

class AccessConditionSchema(BaseModel):
    chain_type: ChainType = Field(alias="chainType", default=ChainType.EVM)
    decryption_type: DecryptionType = Field(alias="decryptionType", default=DecryptionType.ADDRESS)
    conditions: List[Union[EVMCondition, SolanaCondition, CoreumCondition, RadixCondition]]
    address: str
    key_shards: List[dict] = Field(alias="keyShards", min_items=5, max_items=5)
    cid: str
    aggregator: Optional[str] = None

    @validator('conditions')
    def validate_conditions_uniqueness(cls, v):
        ids = [condition.id for condition in v]
        if len(ids) != len(set(ids)):
            raise ValueError('Condition IDs must be unique')
        return v

    @validator('aggregator')
    def validate_aggregator(cls, v, values):
        if 'conditions' in values and len(values['conditions']) > 1:
            if not v:
                raise ValueError('aggregator is required when there are multiple conditions')
            if not re.search(r'( and | or )', v, re.IGNORECASE):
                raise ValueError('aggregator must contain " and " or " or "')
        return v

    @root_validator
    def validate_condition_types(cls, values):
        chain_type = values.get('chain_type', ChainType.EVM)
        conditions = values.get('conditions', [])
        
        expected_type = {
            ChainType.EVM: EVMCondition,
            ChainType.SOLANA: SolanaCondition,
            ChainType.COREUM: CoreumCondition,
            ChainType.RADIX: RadixCondition
        }.get(chain_type)
        
        for condition in conditions:
            if not isinstance(condition, expected_type):
                raise ValueError(f'All conditions must be of type {expected_type.__name__} for chain type {chain_type}')
        
        return values

    class Config:
        allow_population_by_field_name = True