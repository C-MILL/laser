import serial
import time


def main():
    try:
        # Initialize serial connection
        ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)  # Ensure the port matches your setup
        ser.flushInput()
        ser.flushOutput()

        while True:
            try:
                string = input("Enter string: ")  # Input from user
                string = string + "\n"  # "\n" for line separation
                string = string.encode('utf-8')
                ser.write(string)
                print("Sent: ", string)

                # Wait for a response
                time.sleep(1)
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    print("Received: ", line)
                else:
                    print("No response received.")

            except Exception as e:
                print(f"Error during communication: {e}")

    except Exception as e:
        print(f"Failed to establish serial connection: {e}")


if __name__ == '__main__':
    main()
