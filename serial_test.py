import serial, time

ser = serial.Serial('COM6', 115200, timeout=1)
print("Listening on", ser.port)
try:
    while True:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if line:
            print("RAW >", line)
        time.sleep(0.01)
except KeyboardInterrupt:
    ser.close()
    print("Closed")
