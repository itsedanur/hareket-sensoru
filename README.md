#  Hareket Sensörü WhatsApp Alarm Sistemi

Bu Python projesi, bilgisayar kamerası üzerinden hareket algılayarak **otomatik olarak WhatsApp üzerinden uyarı mesajı** gönderir. Özellikle güvenlik sistemleri, ev izleme veya ofislerde uzaktan uyarı almak isteyenler için kullanışlıdır.

##  Özellikler

- Hareket algılama (kamera ile)
- Algılanan hareketlerde otomatik WhatsApp mesajı gönderme
- Mesajda tarih ve saat bilgisi
- Spam engelleme için bekleme süresi
- Gerçek zamanlı görüntüleme arayüzü (kamera ve hareket maskesi)

##  Kullanılan Kütüphaneler

- `opencv-python` (`cv2`)
- `pyautogui`
- `webbrowser`
- `time`
- `os`

## Kurulum

1. Gerekli kütüphaneleri yükle:
   ```bash
   pip install opencv-python pyautogui

 Uyarılar

Program mesajlar arasında 10 saniye bekleme koyar. (Spam koruması)
Tarayıcı otomatik kapanır ama bazı sistemlerde command + w yerine ctrl + w gerekebilir.

👩‍💻 Geliştirici

Eda Nur Unal
