import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import serial


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load the UI file
        loadUi('fe/main.ui', self)

        # Initialize serial connection to None
        self.ser = None

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

    def check_connection(self):
        try:
            if self.ser is None:
                # Try to establish the connection
                self.ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
                self.ser.flushInput()
                self.ser.flushOutput()
                self.pushButton.setStyleSheet("background-color: green")
                self.ten_left.setEnabled(True)
                self.ten_right.setEnabled(True)
            # Test the connection
            self.ser.write(b'PING\n')
            time.sleep(1)
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').rstrip()
                if response == "PONG":
                    self.pushButton.setStyleSheet("background-color: green")
                    self.ten_left.setEnabled(True)
                    self.ten_right.setEnabled(True)
                else:
                    raise serial.SerialException("Unexpected response")
        except (serial.SerialException, OSError):
            self.pushButton.setStyleSheet("background-color: red")
            self.ten_left.setEnabled(False)
            self.ten_right.setEnabled(False)
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
                time.sleep(1)
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode('utf-8').rstrip()
                    print(f"Received: {response}")
                else:
                    print("No response received.")
            except Exception as e:
                print(f"Error during communication: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
