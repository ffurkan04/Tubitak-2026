import serial
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
arduino_port = "COM7" 
baudrate = 9600

# Sistem ayarları 
message_time = 80    # İki bildirim arası bekleme süresi
min_signal = 4      # Analiz penceresi süresi içinde en az 4 sinyal gelmeli (Tavsiye değer:3)
window_time = 3     # Analiz penceresi

# Mesaj Değişkenleri 
last_message = 0 
hareket_listesi = [] 

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': mesaj}
    try:
        print("Telegram'a istek gönderiliyor...")
        response = requests.get(url, params=params, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return False

# Arduino Bağlantısı
try:
    ser = serial.Serial(arduino_port, baudrate, timeout=1)
    print(f"Sistem aktif: {arduino_port} üzerinden hareket bekleniyor...")
except Exception as e:
    print(f"HATA: Arduino bağlantısı başarısız: {e}")
    ser = None

if ser:
    while True:
        try:
            if ser.in_waiting > 0:
                veri = ser.readline().decode('utf-8').strip()
                
                # Arduino'dan gelen tam mesajı kontrol et
                if veri == "DIKKAT: Enkaz altinda hareket algilandi!":
                    now = time.time()
                    hareket_listesi.append(now)
                    
                    # Pencere dışı kalan eski sinyalleri temizle
                    hareket_listesi = [t for t in hareket_listesi if now - t <= window_time]
                    
                    sinyal_sayisi = len(hareket_listesi)
                    
                    # 1. KONTROL: Yeterli sinyal yoğunluğu var mı? (Gerçek hareket mi?)
                    if sinyal_sayisi >= min_signal:
                        
                        # 2. KONTROL: Spam süresi doldu mu?
                        if now - last_message > message_time:
                            print("!!! DOĞRULANMIŞ HAREKET: Telegram'a gönderiliyor...")
                            if telegram_mesaj_gonder("UYARI: Enkaz altında gerçek hareket algılandı!"):
                                print("Mesaj başarıyla iletildi!")
                                last_message = now
                                hareket_listesi = [] # Gönderdikten sonra temizle
                        else:
                            kalan = int(message_time - (now - last_message))
                            print(f"Hareket doğrulanıyor ancak spam koruması devrede. Bekle: {kalan} sn.")
                    else:
                        print(f"Sinyal alınıyor... Filtre durumu: {sinyal_sayisi}/{min_signal}")
                        
        except Exception as e:
            print(f"Hata: {e}")
            break