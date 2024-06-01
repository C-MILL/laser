import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import serial
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Load the UI file
        loadUi('fe/main.ui', self)

        # Initialize serial connection
        self.ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)  # Adjust the port as necessary

        # Bind buttons
        self.ten_left.clicked.connect(self.send_ten_left)
        self.ten_right.clicked.connect(self.send_ten_right)

    def send_ten_left(self):
        self.send_command('10L')

    def send_ten_right(self):
        self.send_command('10R')

    def send_command(self, command):
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
