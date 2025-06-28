import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
)

DB_NAME = "crud.db"

class CrudApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD приложение: Поиск и удаление пользователей")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()
        self.init_db()

    def setup_ui(self):
        layout = QVBoxLayout()

        search_label = QLabel("🔍 Поиск пользователей по имени:")
        layout.addWidget(search_label)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите имя или его часть")
        search_btn = QPushButton("Искать")
        search_btn.clicked.connect(self.search_user)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        delete_label = QLabel("🗑 Удаление пользователя по ID:")
        layout.addWidget(delete_label)

        delete_layout = QHBoxLayout()
        self.delete_input = QLineEdit()
        self.delete_input.setPlaceholderText("Введите ID пользователя")
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.delete_user)

        delete_layout.addWidget(self.delete_input)
        delete_layout.addWidget(delete_btn)
        layout.addLayout(delete_layout)

        self.setLayout(layout)

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """)
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        if count == 0:
            users = [
                ("Emily", "ramdilu@icloud.com"),
                ("Artur", "moloiikin@gmail.com"),
                ("Alex", "alexmukh@yandex.by")
            ]
            cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)
            conn.commit()

        conn.close()

    def search_user(self):
        name = self.search_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка ввода", "Введите имя для поиска.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email FROM users WHERE name LIKE ?",
            (f"%{name}%",)
        )
        rows = cursor.fetchall()
        conn.close()

        if rows:
            output = ""
            for row in rows:
                output += f"ID: {row[0]}, Имя: {row[1]}, Email: {row[2]}\n"
            self.results_area.setText(output)
        else: 
            self.results_area.setText("Пользователь не найден ")

    def delete_user(self):
        user_id = self.delete_input.text().strip()

        if not user_id.isdigit():
            QMessageBox.warning(self,"Ощибка кода", "ID должно быть число")
            return
    
        reply = QMessageBox.question(
            self , "Подтверждение удаления",
            f"Вы точно хотите ужалить пользователя с ID {user_id}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id =?",(int(user_id)))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted > 0:
            QMessageBox.information(self, "Успех",f"Пользователь с таким ID {user_id} удален")
            self.results_area.clear()
        else:
            QMessageBox.warning(self, "ОШИБКА", "Пользователь с таким ID не найден ")

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = CrudApp()
    window.show()
    sys.exit(app.exec())