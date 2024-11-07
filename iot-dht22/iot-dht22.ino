#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Definicija prilagođenog simbola za stepen
byte degreeSymbol[8] = {
  B00111,
  B00101,
  B00111,
  B00000,
  B00000,
  B00000,
  B00000,
  B00000
};

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    dht.begin();
    
    // Kreiraj prilagođeni karakter za simbol stepena
    lcd.createChar(0, degreeSymbol);
}

void loop() {
    // Očitavanje temperature i vlažnosti
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    // Prikaz na LCD ekranu
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Temp: ");
    lcd.print(temperature);
    lcd.write(byte(0)); // Prikaz prilagođenog simbola za stepen
    lcd.print("C");

    lcd.setCursor(0, 1);
    lcd.print("Vlaz: ");
    lcd.print(humidity);
    lcd.print(" %");

    // Provera da li je primljena komanda
    if (Serial.available() > 0) {
        char command = Serial.read();

        // Ako je primljena komanda "M", šalji podatke u JSON formatu
        if (command == 'M') {
            Serial.print("{\"Rh\": ");
            Serial.print(humidity);
            Serial.print(", \"T\": ");
            Serial.print(temperature);
            Serial.println("}");
        }
    }

    delay(1000); // Pauza od 1 sekunde između osvežavanja ekrana
}
