"""Local-network device discovery functionality."""
from contracts.models import DeviceInfo
from fixtures.fake_devices import get_mock_devices


def discover_devices() -> list[DeviceInfo]:
    """Demo/test için sahte cihaz listesini döndürür."""
    return get_mock_devices()