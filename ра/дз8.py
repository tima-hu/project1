# client.py
import sys
import socket
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)

HOST = '127.0.0.1'
PORT = 65432

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Клиент: регистрация пользователей")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.user_list = QListWidget()

        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        btn_layout = QHBoxLayout()
        self.send_button = QPushButton("Отправить")
        self.list_button = QPushButton("Получить список")
        self.clear_button = QPushButton("Очистить поля")

        self.send_button.clicked.connect(self.send_data)
        self.list_button.clicked.connect(self.get_users)
        self.clear_button.clicked.connect(self.clear_fields)

        btn_layout.addWidget(self.send_button)
        btn_layout.addWidget(self.list_button)
        btn_layout.addWidget(self.clear_button)

        layout.addLayout(btn_layout)
        layout.addWidget(self.user_list)

        self.setLayout(layout)

    def send_data(self):
        name = self.name_input.text()
        email = self.email_input.text()
        if not name or not email:
            QMessageBox.warning(self, "Ошибка", "Заполните оба поля")
            return

        try:
            with socket.create_connection((HOST, PORT)) as sock:
                sock.sendall(f"{name};{email}".encode())
                response = sock.recv(1024).decode()
                QMessageBox.information(self, "Результат", response)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def get_users(self):
        try:
            with socket.create_connection((HOST, PORT)) as sock:
                sock.sendall("СПИСОК".encode())
                data = sock.recv(4096).decode()
                self.user_list.clear()
                users = data.split('|') if data else []
                self.user_list.addItems(users)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.user_list.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec())
