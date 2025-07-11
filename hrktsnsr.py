# Gerekli kütüphanelerin yüklenmesi
# pip install opencv-python pyautogui
import cv2  # OpenCV kütüphanesi - görüntü işleme için
import time  # Zaman işlemleri ve bekleme süreleri için
import pyautogui  # Klavye/fare otomasyonu ve WhatsApp kontrolü için
import webbrowser  # WhatsApp Web'i açmak için
import os  # Dosya ve dizin işlemleri için

def send_whatsapp_message():
    """
    WhatsApp Web üzerinden otomatik mesaj gönderme fonksiyonu.
    Hareket algılandığında çağrılır ve şu işlemleri yapar:
    1. Tarih/saat bilgisi ile mesaj oluşturur
    2. WhatsApp Web'i açar
    3. Mesajı gönderir
    4. Tarayıcı sekmesini kapatır
    """
    # Alıcı telefon numarası - başında ülke kodu olmalı
    phone_number = "+90 BURAYA NUMARANI YAZ"  
    
    # Güncel tarih ve saat bilgisini al (gün saat:dakika formatında)
    timestamp = time.strftime("%d %H:%M")  
    
    # Gönderilecek mesaj metnini oluştur
    message = f"Hareket tespit edildi! Tarih/Saat: {timestamp}"
    
    # WhatsApp Web API URL'sini oluştur
    web_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    
    try:
        # İşlem başlangıç logu
        print(f"[INFO] WhatsApp üzerinden mesaj gönderiliyor: {message}")
        
        # WhatsApp Web'i varsayılan tarayıcıda aç
        webbrowser.open(web_url)  
        
        # WhatsApp Web'in yüklenmesi için bekle (internet hızına göre ayarlanabilir)
        time.sleep(20)  
        
        # Enter tuşuna basarak mesajı gönder
        pyautogui.press('enter')  
        
        # Mesajın iletilmesi için bekle
        time.sleep(5)  
        
        # Tarayıcı sekmesini kapat (Ctrl+W)
        pyautogui.hotkey('ctrl', 'w')  
        
        # Tarayıcının kapanması için son bekleme
        time.sleep(2)  
        
        # Başarılı gönderim logu
        print("[INFO] WhatsApp mesajı gönderildi!")
        return True
        
    except Exception as e:
        # Hata durumunda log
        print("[ERROR] WhatsApp gönderiminde hata oluştu:", e)
        return False

def main():
    """
    Ana program döngüsü.
    Kamera görüntüsünü alır, hareket algılar ve gerektiğinde WhatsApp mesajı gönderir.
    """
    # PyAutoGUI için güvenli bekleme süresi
    pyautogui.PAUSE = 1.5  
    
    # Varsayılan kamerayı başlat (dizüstü bilgisayarlarda genelde dahili kamera)
    cap = cv2.VideoCapture(0)  
    
    # Kamera açılamadıysa programı sonlandır
    if not cap.isOpened():
        print("[ERROR] Kamera açılamadı!")
        return

    # MOG2 arka plan çıkarıcı algoritmasını yapılandır
    backSub = cv2.createBackgroundSubtractorMOG2(
        history=500,  # Son 500 frame'i kullanarak arka planı öğren
        varThreshold=25,  # Hareket hassasiyeti (düşük değer = daha hassas)
        detectShadows=True  # Gölgeleri de tespit et
    )
    
    # Son hareket tespiti zamanını takip et
    last_motion_time = 0  
    
    # İki mesaj arasında beklenecek minimum süre (spam önleme)
    cooldown = 10  

    while True:
        # Kameradan yeni bir görüntü frame'i al
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Kamera görüntüsü alınamadı!")
            break
        
        # Hareket algılama işlem zinciri
        fgMask = backSub.apply(frame)  # Arka plandan farklı olan pikselleri bul
        
        _, thresh = cv2.threshold(fgMask, 250, 255, cv2.THRESH_BINARY)  # Siyah-beyaz görüntüye çevir
        thresh = cv2.erode(thresh, None, iterations=2)  # Gürültüleri temizle
        thresh = cv2.dilate(thresh, None, iterations=2)  # Hareket bölgelerini genişlet
        
        # Hareket eden bölgelerin sınırlarını bul
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False
        
        # Her bir hareket bölgesini kontrol et
        for contour in contours:
            if cv2.contourArea(contour) < 1500:  # Çok küçük hareketleri yoksay
                continue
            motion_detected = True
            break
        
        # Şu anki zamanı al
        current_time = time.time()

        # Hareket varsa ve cooldown süresi geçtiyse
        if motion_detected and (current_time - last_motion_time > cooldown):
            print("[INFO] Hareket tespit edildi!")
            
            # WhatsApp mesajı göndermeyi dene
            if send_whatsapp_message():
                last_motion_time = current_time  # Son hareket zamanını güncelle
                # Ekranda kırmızı yazıyla uyarı göster
                cv2.putText(frame, "Hareket Tespit Edildi!", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                print("[WARN] Mesaj gönderilemedi, yeniden deneniyor...")
                time.sleep(5)  # Hata durumunda 5 saniye bekle
        else:
            # Hareket yoksa yeşil yazıyla normal durum bildirisi
            cv2.putText(frame, "Hareketlilik Yok", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Canlı görüntü ve hareket maskesini göster
        cv2.imshow("Kamera", frame)  # Ana kamera görüntüsü
        cv2.imshow("Hareket Maskesi", thresh)  # Hareket algılama maskesi
        
        # Q tuşuna basılırsa döngüden çık
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Program sonlandığında kaynakları temizle
    cap.release()  # Kamerayı serbest bırak
    cv2.destroyAllWindows()  # Tüm pencereleri kapat

# Program başlangıç noktası
if __name__ == '__main__':
    main()
