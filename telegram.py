import serial
import requests
import os
import time # Hatalarda beklemek için ekledik
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
arduino_port = "COM7" 
baudrate = 9600

# Mesaj atmak için aradaki ara
message_time = 80 #60 saniye 
last_message = 0 #son mesajın atıldığı zamanı tutar. 
 
def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': mesaj
    }
    try:
        print("Telegram'a istek gönderiliyor...") # Log ekledik
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("Mesaj başarıyla iletildi!")
        else:
            print(f"Mesaj gönderilemedi! Hata Kodu: {response.status_code}")
            print(f"Sunucu Yanıtı: {response.text}")
            
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")

# --- Arduino Bağlantısını Başlatma ---
ser = None # ser değişkenini başta boş olarak tanımlıyoruz

try:
    ser = serial.Serial(arduino_port, baudrate, timeout=1)
    print(f"Sistem aktif: {arduino_port} üzerinden hareket bekleniyor...")
except Exception as e:
    print(f"HATA: Arduino bulunamadı! {arduino_port} portu meşgul olabilir veya yanlış olabilir.")
    print(f"Detaylı Hata: {e}")

# --- Ana Döngü ---
if ser: # Sadece bağlantı varsa döngüye gir
    while True:
        try:
            if ser.in_waiting > 0:
                veri = ser.readline().decode('utf-8').strip()
                if veri == "DIKKAT: Enkaz altinda hareket algilandi!": #Arduino tarafından gönderilen mesaj. 
                    now = time.time() #şu anı alıyor.
                    if now-last_message>message_time: 
                        print("Hareket algilandi! Telegram'a gonderiliyor...")
                        telegram_mesaj_gonder("UYARI: Enkaz altında hareket algılandı!")
                        last_message = now
                    else : 
                        kalan_sure = int(message_time - (now-last_message))
                        print(f"Hareket var ama spam koruması aktif. Beklenen süre: {kalan_sure} sn.")
                    
        except Exception as e:
            print(f"Bağlantı koptu: {e}")
            break
else:
    print("Program bağlantı sağlanamadığı için başlatılamadı. Lütfen portu kontrol edip tekrar çalıştırın.")