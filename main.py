import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import serial
import serial.tools.list_ports

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load the UI file
        loadUi('fe/main.ui', self)

        # Initialize serial connection to None
        self.ser = None
        self.current_port = None

        # Bind buttons
        self.pushButton.clicked.connect(self.check_connection)
        self.ten_left.clicked.connect(self.send_ten_left)
        self.ten_right.clicked.connect(self.send_ten_right)
        self.motor1_left.clicked.connect(self.send_motor1_left)
        self.motor1_right.clicked.connect(self.send_motor1_right)
        self.motor2_left.clicked.connect(self.send_motor2_left)
        self.motor2_right.clicked.connect(self.send_motor2_right)
        self.set_home.clicked.connect(self.set_home_position)
        self.move_home.clicked.connect(self.move_to_home)
        self.reset_position_btn.clicked.connect(self.reset_position_command)

        # Disable command buttons initially
        self.ten_left.setEnabled(False)
        self.ten_right.setEnabled(False)
        self.motor1_left.setEnabled(False)
        self.motor1_right.setEnabled(False)
        self.motor2_left.setEnabled(False)
        self.motor2_right.setEnabled(False)
        self.set_home.setEnabled(False)
        self.move_home.setEnabled(False)
        self.reset_position_btn.setEnabled(False)

        # Set up a timer to periodically check the connection
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_connection)
        self.timer.start(5000)  # Check every 5 seconds

        # Access labels
        self.connectionStatusLabel = self.findChild(QLabel, 'connectionStatusLabel')
        self.responseLabel = self.findChild(QLabel, 'responseLabel')

    def find_serial_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.device or "ttyACM" in port.device:
                return port.device
        return None

    def check_connection(self):
        try:
            if self.ser is None or not self.ser.is_open:
                # Find available serial port
                port = self.find_serial_port()
                if port:
                    print(f"Attempting to open serial connection on {port}...")
                    self.ser = serial.Serial(port, 9600, timeout=1)
                    self.ser.flushInput()
                    self.ser.flushOutput()
                    self.current_port = port
                    print(f"Serial connection established on {port}.")
                    self.connectionStatusLabel.setText(f"Connection Status: Connected ({port})")
                else:
                    raise serial.SerialException("No USB serial ports found.")

            # Test the connection
            self.ser.write(b'PING\n')
            print("Sent PING to ESP32.")
            time.sleep(1)  # Ensure there's enough delay for a response
            if self.ser.in_waiting > 0:
                try:
                    response = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                    print(f"Received from ESP32: {response}")
                    if response == "PONG":
                        self.pushButton.setStyleSheet("background-color: green")
                        self.ten_left.setEnabled(True)
                        self.ten_right.setEnabled(True)
                        self.motor1_left.setEnabled(True)
                        self.motor1_right.setEnabled(True)
                        self.motor2_left.setEnabled(True)
                        self.motor2_right.setEnabled(True)
                        self.set_home.setEnabled(True)
                        self.move_home.setEnabled(True)
                        self.reset_position_btn.setEnabled(True)
                        self.connectionStatusLabel.setText(f"Connection Status: Connected ({self.current_port})")
                    else:
                        print("Unexpected response")
                        self.responseLabel.setText(f"Unexpected response: {response}")
                except UnicodeDecodeError as e:
                    raw_response = self.ser.readline()
                    print(f"Decoding error: {e}, raw response: {raw_response}")
                    self.responseLabel.setText(f"Decoding error: {e}")
            else:
                print("No response received")
                self.responseLabel.setText("No response received")
        except (serial.SerialException, OSError) as e:
            print(f"Connection check failed: {e}")
            self.pushButton.setStyleSheet("background-color: red")
            self.ten_left.setEnabled(False)
            self.ten_right.setEnabled(False)
            self.motor1_left.setEnabled(False)
            self.motor1_right.setEnabled(False)
            self.motor2_left.setEnabled(False)
            self.motor2_right.setEnabled(False)
            self.set_home.setEnabled(False)
            self.move_home.setEnabled(False)
            self.reset_position_btn.setEnabled(False)
            self.connectionStatusLabel.setText("Connection Status: Not Connected")
            if self.ser is not None:
                self.ser.close()
                self.ser = None

    def send_ten_left(self):
        self.send_command('s 10 200')  # Example command for 10 steps left with speed 200

    def send_ten_right(self):
        self.send_command('c 10 200')  # Example command for 10 steps right with speed 200

    def send_motor1_left(self):
        self.send_command('p 100 200')  # 100 steps left for motor 1 with speed 200

    def send_motor1_right(self):
        self.send_command('c 100 200')  # 100 steps right for motor 1 with speed 200

    def send_motor2_left(self):
        self.send_command('b 100 200')  # 100 steps left for motor 2 with speed 200

    def send_motor2_right(self):
        self.send_command('c 100 200')  # 100 steps right for motor 2 with speed 200

    def set_home_position(self):
        self.send_command('set_home')

    def move_to_home(self):
        self.send_command('move_home')

    def reset_position_command(self):
        self.send_command('reset_position')

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            try:
                command += '\n'
                self.ser.write(command.encode('utf-8'))
                print(f"Sent: {command.strip()}")
                self.responseLabel.setText(f"Sent: {command.strip()}")
                time.sleep(1)
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                    print(f"Received: {response}")
                    self.responseLabel.setText(f"Received: {response}")
                else:
                    print("No response received.")
                    self.responseLabel.setText("No response received.")
            except Exception as e:
                print(f"Error during communication: {e}")
                self.responseLabel.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
