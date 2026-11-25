"""Tests for the Week 2 K1 direct TCP listener and client handshake."""

import socket
import threading
import unittest

from contracts.models import ConnectionStatus
from network.client import connect
from network.server import accept_connection, create_listener


class NetworkListenerTests(unittest.TestCase):
    def test_direct_ping_pong_connection(self) -> None:
        listener = create_listener("127.0.0.1", 0, timeout=2)
        port = listener.getsockname()[1]

        try:
            server_result = {}

            def accept_client() -> None:
                connection, address = accept_connection(listener, timeout=2)
                server_result["address"] = address
                connection.close()

            server_thread = threading.Thread(target=accept_client)
            server_thread.start()

            client_status = connect("127.0.0.1", port, timeout=2)
            server_thread.join(timeout=2)

            self.assertFalse(server_thread.is_alive())
            self.assertEqual(ConnectionStatus.CONNECTED, client_status)
            self.assertIn("address", server_result)
        finally:
            listener.close()

    def test_rejected_message_closes_connection(self) -> None:
        listener = create_listener("127.0.0.1", 0, timeout=2)
        port = listener.getsockname()[1]
        server_errors = []

        def accept_client() -> None:
            try:
                accept_connection(listener, timeout=2)
            except Exception as error:
                server_errors.append(error)

        server_thread = threading.Thread(target=accept_client)
        server_thread.start()

        try:
            with socket.create_connection(("127.0.0.1", port), timeout=2) as connection:
                connection.sendall(b"INVALID\n")
            server_thread.join(timeout=2)

            self.assertFalse(server_thread.is_alive())
            self.assertEqual(1, len(server_errors))
            self.assertIsInstance(server_errors[0], ValueError)
        finally:
            listener.close()

    def test_client_returns_failed_when_server_is_unavailable(self) -> None:
        unavailable_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        unavailable_listener.bind(("127.0.0.1", 0))
        port = unavailable_listener.getsockname()[1]
        unavailable_listener.close()

        status = connect("127.0.0.1", port, timeout=1)

        self.assertEqual(ConnectionStatus.FAILED, status)


if __name__ == "__main__":
    unittest.main()
