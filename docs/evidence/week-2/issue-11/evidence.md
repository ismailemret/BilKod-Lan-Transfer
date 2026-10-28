# Issue #11 Evidence

## Test Bilgileri

- **Ortam:** Windows 11 Home Single Language (10.0.26100), Python 3.13.5
- **Kısa Adımlar:** Depo kökünden PowerShell'de
  `python -m unittest discover -s docs/evidence/week-2/issue-11 -p "test_*.py" -v`
  komutunu çalıştır.
- **Kişisel Not:** Generator'dan gelen her blok hemen diske yazılıyor; böylece
  bellek kullanımı dosyanın toplam boyutuna bağlı kalmıyor.

## Uygulama Özeti

- `iter_file_chunks()` dosyayı ikili kipte açıp sabit 64 KB bloklar halinde
  üretir; okuma hatalarını loglayıp yeniden fırlatır.
- `save_chunks_to_temp_file()` parçaları sırasıyla güvenli biçimde
  `filename.part` dosyasına yazar. Önceki haftadaki atomik geçici dosya
  kaydetme mekanizmasını kullanır.
- Kaydetme yarıda kesilirse geçici dosya temizlenir ve parçaları üreten
  iterator kapatılır. Canlı socket kullanılmaz.

## Doğrulama Senaryoları

Çalıştırılan test kodu `test_chunked_transfer.py` dosyasındadır. Testler:

1. 1 MB'tan büyük dosyayı 64 KB üst sınırını aşmadan okur ve `received.bin.part`
   dosyasına yazar; dosya boyutu ve SHA-256 değerini doğrular.
2. Kaynak dosya bulunamadığında hatanın loglanıp çağırana iletilmesini denetler.
3. Hedef dizin bulunamadığında hatanın loglanıp çağırana iletilmesini denetler.
4. Yazma başarısız olursa generator'ın kapatıldığını ve geçici dosyanın
   temizlendiğini doğrular.

## Gerçek Çalıştırma Çıktısı

```text
Python 3.13.5 | Windows 11 Home Single Language (10.0.26100)
test_failed_save_closes_chunk_generator_and_cleans_temp ... ok
test_invalid_destination_is_logged_and_raised ... ok
test_large_file_is_read_in_bounded_chunks_and_saved_to_part ... ok
test_missing_source_is_logged_and_raised ... ok

Ran 4 tests in 0.123s
OK
Error checks: missing source/destination logged and raised; failed stream closed and temp cleaned
Demo: 1,048,832 bytes; 17 chunks; max 65,536; last 256 bytes
Saved: received.bin.part; bytes: 1048832; SHA-256 matches: True
```
