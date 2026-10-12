from typing import List
from contracts.models import DeviceInfo

FAKE_DEVICES: List[DeviceInfo] = [
    DeviceInfo(device_id="dev-01", hostname="Laptop-Alpha", ip_address="192.168.1.101", port=50001, is_self=False),
    DeviceInfo(device_id="dev-02", hostname="Desktop-Bravo", ip_address="192.168.1.102", port=50001, is_self=False),
    DeviceInfo(device_id="dev-self", hostname="Local-Host", ip_address="127.0.0.1", port=50001, is_self=True),
]

def get_mock_devices() -> List[DeviceInfo]:
    return list(FAKE_DEVICES)
