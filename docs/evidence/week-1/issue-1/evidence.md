<<<<<<< HEAD
# Issue #1 Evidence

## 1. Başarılı Akış / El Sıkışma Terminal Logları

```text
Gerçek sunucu ve istemci loglarını buraya elle yapıştırın.
```

## 2. Hata Yönetimi Senaryosu Terminal Logu

```text
Gerçek hata senaryosu logunu buraya elle yapıştırın.
```

## 3. Ekip Üyesi Açıklaması

### Ne Yaptım? (Özet)

Bu bölümü ekip üyesi kendi cümleleriyle elle doldurur.

### Değiştirilen Dosyalar

Bu bölümü ekip üyesi kendi cümleleriyle elle doldurur.

### Nasıl Test Ettim?

Bu bölümü ekip üyesi kendi cümleleriyle elle doldurur.

### Kısıt ve Mimari Kontrol Beyanı

- [ ] Sadece kendi klasörümde çalıştım.
- [ ] `print()` kullanmadım.
- [ ] Kodu satır satır okudum ve çalışma mantığını biliyorum.
=======
# Issue #1 Evidence

## 1. Başarılı Akış / El Sıkışma Terminal Logları

``
// Başarılı Akış Log
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import logging; logging.basicConfig(level=logging.INFO); from network.server import TCPServer; server=TCPServer('127.0.0.1', 8080); server.start(); conn, addr=server.accept_connection(); conn.close(); server.close()
                                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\BİLKOD\BilKod-Lan-Transfer\network\__init__.py", line 3, in <module>
    from .client import TCPClient
  File "C:\BİLKOD\BilKod-Lan-Transfer\network\client.py", line 6, in <module>
    from utils.logger import logger
ImportError: cannot import name 'logger' from 'utils.logger' (C:\BİLKOD\BilKod-Lan-Transfer\utils\logger.py)


// Başarılı El Sıkma Log
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import logging; logging.basicConfig(level=logging.INFO); from network.client import TCPClient; client=TCPClient('127.0.0.1', 8080); client.connect(); client.close()
                                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\BİLKOD\BilKod-Lan-Transfer\network\__init__.py", line 3, in <module>
    from .client import TCPClient
  File "C:\BİLKOD\BilKod-Lan-Transfer\network\client.py", line 6, in <module>
    from utils.logger import logger
ImportError: cannot import name 'logger' from 'utils.logger' (C:\BİLKOD\BilKod-Lan-Transfer\utils\logger.py)
```

## 2. Hata Yönetimi Senaryosu Terminal Logu

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import logging; logging.basicConfig(level=logging.INFO); from network.client import TCPClient; TCPClient('127.0.0.1', 1, timeout=2).connect()
                                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\BİLKOD\BilKod-Lan-Transfer\network\__init__.py", line 3, in <module>
    from .client import TCPClient
  File "C:\BİLKOD\BilKod-Lan-Transfer\network\client.py", line 6, in <module>
    from utils.logger import logger
ImportError: cannot import name 'logger' from 'utils.logger' (C:\BİLKOD\BilKod-Lan-Transfer\utils\logger.py)
```

## 3. Ekip Üyesi Açıklaması

### Ne Yaptım? (Özet)

TCP sunucusu ekledim. hedef IP ve porta bağlanabilme yeteneği ekledim. Log çağrılarını dinleyebilme yeteneğide ekledim.

### Değiştirilen Dosyalar

discovery->__init__.py, discovery->discovery_.py, network->__init__.py, networky->client.py, networky->server.py

### Nasıl Test Ettim?

Gemini ve Copilot yapay zekaları üzerinden ayrı ayrı test ettirdim.

### Kısıt ve Mimari Kontrol Beyanı

- [+] Sadece kendi klasörümde çalıştım.
- [+] `print()` kullanmadım.
- [+] Kodu satır satır okudum ve çalışma mantığını biliyorum.
>>>>>>> d8fe679 (Update device discovery and networking)
