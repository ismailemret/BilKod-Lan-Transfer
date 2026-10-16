from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ConnectionStatus(Enum):
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    FAILED = "FAILED"

class TransferStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    TRANSFERRING = "TRANSFERRING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

@dataclass(frozen=True)
class DeviceInfo:
    device_id: str
    hostname: str
    ip_address: str
    port: int
    is_self: bool = False

@dataclass(frozen=True)
class ConnectionRequest:
    sender_id: str
    target_id: str
    timestamp: float

@dataclass(frozen=True)
class TransferOffer:
    transfer_id: str
    sender_id: str
    filename: str
    file_size_bytes: int
    expected_sha256: str

@dataclass(frozen=True)
class TransferChunk:
    transfer_id: str
    chunk_index: int
    chunk_size_bytes: int
    data: bytes

@dataclass(frozen=True)
class TransferProgress:
    transfer_id: str
    transferred_bytes: int
    total_bytes: int
    speed_bps: float
    percentage: float

@dataclass(frozen=True)
class TransferResult:
    transfer_id: str
    status: TransferStatus
    file_path: Optional[str] = None
    error_message: Optional[str] = None

@dataclass(frozen=True)
class AppEvent:
    event_type: str
    payload: dict
