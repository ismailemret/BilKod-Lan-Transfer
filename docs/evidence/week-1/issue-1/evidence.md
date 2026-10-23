# Issue #1 Evidence

## 1. Başarılı Akış / El Sıkışma Terminal Logları

```text
1. Terminal log:
2026-10-22 18:40:24,138 | INFO | __main__ | Sunucu 0.0.0.0:5050 adresinde dinliyor
2026-10-22 18:40:33,610 | INFO | __main__ | İstemci bağlandı: ('127.0.0.1', 51324)
2026-10-22 18:40:33,630 | INFO | __main__ | El sıkışma tamamlandı

2. Terminal log:
2026-10-22 18:40:33,630 | INFO | __main__ | Bağlantı durumu: CONNECTED; sunucu yanıtı: PONG
2026-10-22 18:40:33,630 | INFO | __main__ | Son bağlantı durumu: CONNECTED
```

## 2. Hata Yönetimi Senaryosu Terminal Logu

```text
2026-10-22 18:44:52,049 | ERROR | __main__ | Sunucuya bağlanırken socket hatası
Traceback (most recent call last):
  File "C:\BilKod-Lan-Transfer\network\client.py", line 19, in connect
    with socket.create_connection(
         ~~~~~~~~~~~~~~~~~~~~~~~~^
        (SERVER_HOST, PORT),
        ^^^^^^^^^^^^^^^^^^^^
        timeout=10,
        ^^^^^^^^^^^
    ) as connection:
    ^
  File "C:\Users\ENBA\AppData\Local\Programs\Python\Python313\Lib\socket.py", line 864, in create_connection
    raise exceptions[0]
  File "C:\Users\ENBA\AppData\Local\Programs\Python\Python313\Lib\socket.py", line 849, in create_connection
    sock.connect(sa)
    ~~~~~~~~~~~~^^^^
ConnectionRefusedError: [WinError 10061] Hedef makine etkin olarak reddettiğinden bağlantı kurulamadı
2026-10-22 18:44:52,060 | INFO | __main__ | Son bağlantı durumu: FAILED
```

## 3. Ekip Üyesi Açıklaması

### Ne Yaptım? (Özet)

TCP istemci-sunucu bağlantı iskeletini oluşturdum. Sunucu 5050 portunda dinliyor; istemci PING mesajı gönderiyor ve sunucudan PONG yanıtı alıyor. Socket hataları logger ile kaydediliyor ve bağlantı durumları ConnectionStatus enum'u ile raporlanıyor.

### Değiştirilen Dosyalar

- `network/client.py`
- `network/server.py`

### Nasıl Test Ettim?

Başarılı bağlantı testi için önce terminalden `python -m network.server` komutuyla sunucuyu, ardından ayrı bir terminalde `python -m network.client` komutuyla istemciyi çalıştırdım. İstemcinin PONG yanıtı aldığını ve CONNECTED durumunu; sunucunun da istemci bağlantısını kabul edip el sıkışmayı tamamladığını loglardan doğruladım.

Hata senaryosu için sunucu çalışmıyorken `python -m network.client` komutunu çalıştırdım. ConnectionRefusedError oluştuğunu ve istemcinin FAILED durumunu logladığını doğruladım.

### Kısıt ve Mimari Kontrol Beyanı

- [x] Sadece kendi klasörümde çalıştım.
- [x] `print()` kullanmadım.
- [x] Kodu satır satır okudum ve çalışma mantığını biliyorum.
