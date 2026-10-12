# BilKod - Yerel Ağda Dosya Paylaşımı (LAN File Transfer)

Python 3.10+ standart kütüphanesi (`socket`, `hashlib`, `pathlib`, `threading`, `tkinter`) ile geliştirilen internetsiz yerel ağ dosya transfer aracı.

## Rol Dağılımı ve Sınırlar
- **K1:** network/, discovery/
- **K2:** transfer/, storage/
- **K3:** ui/, docs/ui/
- **Lider:** core/, contracts/, fixtures/, app.py, tests/integration/
