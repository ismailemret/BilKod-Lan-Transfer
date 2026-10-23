"""TCP server functionality for the LAN transfer application."""
from multiprocessing.dummy import connection
import socket

from utils.logger import get_logger


HOST = "0.0.0.0"
PORT = 5050
logger = get_logger(__name__)


def serve() -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.settimeout(10)
            listener.bind((HOST, PORT))
            listener.listen(1)
            logger.info("Sunucu %s:%s adresinde dinliyor", HOST, PORT)

            connection, address = listener.accept()
            with connection:
                connection.settimeout(10)
                logger.info("İstemci bağlandı: %s", address)

                with connection.makefile("rb") as reader:
                    message = reader.readline(1024)

                if message != b"PING\n":
                    raise ValueError("Beklenmeyen istemci mesajı")

                connection.sendall(b"PONG\n")
                logger.info("El sıkışma tamamlandı")

    except ConnectionResetError:
        logger.exception("İstemci bağlantıyı beklenmedik şekilde kapattı")
        raise
    except OSError:
        logger.exception("Sunucu socket hatası")
        raise


if __name__ == "__main__":
    serve()