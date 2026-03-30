from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QMessageBox, QFrame, QDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from gui.change_password_dialog import ChangePasswordDialog


class MainMenu(QWidget):

    logout_signal = pyqtSignal()
    open_section_signal = pyqtSignal(str)

    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Главное меню - {self.current_user['full_name']}")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Заселение в студенческое общежитие")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(title)

        user_info = QLabel(f"Пользователь: {self.current_user['full_name']} | Роль: {self.current_user['role']}")
        user_info.setAlignment(Qt.AlignCenter)
        user_info.setFont(QFont("Arial", 12))
        user_info.setStyleSheet("color: #666;")
        main_layout.addWidget(user_info)

        main_layout.addSpacing(20)

        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)

        if self.current_user['role'] == 'администратор':
            btn_buildings = self.create_menu_button("🏢 Корпуса", "Справочник корпусов общежития")
            btn_buildings.clicked.connect(lambda: self.open_section("buildings"))
            buttons_layout.addWidget(btn_buildings)

            btn_floors = self.create_menu_button("📶 Этажи", "Справочник этажей")
            btn_floors.clicked.connect(lambda: self.open_section("floors"))
            buttons_layout.addWidget(btn_floors)

            btn_rooms = self.create_menu_button("🚪 Комнаты", "Учет комнат и мест")
            btn_rooms.clicked.connect(lambda: self.open_section("rooms"))
            buttons_layout.addWidget(btn_rooms)

            btn_students = self.create_menu_button("👨‍🎓 Студенты", "База данных студентов")
            btn_students.clicked.connect(lambda: self.open_section("students"))
            buttons_layout.addWidget(btn_students)

            btn_residents = self.create_menu_button("📋 Проживающие", "Заселение и выселение")
            btn_residents.clicked.connect(lambda: self.open_section("residents"))
            buttons_layout.addWidget(btn_residents)

            btn_contracts = self.create_menu_button("📄 Договоры", "Договоры на проживание")
            btn_contracts.clicked.connect(lambda: self.open_section("contracts"))
            buttons_layout.addWidget(btn_contracts)

            btn_reports = self.create_menu_button("📊 Отчеты", "Формирование отчетов")
            btn_reports.clicked.connect(lambda: self.open_section("reports"))
            buttons_layout.addWidget(btn_reports)

            btn_admin = self.create_menu_button("⚙️ Администрирование", "Управление пользователями")
            btn_admin.clicked.connect(lambda: self.open_section("admin"))
            buttons_layout.addWidget(btn_admin)

        elif self.current_user['role'] == 'менеджер':
            btn_rooms = self.create_menu_button("🚪 Комнаты", "Учет комнат и мест")
            btn_rooms.clicked.connect(lambda: self.open_section("rooms"))
            buttons_layout.addWidget(btn_rooms)

            btn_students = self.create_menu_button("👨‍🎓 Студенты", "База данных студентов")
            btn_students.clicked.connect(lambda: self.open_section("students"))
            buttons_layout.addWidget(btn_students)

            btn_residents = self.create_menu_button("📋 Проживающие", "Заселение и выселение")
            btn_residents.clicked.connect(lambda: self.open_section("residents"))
            buttons_layout.addWidget(btn_residents)

            btn_contracts = self.create_menu_button("📄 Договоры", "Договоры на проживание")
            btn_contracts.clicked.connect(lambda: self.open_section("contracts"))
            buttons_layout.addWidget(btn_contracts)

            btn_reports = self.create_menu_button("📊 Отчеты", "Формирование отчетов")
            btn_reports.clicked.connect(lambda: self.open_section("reports"))
            buttons_layout.addWidget(btn_reports)

        elif self.current_user['role'] == 'комендант':
            btn_buildings = self.create_menu_button("🏢 Корпуса", "Справочник корпусов общежития")
            btn_buildings.clicked.connect(lambda: self.open_section("buildings"))
            buttons_layout.addWidget(btn_buildings)

            btn_floors = self.create_menu_button("📶 Этажи", "Справочник этажей")
            btn_floors.clicked.connect(lambda: self.open_section("floors"))
            buttons_layout.addWidget(btn_floors)

            btn_rooms = self.create_menu_button("🚪 Комнаты", "Учет комнат и мест")
            btn_rooms.clicked.connect(lambda: self.open_section("rooms"))
            buttons_layout.addWidget(btn_rooms)

            btn_residents = self.create_menu_button("📋 Проживающие", "Заселение и выселение")
            btn_residents.clicked.connect(lambda: self.open_section("residents"))
            buttons_layout.addWidget(btn_residents)

            btn_reports = self.create_menu_button("📊 Отчеты", "Формирование отчетов")
            btn_reports.clicked.connect(lambda: self.open_section("reports"))
            buttons_layout.addWidget(btn_reports)

        buttons_widget.setLayout(buttons_layout)
        main_layout.addWidget(buttons_widget)

        main_layout.addStretch()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        btn_password = QPushButton("🔑 Сменить пароль")
        btn_password.clicked.connect(self.change_password)
        main_layout.addWidget(btn_password)

        btn_logout = QPushButton("🚪 Выйти из системы")
        btn_logout.clicked.connect(self.logout)
        main_layout.addWidget(btn_logout)

        self.setLayout(main_layout)

    def create_menu_button(self, text, tooltip):
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def open_section(self, section_name):
        self.open_section_signal.emit(section_name)

    def logout(self):
        reply = QMessageBox.question(self, "Выход", "Выйти из системы?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logout_signal.emit()

    def change_password(self):
        dialog = ChangePasswordDialog(self, self.current_user)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Успех",
                "Пароль изменён!\nДля применения изменений необходимо войти в систему заново.")
            self.logout_signal.emit()
