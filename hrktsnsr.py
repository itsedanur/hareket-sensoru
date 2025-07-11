
# pip install opencv-python pyautogui
import cv2 
import time  
import pyautogui  
import webbrowser 
import os  

def send_whatsapp_message():
    """
    WhatsApp Web üzerinden otomatik mesaj gönderme fonksiyonu.
    Hareket algılandığında çağrılır ve şu işlemleri yapar:
    1. Tarih/saat bilgisi ile mesaj oluşturur
    2. WhatsApp Web'i açar
    3. Mesajı gönderir
    4. Tarayıcı sekmesini kapatır
    """

    phone_number = "+90 BURAYA NUMARANI YAZ"  

    timestamp = time.strftime("%d %H:%M")  
    

    message = f"Hareket tespit edildi! Tarih/Saat: {timestamp}"
    

    web_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    
    try:
    
        print(f"[INFO] WhatsApp üzerinden mesaj gönderiliyor: {message}")
        
        
        webbrowser.open(web_url)  
    
        time.sleep(20)  
        
       
        pyautogui.press('enter')  
        
       
        time.sleep(5)  
      
        pyautogui.hotkey('ctrl', 'w')  
        
        
        time.sleep(2)  
        
 
        print("[INFO] WhatsApp mesajı gönderildi!")
        return True
        
    except Exception as e:
      
        print("[ERROR] WhatsApp gönderiminde hata oluştu:", e)
        return False

def main():
    """
    Ana program döngüsü.
    Kamera görüntüsünü alır, hareket algılar ve gerektiğinde WhatsApp mesajı gönderir.
    """
    # PyAutoGUI için güvenli bekleme süresi
    pyautogui.PAUSE = 1.5  
    
    cap = cv2.VideoCapture(0)  
    
    # Kamera açılamadıysa programı sonlandır
    if not cap.isOpened():
        print("[ERROR] Kamera açılamadı!")
        return


    backSub = cv2.createBackgroundSubtractorMOG2(
        history=500,  # Son 500 frame'i kullanarak arka planı öğren
        varThreshold=25,  # Hareket hassasiyeti (düşük değer = daha hassas)
        detectShadows=True  # Gölgeleri de tespit et
    )

    last_motion_time = 0  

    cooldown = 10  

    while True:
        # Kameradan yeni bir görüntü frame'i al
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Kamera görüntüsü alınamadı!")
            break
        
        
        fgMask = backSub.apply(frame)  # Arka plandan farklı olan pikselleri bul
        
        _, thresh = cv2.threshold(fgMask, 250, 255, cv2.THRESH_BINARY)  # Siyah-beyaz görüntüye çevir
        thresh = cv2.erode(thresh, None, iterations=2)  # Gürültüleri temizle
        thresh = cv2.dilate(thresh, None, iterations=2)  # Hareket bölgelerini genişlet
        

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False
        
        for contour in contours:
            if cv2.contourArea(contour) < 1500:  # Çok küçük hareketleri yoksay
                continue
            motion_detected = True
            break
        
  
        current_time = time.time()

        if motion_detected and (current_time - last_motion_time > cooldown):
            print("[INFO] Hareket tespit edildi!")
            
         
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

   
    cap.release()  # Kamerayı serbest bırak
    cv2.destroyAllWindows()  # Tüm pencereleri kapat

# Program başlangıç noktası
if __name__ == '__main__':
    main()
