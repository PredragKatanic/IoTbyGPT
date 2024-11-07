import serial
import time
import json
import requests
from datetime import datetime

# Konfiguracija serijskog porta
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
API_URL = 'http://127.0.0.1:8000/api/measurements/'

def main():
    # Povezivanje na serijski port
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Povezan na serijski port: {SERIAL_PORT} sa brzinom {BAUD_RATE} bps")
        
        while True:
            # Slanje komande "M" uređaju
            ser.write(b'M\n')
            
            # Čitanje odgovora sa serijskog porta
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                try:
                    # Parsiranje JSON podataka
                    data = json.loads(line)
                    temperature = data.get("T")
                    humidity = data.get("Rh")
                    
                    if temperature is not None and humidity is not None:
                        # Slanje podataka na Backend API
                        payload = {
                            "temperature": temperature,
                            "humidity": humidity
                        }
                        try:
                            response = requests.post(API_URL, json=payload)
                            response.raise_for_status()
                            print(f"Podaci poslati na API: {payload}")
                        except requests.RequestException as e:
                            print(f"Greška prilikom slanja podataka na API: {e}")
                except json.JSONDecodeError:
                    # Ispis greške pri parsiranju JSON-a
                    print(f"Greška u parsiranju JSON podataka: {line}")
            
            # Pauza od 1 sekunde pre slanja naredne komande
            time.sleep(1)
    
    except serial.SerialException as e:
        print(f"Greška prilikom otvaranja serijskog porta: {e}")
    
    except KeyboardInterrupt:
        print("Prekid programa.")
    
    finally:
        # Zatvaranje serijskog porta kada se program završi
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serijski port zatvoren.")

if __name__ == "__main__":
    main()
