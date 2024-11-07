import serial
import time
import json
from datetime import datetime

# Konfiguracija serijskog porta
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

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
                    
                    # Dobijanje trenutnog vremena
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Ispis podataka u konzoli
                    print(f"{current_time} - Temperature: {temperature}°C, Humidity: {humidity}%")
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
