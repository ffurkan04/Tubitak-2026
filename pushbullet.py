#Mesajın pushbullet üzerinden gönderilmesi için gerekli olan dosya
#telegram.py ile beraber kullanılmasına gerek yoktur. 
import serial
import time
from pushbullet import Pushbullet

port = 'COM7'  #Kullanılan port 
baudrate = 9600  #Baudrate değeri

# Ayarlar
pb = Pushbullet("SENIN_API_ANAHTARIN")
arduino = serial.Serpytial(port, baudrate) 

print("Sistem aktif, hareket bekleniyor...")

while True:
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').strip()
        if line == "HAREKET":
            print("Hareket algılandı! Telefona mesaj gönderiliyor...")
            pb.push_note("Uyarı!","Enkaz altında hareket algılandı!")
            time.sleep(2)