
# pip install opencv-python pyautogui
import cv2 
import time  
import pyautogui  
import webbrowser 
import os  

def send_whatsapp_message():
    
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
      
        pyautogui.hotkey('command', 'w')  
        
        
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
   i
    pyautogui.PAUSE = 1.5  
    
    cap = cv2.VideoCapture(0)  
    
    # Kamera açılamadıysa programı sonlandır
    if not cap.isOpened():
        print("[ERROR] Kamera açılamadı!")
        return


    backSub = cv2.createBackgroundSubtractorMOG2(
        history=500,  
        varThreshold=25,  
        detectShadows=True  
    )

    last_motion_time = 0  

    cooldown = 10  

    while True:
       
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Kamera görüntüsü alınamadı!")
            break
        
        
        fgMask = backSub.apply(frame)  
        
        _, thresh = cv2.threshold(fgMask, 250, 255, cv2.THRESH_BINARY)  
        thresh = cv2.erode(thresh, None, iterations=2)  
        thresh = cv2.dilate(thresh, None, iterations=2)  
        

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False
        
        for contour in contours:
            if cv2.contourArea(contour) < 1500:  
                continue
            motion_detected = True
            break
        
  
        current_time = time.time()

        if motion_detected and (current_time - last_motion_time > cooldown):
            print("[INFO] Hareket tespit edildi!")
            
         
            if send_whatsapp_message():
                last_motion_time = current_time  
              
                cv2.putText(frame, "Hareket Tespit Edildi!", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                print("[WARN] Mesaj gönderilemedi, yeniden deneniyor...")
                time.sleep(5)  
        else:
            
            cv2.putText(frame, "Hareketlilik Yok", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
     
        cv2.imshow("Kamera", frame)  
        cv2.imshow("Hareket Maskesi", thresh)  
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    cap.release()  
    cv2.destroyAllWindows()  


if __name__ == '__main__':
    main()
