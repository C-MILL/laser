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

        # Disable command buttons initially
        self.ten_left.setEnabled(False)
        self.ten_right.setEnabled(False)

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
            if "USB" in port.device:
                return port.device
        return None

    def check_connection(self):
        try:
            if self.ser is None or not self.ser.is_open:
                # Find available serial port
                port = self.find_serial_port()
                if port:
                    print(f"Attempting to open serial connection on {port}...")
                    self.ser = serial.Serial(port, 115200, timeout=1)
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
            time.sleep(1)
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').rstrip()
                print(f"Received from ESP32: {response}")
                if response == "PONG":
                    self.pushButton.setStyleSheet("background-color: green")
                    self.ten_left.setEnabled(True)
                    self.ten_right.setEnabled(True)
                    self.connectionStatusLabel.setText(f"Connection Status: Connected ({self.current_port})")
                else:
                    raise serial.SerialException("Unexpected response")
            else:
                raise serial.SerialException("No response received")
        except (serial.SerialException, OSError) as e:
            print(f"Connection check failed: {e}")
            self.pushButton.setStyleSheet("background-color: red")
            self.ten_left.setEnabled(False)
            self.ten_right.setEnabled(False)
            self.connectionStatusLabel.setText("Connection Status: Not Connected")
            if self.ser is not None:
                self.ser.close()
                self.ser = None

    def send_ten_left(self):
        self.send_command('10L')

    def send_ten_right(self):
        self.send_command('10R')

    def send_command(self, command):
        if self.ser and self.ser.is_open:
            try:
                command += '\n'
                self.ser.write(command.encode('utf-8'))
                print(f"Sent: {command.strip()}")
                self.responseLabel.setText(f"Sent: {command.strip()}")
                time.sleep(1)
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode('utf-8').rstrip()
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
