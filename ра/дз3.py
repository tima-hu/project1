import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QVBoxLayout, QPushButton, QComboBox, QSpinBox, QCheckBox,
    QRadioButton, QListWidget, QMessageBox
)

class ExerciseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Анкета пользователя")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.age_input = QSpinBox()
        self.email_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")
        self.email_input.setPlaceholderText("Введите email")

        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Возраст:"))
        layout.addWidget(self.age_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        
        layout.addWidget(QLabel("Пол:"))
        self.radio1 = QRadioButton("Мужской")
        self.radio2 = QRadioButton("Женский")
        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)

        
        layout.addWidget(QLabel("Хобби:"))
        self.hobby1 = QCheckBox("Чтение")
        self.hobby2 = QCheckBox("Спорт")
        self.hobby3 = QCheckBox("Программирование")
        self.hobby4 = QCheckBox("Путешествия")
        layout.addWidget(self.hobby1)
        layout.addWidget(self.hobby2)
        layout.addWidget(self.hobby3)
        layout.addWidget(self.hobby4)

        
        self.check = QCheckBox("Я согласен с условиями")
        layout.addWidget(self.check)

        
        self.result_label = QLabel("")
        self.button = QPushButton("Показать хобби")
        self.button.clicked.connect(self.show_hobbies)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)

        
        self.submit_btn = QPushButton("Сохранить")
        self.submit_btn.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def show_hobbies(self):
        selected = []
        if self.hobby1.isChecked():
            selected.append("Чтение")
        if self.hobby2.isChecked():
            selected.append("Спорт")
        if self.hobby3.isChecked():
            selected.append("Программирование")
        if self.hobby4.isChecked():
            selected.append("Путешествия")

        if selected:
            self.result_label.setText("Вы выбрали: " + ", ".join(selected))
        else:
            self.result_label.setText("Хобби не выбраны.")

    def submit_data(self):
        name = self.name_input.text()
        age = self.age_input.value()
        email = self.email_input.text()
        gender = "Мужской" if self.radio1.isChecked() else "Женский" if self.radio2.isChecked() else "Не выбран"
        hobbies = self.result_label.text()

        if not name or not self.check.isChecked():
            QMessageBox.warning(self, "Ошибка", "Введите имя и согласитесь с условиями!")
            return

        info = f"Имя: {name}\nВозраст: {age}\nEmail: {email}\nПол: {gender}\n{hobbies}"
        QMessageBox.information(self, "Данные отправлены", info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = ExerciseApp()
    demo.show()
    sys.exit(app.exec())
