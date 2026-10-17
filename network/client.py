<<<<<<< HEAD
"""TCP client functionality for the LAN transfer application."""
=======
"""TCP client functionality for the LAN transfer application."""

import socket
from typing import Optional

from utils.logger import logger


class TCPClient:
    """A minimal TCP client for connecting to a host and port."""

    def __init__(self, host: str, port: int, timeout: Optional[float] = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self._socket: Optional[socket.socket] = None

    def connect(self) -> socket.socket:
        """Connect to the configured endpoint and return the connected socket."""
        if self._socket is not None:
            raise RuntimeError("TCP client is already connected")

        try:
            self._socket = socket.create_connection(
                (self.host, self.port),
                timeout=self.timeout,
            )
        except OSError:
            logger.exception("Failed to connect to TCP server at %s:%s", self.host, self.port)
            raise

        logger.info("Connected to TCP server at %s:%s", self.host, self.port)
        return self._socket

    def close(self) -> None:
        """Close the client socket if it is connected."""
        if self._socket is not None:
            self._socket.close()
            self._socket = None
            logger.info("TCP client disconnected from %s:%s", self.host, self.port)
>>>>>>> d8fe679 (Update device discovery and networking)
