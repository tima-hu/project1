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
        self.setGeometry(100, 100, 500, 500)
        self.setup_ui()
        self.init_db()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Поиск по имени
        layout.addWidget(QLabel("🔍 Поиск пользователей по имени:"))
        name_search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите имя или его часть")
        search_btn = QPushButton("Искать")
        search_btn.clicked.connect(self.search_user)
        name_search_layout.addWidget(self.search_input)
        name_search_layout.addWidget(search_btn)
        layout.addLayout(name_search_layout)

        # Поиск по email
        layout.addWidget(QLabel("📧 Поиск пользователей по email:"))
        email_search_layout = QHBoxLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите email или его часть")
        email_search_btn = QPushButton("Искать по email")
        email_search_btn.clicked.connect(self.search_by_email)
        email_search_layout.addWidget(self.email_input)
        email_search_layout.addWidget(email_search_btn)
        layout.addLayout(email_search_layout)

        # Область вывода результатов
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        # Удаление по ID
        layout.addWidget(QLabel("🗑 Удаление пользователя по ID:"))
        delete_layout = QHBoxLayout()
        self.delete_input = QLineEdit()
        self.delete_input.setPlaceholderText("Введите ID пользователя")
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.delete_user)
        delete_layout.addWidget(self.delete_input)
        delete_layout.addWidget(delete_btn)
        layout.addLayout(delete_layout)

        # Удаление по имени
        layout.addWidget(QLabel("🗑 Удаление пользователя по имени:"))
        delete_name_layout = QHBoxLayout()
        self.delete_name_input = QLineEdit()
        self.delete_name_input.setPlaceholderText("Введите имя пользователя")
        delete_name_btn = QPushButton("Удалить по имени")
        delete_name_btn.clicked.connect(self.delete_by_name)
        delete_name_layout.addWidget(self.delete_name_input)
        delete_name_layout.addWidget(delete_name_btn)
        layout.addLayout(delete_name_layout)

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
        cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            output = "\n".join([f"ID: {r[0]}, Имя: {r[1]}, Email: {r[2]}" for r in rows])
            output += f"\n\nНайдено записей: {len(rows)}"
            self.results_area.setText(output)
        else:
            self.results_area.setText("Пользователи не найдены.")

    def search_by_email(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Ошибка ввода", "Введите email для поиска.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE email LIKE ?", (f"%{email}%",))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            output = "\n".join([f"ID: {r[0]}, Имя: {r[1]}, Email: {r[2]}" for r in rows])
            output += f"\n\nНайдено записей: {len(rows)}"
            self.results_area.setText(output)
        else:
            self.results_area.setText("Пользователи не найдены.")

    def delete_user(self):
        user_id = self.delete_input.text().strip()
        if not user_id.isdigit():
            QMessageBox.warning(self, "Ошибка ввода", "ID должен быть числом.")
            return

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Удалить пользователя с ID {user_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (int(user_id),))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted > 0:
            QMessageBox.information(self, "Успех", f"Пользователь с ID {user_id} удален.")
            self.results_area.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким ID не найден.")

    def delete_by_name(self):
        name = self.delete_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка ввода", "Введите имя для удаления.")
            return

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Удалить всех пользователей с именем '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE name = ?", (name,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted > 0:
            QMessageBox.information(self, "Успех", f"Удалено пользователей: {deleted}")
            self.results_area.clear()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователи с таким именем не найдены.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrudApp()
    window.show()
    sys.exit(app.exec())
