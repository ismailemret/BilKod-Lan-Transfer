<<<<<<< HEAD
"""Local-network device discovery functionality."""
from dataclasses import dataclass
from typing import List, Optional, Protocol
from network import ConnectionStatus


@dataclass
class DeviceInfo:
    device_id: str
    name: str
    ip_address: str
    port: int
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED


class DeviceProvider(Protocol):
    def get_devices(self) -> List[DeviceInfo]:
        ...

    def get_device_by_id(self, device_id: str) -> Optional[DeviceInfo]:
        ...


class MockDeviceProvider:
    def __init__(self) -> None:
        self._devices: List[DeviceInfo] = [
            DeviceInfo(
                device_id="dev-001",
                name="Masaüstü-PC",
                ip_address="192.168.1.10",
                port=8080,
                status=ConnectionStatus.CONNECTED,
            ),
            DeviceInfo(
                device_id="dev-002",
                name="Dizüstü-Bilgisayar",
                ip_address="192.168.1.11",
                port=8080,
                status=ConnectionStatus.DISCONNECTED,
            ),
            DeviceInfo(
                device_id="dev-003",
                name="Mobil-Cihaz",
                ip_address="192.168.1.12",
                port=8080,
                status=ConnectionStatus.CONNECTING,
            ),
        ]

    def get_devices(self) -> List[DeviceInfo]:
        return list(self._devices)

    def get_device_by_id(self, device_id: str) -> Optional[DeviceInfo]:
        for device in self._devices:
            if device.device_id == device_id:
                return device
        return None
=======
"""Local-network device discovery functionality."""
from typing import List, Optional, Protocol
from contracts.models import ConnectionStatus, DeviceInfo


class DeviceProvider(Protocol):
    def get_devices(self) -> List[DeviceInfo]:
        ...

    def get_device_by_id(self, device_id: str) -> Optional[DeviceInfo]:
        ...


class MockDeviceProvider:
    def __init__(self) -> None:
        self._devices: List[DeviceInfo] = [
            DeviceInfo(
                device_id="dev-001",
                name="Masaüstü-PC",
                ip_address="192.168.1.10",
                port=8080,
                status=ConnectionStatus.CONNECTED,
            ),
            DeviceInfo(
                device_id="dev-002",
                name="Dizüstü-Bilgisayar",
                ip_address="192.168.1.11",
                port=8080,
                status=ConnectionStatus.DISCONNECTED,
            ),
            DeviceInfo(
                device_id="dev-003",
                name="Mobil-Cihaz",
                ip_address="192.168.1.12",
                port=8080,
                status=ConnectionStatus.CONNECTING,
            ),
        ]

    def get_devices(self) -> List[DeviceInfo]:
        return list(self._devices)

    def get_device_by_id(self, device_id: str) -> Optional[DeviceInfo]:
        for device in self._devices:
            if device.device_id == device_id:
                return device
        return None
>>>>>>> d8fe679 (Update device discovery and networking)
