from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import pyqtSignal

from gui.main_menu import MainMenu
from gui.building_section import BuildingSection
from gui.floor_section import FloorSection
from gui.room_section import RoomSection
from gui.student_section import StudentSection
from gui.resident_section import ResidentSection
from gui.contract_section import ContractSection
from gui.reports_section import ReportsSection
from gui.admin_section import AdminSection


class AppWindow(QMainWindow):

    logout_signal = pyqtSignal()

    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Заселение в студенческое общежитие")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #fafafa;")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_menu = MainMenu(self.current_user)
        self.main_menu.logout_signal.connect(self.logout)
        self.main_menu.open_section_signal.connect(self.open_section)
        self.stack.addWidget(self.main_menu)

        self.sections = {}

        self.show()

    def open_section(self, section_name):
        if section_name not in self.sections:
            if section_name == 'buildings':
                section = BuildingSection()
            elif section_name == 'floors':
                section = FloorSection()
            elif section_name == 'rooms':
                section = RoomSection()
            elif section_name == 'students':
                section = StudentSection()
            elif section_name == 'residents':
                section = ResidentSection()
            elif section_name == 'contracts':
                section = ContractSection()
            elif section_name == 'reports':
                section = ReportsSection()
            elif section_name == 'admin':
                section = AdminSection()
            else:
                return

            section.back_signal.connect(self.show_menu)
            self.sections[section_name] = section
            self.stack.addWidget(section)

        self.stack.setCurrentWidget(self.sections[section_name])

    def show_menu(self):
        self.stack.setCurrentWidget(self.main_menu)

    def logout(self):
        self.logout_signal.emit()
