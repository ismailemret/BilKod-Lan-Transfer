<<<<<<< HEAD
"""TCP server functionality for the LAN transfer application."""
=======
"""TCP server functionality for the LAN transfer application."""

import socket
from typing import Optional, Tuple

from utils.logger import logger


class TCPServer:
    """A minimal TCP listener that accepts one client connection at a time."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        self.host = host
        self.port = port
        self._socket: Optional[socket.socket] = None

    def start(self) -> None:
        """Bind the listening socket and start accepting connections."""
        if self._socket is not None:
            raise RuntimeError("TCP server is already running")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
        except OSError:
            server_socket.close()
            logger.exception("Failed to start TCP server on %s:%s", self.host, self.port)
            raise

        self._socket = server_socket
        logger.info("TCP server listening on %s:%s", self.host, self.port)

    def accept_connection(self) -> Tuple[socket.socket, Tuple[str, int]]:
        """Wait for and return the next connected client socket and address."""
        if self._socket is None:
            raise RuntimeError("TCP server has not been started")

        connection, address = self._socket.accept()
        logger.info("Accepted TCP connection from %s:%s", address[0], address[1])
        return connection, address

    def close(self) -> None:
        """Close the listening socket if it is running."""
        if self._socket is not None:
            self._socket.close()
            self._socket = None
            logger.info("TCP server stopped")
>>>>>>> d8fe679 (Update device discovery and networking)
