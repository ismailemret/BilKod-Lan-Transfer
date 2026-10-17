<<<<<<< HEAD
from enum import Enum


class ConnectionStatus(Enum):
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    ERROR = "ERROR"
=======
"""TCP networking primitives."""

from .client import TCPClient
from .server import TCPServer

__all__ = ["TCPClient", "TCPServer"]
>>>>>>> d8fe679 (Update device discovery and networking)
