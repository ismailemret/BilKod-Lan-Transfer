from fixtures.fake_devices import get_mock_devices

def main():
    print("=" * 60)
    print("BİLKOD Proje 1: Yerel Ağda Dosya Paylaşımı")
    print("=" * 60)
    devices = get_mock_devices()
    print(f"[*] Yüklenen sahte cihaz adedi: {len(devices)}")
    for d in devices:
        print(f"  - [{d.device_id}] {d.hostname} ({d.ip_address}:{d.port})")

if __name__ == "__main__":
    main()
