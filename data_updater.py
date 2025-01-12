import serial
import time
import json


def read_arduino_serial(port='COM3', baud_rate=9600):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to Arduino on {port}")
        
        time.sleep(2)
        
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                print(line)
                if line:
                    process_line(line)
                    
    except serial.SerialException as e:
        print(f"Error: Could not connect to port {port}: {e}")
    except KeyboardInterrupt:
        print("\nStopping serial monitor...")
    finally:
        if 'ser' in locals():
            ser.close()
            print("Serial connection closed")


def process_line(line):
    print(line)
    moistureLevel = int(line) / 10
    if moistureLevel < 60:
        status = 'Dry'
    else:
        status = 'Wet'

    new_data = {
    "lastIrrigated": "08:30 AM",
    "moistureLevel": moistureLevel,
    "level": "Off",
    "status": status,
    "lastUpdated": int(time.time())

    }
    print(new_data)

    with open('moisture-status.json', 'w') as json_file:
        json.dump(new_data, json_file)


if __name__ == "__main__":
    PORT = 'COM5'
    BAUD_RATE = 115200
    
    read_arduino_serial(PORT, BAUD_RATE)