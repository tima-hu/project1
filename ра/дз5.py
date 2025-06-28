# Нужно сделать:

# Добавить функцию удаления по ID:

# Добавь новое поле для ввода ID.

# Добавь кнопку "Удалить человека".

# При нажатии на кнопку программа должна удалять человека с указанным ID из базы данных.

# Добавить функцию редактирования данных:

# Вводится ID, новое имя и новый возраст.

# Добавь кнопку "Редактировать человека".

# Обнови данные в таблице по ID.


# Структура итогового интерфейса:

# Поля: ID, Имя, Возраст

# Кнопки:

# Добавить человека

# Показать всех

# Удалить человека

# Редактировать человека


import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QTextEdit
)
from ра.database.databases import init_db, add_person, get_all_people, delete_person, edit_person

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD - Добавление и Получение")
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")

        self.add_button = QPushButton("Добавить человека")
        self.add_button.clicked.connect(self.handle_add)

        self.show_button = QPushButton("Показать всех")
        self.show_button.clicked.connect(self.handle_show)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")
        self.delete_button = QPushButton("Удалить человека")
        self.delete_button.clicked.connect(self.handle_delete)
        self.edit_button = QPushButton("Редактировать человека")
        self.edit_button.clicked.connect(self.handle_edit)


        layout.addWidget(QLabel("ID (для удаления или редактирования):"))
        layout.addWidget(self.id_input)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Возраст:"))
        layout.addWidget(self.age_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.show_button)
        layout.addWidget(self.output_area)
        

        self.setLayout(layout)

    def handle_add(self):
        name = self.name_input.text()
        age = self.age_input.text()

        if name and age.isdigit():
            add_person(name, int(age))
            self.name_input.clear()
            self.age_input.clear()
            self.output_area.setText("Человек добавлен!")
        else:
            self.output_area.setText("Ошибка: введите имя и возраст (число)")


    def handle_delete(self):                   
        person_id = self.id_input.text()
        if person_id.isdigit():
            delete_person(int(person_id))
            self.output_area.setText(f"Человек с ID {person_id} удалён.")
            self.id_input.clear()
        else:
            self.output_area.setText("Ошибка: введите корректный ID")

    def handle_edit(self):                     
        person_id = self.id_input.text()
        name = self.name_input.text()
        age = self.age_input.text()

        if person_id.isdigit() and name and age.isdigit():
            edit_person(int(person_id), name, int(age))
            self.output_area.setText(f"Человек с ID {person_id} обновлён.")
            self.id_input.clear()
            self.name_input.clear()
            self.age_input.clear()
        else:
            self.output_area.setText("Ошибка: введите ID, имя и возраст (число)")
    def handle_show(self):  
        people = get_all_people()
        result = ""
        for person in people:
            result += f"{person[0]}: {person[1]}, {person[2]} лет\n"
        self.output_area.setText(result)

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
