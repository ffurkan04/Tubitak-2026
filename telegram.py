#Mesajın telegram üzerinden gönderilmesi için gerekli olan dosya
#pushbyllet.py ile beraber kullanılmasına gerek yoktur. 
import serial
import requests

# Ayarlar
TOKEN = "SENIN_BOT_TOKENIN"
CHAT_ID = "SENIN_CHAT_ID_NUMARAN"

arduino_port = "COM7" # Arduino'nun bağlı olduğu port
baudrate = 9600  #Baudrate değeri

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    requests.get(url)

# Arduino ile bağlantıyı başlat
try:
    ser = serial.Serial(arduino_port, baudrate)
    print("Sistem aktif, hareket bekleniyor...")
except:
    print("Arduino bulunamadi! Portu kontrol et.")

while True:
    if ser.in_waiting > 0:
        veri = ser.readline().decode('utf-8').strip()
        if veri == "HAREKET":
            print("Hareket algilandi! Telegram'a gonderiliyor...")
            telegram_mesaj_gonder("UYARI: Enkaz altında hareket algılandı!")