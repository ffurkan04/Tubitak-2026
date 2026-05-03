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

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    try:
        requests.get(url)
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

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
                    print("Hareket algilandi! Telegram'a gonderiliyor...")
                    telegram_mesaj_gonder("UYARI: Enkaz altında hareket algılandı!")
        except Exception as e:
            print(f"Bağlantı koptu: {e}")
            break
else:
    print("Program bağlantı sağlanamadığı için başlatılamadı. Lütfen portu kontrol edip tekrar çalıştırın.")