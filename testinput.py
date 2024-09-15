from serial import Serial
ser = Serial('/dev/cu.usbserial-11340', 9600)

while(True):
    ser.write(input().encode())