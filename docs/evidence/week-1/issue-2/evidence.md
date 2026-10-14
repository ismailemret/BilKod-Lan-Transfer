# Issue #2 Evidence

## 1. Başarılı Akış / Metadata ve Storage Terminal Logları

```text
Python 3.13.5 | unittest: TransferStorageSmokeTests
test_chunk_storage_and_path_traversal_sanitization ... ok
test_failed_write_preserves_existing_file_and_cleans_temp ... ok
test_missing_destination_is_logged_and_raised ... ok
test_missing_source_is_logged_and_raised ... ok
test_offer_metadata_and_chunked_sha256 ... ok

Ran 5 tests in 0.073s
OK
```

## 2. Hata Yönetimi Senaryosu Terminal Logu

```text
test_missing_destination_is_logged_and_raised ... ok
test_missing_source_is_logged_and_raised ... ok
test_failed_write_preserves_existing_file_and_cleans_temp ... ok

Beklenen hata durumlarında logger kayıtları assertLogs ile doğrulandı ve
istisnaların çağırana iletildiği kontrol edildi. Başarısız yazma, mevcut
hedef dosyanın içeriğini değiştirmedi ve geçici dosya bırakmadı.
```

## 3. Ekip Üyesi Açıklaması

### Ne Yaptım? (Özet)

Transfer teklifi için dosya adı, bayt boyutu ve parça parça hesaplanan
SHA-256 özetini oluşturan işlevleri ekledim. Storage katmanında dosya adını
hedef dizinle sınırlandırıp TransferChunk veya bayt dizilerini geçici dosyaya
yazdıktan sonra hedefe taşıyan kaydetme işlevini ekledim. Ağ aktarımı
uygulanmadı.

### Değiştirilen Dosyalar

- `transfer/transfer.py`
- `storage/storage.py`

### Nasıl Test Ettim?

Python 3.13.5 ile geçici dosyalar üzerinde beş odaklı unittest çalıştırdım.
Metadata alanlarını ve SHA-256 sonucunu bağımsız `hashlib.sha256` hesabıyla
karşılaştırdım; dosya kaydetme, Windows tarzı yol temizleme, kaynak/hedef
bulunamadığında loglama ve hata iletimi, başarısız yazmada geçici dosya
temizliği senaryolarını doğruladım.

### Kısıt ve Mimari Kontrol Beyanı

- [x] Yalnızca atanan `transfer/`, `storage/` ve bu görev kanıt dosyasında çalışıldı.
- [x] Uygulama kodunda `print()` kullanılmadı.
- [x] Değiştirilen kod satır satır gözden geçirildi; çalışma mantığı doğrulandı.
