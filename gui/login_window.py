from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QDialog, QFormLayout,
                             QComboBox, QDialogButtonBox)
from PyQt5.QtCore import Qt
from models.user import User
from gui.main_window import AppWindow


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация - Заселение в общежитие")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Заселение в студенческое общежитие")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        layout.addSpacing(20)

        layout.addWidget(QLabel("Логин:"))
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        layout.addWidget(self.login_input)

        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Регистрация")
        self.register_btn.clicked.connect(self.show_register)
        layout.addWidget(self.register_btn)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

    def handle_login(self):
        username = self.login_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.status_label.setText("Введите логин и пароль")
            return

        user = User.authenticate(username, password)

        if user:
            self.current_user = user
            self.open_main_window()
        else:
            self.status_label.setText("Неверный логин или пароль")

    def auto_login_admin(self):
        """Автовход для администратора по умолчанию"""
        user = User.authenticate('admin', 'admin123')
        if user:
            self.current_user = user
            self.open_main_window()
        else:
            self.status_label.setText("Ошибка входа. Проверьте БД.")

    def show_register(self):
        dialog = RegisterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.status_label.setText("Регистрация успешна! Теперь войдите.")
            self.status_label.setStyleSheet("color: green;")

    def open_main_window(self):
        self.app_window = AppWindow(self.current_user)
        self.app_window.show()
        self.app_window.logout_signal.connect(self.show_login)
        self.hide()

    def show_login(self):
        self.login_input.clear()
        self.password_input.clear()
        self.status_label.clear()
        self.show()


class RegisterDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация нового пользователя")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Придумайте логин")
        form.addRow("Логин:", self.username)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Придумайте пароль")
        form.addRow("Пароль:", self.password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        form.addRow("Подтверждение:", self.confirm_password)

        self.fullname = QLineEdit()
        self.fullname.setPlaceholderText("Иванов Иван Иванович")
        form.addRow("ФИО:", self.fullname)

        self.role_combo = QComboBox()
        self.role_combo.addItem("Администратор", "администратор")
        self.role_combo.addItem("Менеджер", "менеджер")
        self.role_combo.addItem("Комендант", "комендант")
        form.addRow("Роль:", self.role_combo)

        warning_label = QLabel("⚠️ Роль 'Администратор' дает полный доступ ко всем функциям системы!")
        warning_label.setStyleSheet("color: #f44336; font-size: 11px;")
        warning_label.setWordWrap(True)
        layout.addWidget(warning_label)

        layout.addLayout(form)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.register)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def register(self):
        username = self.username.text().strip()
        password = self.password.text()
        confirm = self.confirm_password.text()
        fullname = self.fullname.text().strip()
        role = self.role_combo.currentData()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        if password != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        if len(password) < 4:
            QMessageBox.warning(self, "Ошибка", "Пароль должен быть не менее 4 символов")
            return

        if not fullname:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО")
            return

        if User.add(username, password, role, fullname):
            QMessageBox.information(self, "Успех",
                f"Пользователь '{username}' зарегистрирован!\nТеперь войдите в систему.")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось зарегистрировать пользователя.\nВозможно, логин занят.")
