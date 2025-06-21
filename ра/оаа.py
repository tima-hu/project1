from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton
)

class HobbyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мои хобби")
        self.setGeometry(100, 100, 300, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Выберите свои хобби:")

        self.hobby1 = QCheckBox("Чтение")
        self.hobby2 = QCheckBox("Спорт")
        self.hobby3 = QCheckBox("Программирование")
        self.hobby4 = QCheckBox("Путешествия")

        self.button = QPushButton("Показать выбранные хобби")
        self.button.clicked.connect(self.show_hobbies)

        self.result_label = QLabel("")

        # Добавляем все элементы в layout
        layout.addWidget(self.label)
        layout.addWidget(self.hobby1)
        layout.addWidget(self.hobby2)
        layout.addWidget(self.hobby3)
        layout.addWidget(self.hobby4)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)

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

# Запуск приложения
app = QApplication([])
window = HobbyWindow()
window.show()
app.exec()

