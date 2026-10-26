# Issue #11 Evidence

## Uygulama Özeti

- `iter_file_chunks()` dosyayı ikili kipte açıp sabit 64 KB bloklar halinde
  üretir; okuma hatalarını loglayıp yeniden fırlatır.
- `save_chunks_to_temp_file()` parçaları sırasıyla güvenli biçimde
  `filename.part` dosyasına yazar. Önceki haftadaki atomik geçici dosya
  kaydetme mekanizmasını kullanır.
- Kaydetme yarıda kesilirse geçici dosya temizlenir ve parçaları üreten
  iterator kapatılır. Canlı socket kullanılmaz.

## Doğrulama Kodu

PowerShell terminalinde depo kökünden Python 3.13 ile aşağıdaki doğrulama
çalıştırıldı. Test, 1 MB'tan büyük dosya oluşturur, okuyucu ile storage
arasında generator kullanır ve başarı/hata senaryolarını denetler.

```python
import hashlib
import tempfile
import unittest
from pathlib import Path

from storage.storage import save_chunks_to_temp_file
from transfer.transfer import TRANSFER_CHUNK_SIZE_BYTES, iter_file_chunks


class ChunkedTransferTests(unittest.TestCase):
    def test_large_file_is_read_in_bounded_chunks_and_saved_to_part(self):
        payload = bytes(range(256)) * 4097
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.bin"
            source.write_bytes(payload)
            lengths = []

            def measured_chunks():
                for chunk in iter_file_chunks(source):
                    lengths.append(len(chunk))
                    yield chunk

            part_path = save_chunks_to_temp_file(root, "received.bin", measured_chunks())
            self.assertEqual(part_path.name, "received.bin.part")
            self.assertEqual(part_path.read_bytes(), payload)
            self.assertEqual(sum(lengths), len(payload))
            self.assertEqual(max(lengths), TRANSFER_CHUNK_SIZE_BYTES)
            self.assertEqual(lengths[-1], len(payload) % TRANSFER_CHUNK_SIZE_BYTES)
            self.assertEqual(
                hashlib.sha256(part_path.read_bytes()).digest(),
                hashlib.sha256(payload).digest(),
            )
            source.unlink()
            self.assertFalse(source.exists())
            print(
                f"Demo: {len(payload):,} bytes; {len(lengths)} chunks; "
                f"max {max(lengths):,}; last {lengths[-1]} bytes"
            )
            print(
                f"Saved: {part_path.name}; bytes: {part_path.stat().st_size}; "
                "SHA-256 matches: True"
            )

    def test_missing_source_is_logged_and_raised(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertLogs("transfer.transfer", level="ERROR"):
                with self.assertRaises(FileNotFoundError):
                    list(iter_file_chunks(Path(temp) / "missing.bin"))

    def test_invalid_destination_is_logged_and_raised(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertLogs("storage.storage", level="ERROR"):
                with self.assertRaises(FileNotFoundError):
                    save_chunks_to_temp_file(
                        Path(temp) / "missing", "file.bin", [b"x"]
                    )

    def test_failed_save_closes_chunk_generator_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = {"closed": False}

            def invalid_chunks():
                try:
                    yield b"partial"
                    yield "not bytes"
                finally:
                    state["closed"] = True

            with self.assertLogs("storage.storage", level="ERROR"):
                with self.assertRaises(TypeError):
                    save_chunks_to_temp_file(
                        root, "file.bin", invalid_chunks()
                    )
            self.assertTrue(state["closed"])
            self.assertEqual(list(root.glob(".bilkod-*.tmp")), [])
            self.assertFalse((root / "file.bin.part").exists())
            print(
                "Error checks: missing source/destination logged and raised; "
                "failed stream closed and temp cleaned"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## Gerçek Çalıştırma Çıktısı

```text
Python 3.13.5
test_failed_save_closes_chunk_generator_and_cleans_temp ... ok
test_invalid_destination_is_logged_and_raised ... ok
test_large_file_is_read_in_bounded_chunks_and_saved_to_part ... ok
test_missing_source_is_logged_and_raised ... ok

Ran 4 tests in 0.055s
OK
Error checks: missing source/destination logged and raised; failed stream closed and temp cleaned
Demo: 1,048,832 bytes; 17 chunks; max 65,536; last 256 bytes
Saved: received.bin.part; bytes: 1048832; SHA-256 matches: True
```
