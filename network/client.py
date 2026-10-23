"""TCP client functionality for the LAN transfer application."""
import socket

from contracts.models import ConnectionStatus
from utils.logger import get_logger


SERVER_HOST = "127.0.0.1"
PORT = 5050
logger = get_logger(__name__)


def connect() -> ConnectionStatus:
    status = ConnectionStatus.DISCONNECTED

    try:
        status = ConnectionStatus.CONNECTING

        with socket.create_connection((SERVER_HOST, PORT), timeout=10,) as connection:
            connection.sendall(b"PING\n")

            with connection.makefile("rb") as reader:
                response = reader.readline(1024)

            if response != b"PONG\n":
                logger.error("Sunucudan beklenmeyen yanıt alındı: %r", response)
                return ConnectionStatus.FAILED

            status = ConnectionStatus.CONNECTED
            logger.info(
                "Bağlantı durumu: %s; sunucu yanıtı: %s",
                status.value,
                response.decode("ascii").strip(),
            )
            return status

    except ConnectionResetError:
        logger.exception("Sunucu bağlantıyı beklenmedik şekilde kapattı")
        return ConnectionStatus.FAILED
    except OSError:
        logger.exception("Sunucuya bağlanırken socket hatası")
        return ConnectionStatus.FAILED


if __name__ == "__main__":
    result = connect()
    logger.info("Son bağlantı durumu: %s", result.value)