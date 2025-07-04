import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)

DB_NAME = "people.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class PeopleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление людьми")
        self.setGeometry(100, 100, 400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Вводные поля
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")

        layout.addWidget(self.id_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)

        # Кнопки
        self.add_button = QPushButton("Добавить человека")
        self.add_button.clicked.connect(self.add_person)

        self.show_button = QPushButton("Показать всех")
        self.show_button.clicked.connect(self.show_people)

        self.delete_button = QPushButton("Удалить человека")
        self.delete_button.clicked.connect(self.delete_person)

        self.edit_button = QPushButton("Редактировать человека")
        self.edit_button.clicked.connect(self.edit_person)

        layout.addWidget(self.add_button)
        layout.addWidget(self.show_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)

        # Список
        self.people_list = QListWidget()
        layout.addWidget(self.people_list)

        self.setLayout(layout)

    def add_person(self):
        name = self.name_input.text().strip()
        age_text = self.age_input.text().strip()

        if not name or not age_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректные имя и возраст.")
            return

        age = int(age_text)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO people (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()

        self.clear_inputs()
        self.show_people()

    def show_people(self):
        self.people_list.clear()
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM people")
        people = cur.fetchall()
        conn.close()

        for person in people:
            id_, name, age = person
            self.people_list.addItem(f"{id_}: {name} ({age} лет)")

    def delete_person(self):
        id_text = self.id_input.text().strip()

        if not id_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректный ID.")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("DELETE FROM people WHERE id = ?", (int(id_text),))
        conn.commit()
        conn.close()

        self.clear_inputs()
        self.show_people()

    def edit_person(self):
        id_text = self.id_input.text().strip()
        name = self.name_input.text().strip()
        age_text = self.age_input.text().strip()

        if not id_text.isdigit() or not name or not age_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректные ID, имя и возраст.")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE people SET name = ?, age = ? WHERE id = ?", (name, int(age_text), int(id_text)))
        conn.commit()
        conn.close()

        self.clear_inputs()
        self.show_people()

    def clear_inputs(self):
        self.id_input.clear()
        self.name_input.clear()
        self.age_input.clear()
        self.people_list.clear()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PeopleApp()
    window.show()
    sys.exit(app.exec())