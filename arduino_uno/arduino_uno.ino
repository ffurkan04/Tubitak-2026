int PIRPin = 2;
void setup() {
  Serial.begin(9600);  // Bilgisayar ile iletişimi başlat
  pinMode(2, INPUT);   // Sensörü 2. pine bağladık
}

void loop() {
  int hareket = digitalRead(PIRPin);  // Hareket var mı bak
  if (hareket == HIGH) {
    Serial.println("DIKKAT: Enkaz altinda hareket algilandi!");
  } else {
    Serial.println("Hareket yok...");
  }
  delay(350);  // 0.35 saniyede bir kontrol et. Tavsiye değer: 550
}