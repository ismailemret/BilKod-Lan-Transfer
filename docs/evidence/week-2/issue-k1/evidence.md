# W2-K1 Kanıtı: Yerel Ağda Dinleyici ve Doğrudan Soket Bağlantısı

## Hedef

Yerel TCP sunucusunun dinleme yapmasını, istemcinin PING mesajı göndermesini,
sunucunun PONG yanıtı vermesini ve beklenmeyen mesaj/hizmet yokluğu
durumlarında güvenli biçimde hata vermesini doğrulamak.

## Değiştirilen Dosyalar

- `network/server.py`
- `network/client.py`
- `docs/evidence/week-2/issue-k1/test_network_listener.py`
- `docs/evidence/week-2/issue-k1/evidence.md`

## Çalıştırma Komutu

Depo kökünden PowerShell açıp çalıştırın:

```powershell
python -m unittest discover `
  -s docs/evidence/week-2/issue-k1 `
  -p "test_*.py" `
  -v
```

Windows'ta Python komutu aynı makinedeyse `python` yerine sistem Python
başlatıcısını kullanabilirsiniz.

## Test Senaryoları

1. Loopback üzerinde dinleyici açılır.
2. Ayrı bir istemci PING gönderir.
3. Sunucu PONG yanıtı gönderir ve istemci `CONNECTED` döndürür.
4. Geçersiz istemci mesajı `ValueError` üreterek bağlantıyı kapatır.
5. Kullanılmayan porta bağlanıldığında istemci `FAILED` döndürür.

## Beklenen Çıktı

```text
test_direct_ping_pong_connection ... ok
test_rejected_message_closes_connection ... ok
test_client_returns_failed_when_server_is_unavailable ... ok

----------------------------------------------------------------------
Ran 3 tests in ...s

OK
```

## Gerçek Çıktı

Çalıştırma sonucu:

```text
test_client_returns_failed_when_server_is_unavailable ... 2026-11-25 17:37:24,999 | ERROR | network.client | Sunucuya bağlanırken socket hatası
... 
ok
test_direct_ping_pong_connection ... 2026-11-25 17:38:27,090 | INFO | network.server | Sunucu 127.0.0.1:51324 adresinde dinliyor
2026-11-25 17:38:27,091 | INFO | network.server | İstemci bağlandı: ('127.0.0.1', 51325)
2026-11-25 17:38:27,091 | INFO | network.server | El sıkışma tamamlandı
2026-11-25 17:38:27,091 | INFO | network.client | Bağlantı durumu: CONNECTED; sunucu yanıtı: PONG
ok
test_rejected_message_closes_connection ... 2026-11-25 17:38:27,091 | INFO | network.server | Sunucu 127.0.0.1:51326 adresinde dinliyor
2026-11-25 17:38:27,092 | INFO | network.server | İstemci bağlandı: ('127.0.0.1', 51327)
ok

----------------------------------------------------------------------
Ran 3 tests in 1.046s

OK
```

İki ayrı terminalle elle doğrulama kontrolü:

Terminal 1:

```
2026-11-25 17:43:32,495 | INFO | __main__ | Sunucu 0.0.0.0:5050 adresinde dinliyor
2026-11-25 17:43:40,251 | INFO | __main__ | İstemci bağlandı: ('127.0.0.1', 63328)
2026-11-25 17:43:40,251 | INFO | __main__ | El sıkışma tamamlandı
```

Terminal 2:

```
2026-11-25 17:43:40,251 | INFO | __main__ | Bağlantı durumu: CONNECTED; sunucu yanıtı: PONG
2026-11-25 17:43:40,252 | INFO | __main__ | Son bağlantı durumu: CONNECTED
```


## Sınır Kontrolü

- Yalnızca `network/`, `docs/evidence/week-2/issue-k1/` ve doğrudan
  kullandığımız mevcut `contracts/models.py` sınırlarında çalışıldı.
- Transfer, storage, UI veya lider klasörlerine değişiklik yapılmadı.
- Gerçek dosya aktarımı yapılmadı; görev yalnızca dinleyici ve direkt socket
  bağlantısını kapsar.
