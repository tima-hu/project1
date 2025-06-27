import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt  

class ExerciseApp(QWidget):
    def __init__(self):  
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Приложение-упражнение")
        self.setFixedSize(400, 300)

        self.label = QLabel("Ожидаю действий...", self)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hello_btn = QPushButton("Привет")
        self.bye_btn = QPushButton("Пока")

        self.hello_btn.clicked.connect(self.say_hello)
        self.bye_btn.clicked.connect(self.say_bye)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.hello_btn)
        button_layout.addWidget(self.bye_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def say_hello(self):
        self.label.setText("Привет, пользователь!")

    def say_bye(self):
        self.label.setText("До свидания!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExerciseApp()
    window.show()
    sys.exit(app.exec())


# eveer
