import serial
import time
if __name__ == '__main__':
    # if connected via serial Pin(RX, TX)
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1) #9600 is baud rate(must be same with that of NodeMCU)
    ser.flush()
while True:
        string = input("enter string:") #input from user
        string = string +"\n" #"\n" for line seperation
        string = string.encode('utf_8')
        ser.write(string)
        print("  ")
        line = ser.readline().decode('utf-8').rstrip()
        print("received: ",line)
        time.sleep(1) #delay of 1 second