"""TCP server functionality for the LAN transfer application."""
import socket
from typing import Tuple

from utils.logger import get_logger


HOST = "0.0.0.0"
PORT = 5050
logger = get_logger(__name__)


def create_listener(
    host: str = HOST,
    port: int = PORT,
    timeout: float = 10,
) -> socket.socket:
    """Create and start a TCP listener for direct LAN connections."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.settimeout(timeout)
    listener.bind((host, port))
    listener.listen(1)
    bound_port = listener.getsockname()[1]
    logger.info("Sunucu %s:%s adresinde dinliyor", host, bound_port)
    return listener


def accept_connection(
    listener: socket.socket,
    timeout: float = 10,
) -> Tuple[socket.socket, tuple]:
    """Accept one TCP client and complete the PING/PONG handshake."""
    connection, address = listener.accept()
    connection.settimeout(timeout)
    logger.info("İstemci bağlandı: %s", address)

    try:
        with connection.makefile("rb") as reader:
            message = reader.readline(1024)

        if message != b"PING\n":
            raise ValueError("Beklenmeyen istemci mesajı")

        connection.sendall(b"PONG\n")
        logger.info("El sıkışma tamamlandı")
        return connection, address
    except Exception:
        connection.close()
        raise


def serve(
    host: str = HOST,
    port: int = PORT,
    timeout: float = 10,
) -> None:
    """Listen on a TCP port and accept one direct socket connection."""
    try:
        with create_listener(host, port, timeout) as listener:
            connection, _ = accept_connection(listener, timeout)
            connection.close()

    except ConnectionResetError:
        logger.exception("İstemci bağlantıyı beklenmedik şekilde kapattı")
        raise
    except OSError:
        logger.exception("Sunucu socket hatası")
        raise


if __name__ == "__main__":
    serve()