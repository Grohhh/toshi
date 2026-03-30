from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QDateEdit)
from PyQt5.QtCore import QDate
from gui.section_base import SectionBase
from models.resident import Resident
from models.student import Student
from models.room import Room
from models.floor import Floor
from models.building import Building


class ResidentSection(SectionBase):

    def __init__(self):
        super().__init__("📋 Проживающие")
        self.selected_id = None
        self.init_content()
        self.load_data()

    def init_content(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', 'Код', 'ФИО', 'Комната', 'Кровать', 'Дата заселения', 'Договор', 'Статус'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        form_layout1 = QHBoxLayout()

        form_layout1.addWidget(QLabel("Студент:"))
        self.student_combo = QComboBox()
        self.load_students()
        form_layout1.addWidget(self.student_combo)

        form_layout1.addWidget(QLabel("Комната:"))
        self.room_combo = QComboBox()
        self.load_rooms()
        form_layout1.addWidget(self.room_combo)

        form_layout1.addWidget(QLabel("Кровать:"))
        self.bed_input = QLineEdit()
        form_layout1.addWidget(self.bed_input)

        layout.addLayout(form_layout1)

        form_layout2 = QHBoxLayout()

        form_layout2.addWidget(QLabel("Дата заселения:"))
        self.checkin_date = QDateEdit()
        self.checkin_date.setCalendarPopup(True)
        self.checkin_date.setDate(QDate.currentDate())
        self.checkin_date.setDisplayFormat('yyyy-MM-dd')
        form_layout2.addWidget(self.checkin_date)

        form_layout2.addWidget(QLabel("Номер договора:"))
        self.contract_input = QLineEdit()
        form_layout2.addWidget(self.contract_input)

        layout.addLayout(form_layout2)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Заселить")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)

        self.checkout_btn = QPushButton("Выселить")
        self.checkout_btn.clicked.connect(self.checkout_record)
        btn_layout.addWidget(self.checkout_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_record)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)

    def load_students(self):
        self.student_combo.clear()
        for s in Student.get_all():
            self.student_combo.addItem(f"{s[2]} {s[3]} ({s[1]})", s[0])

    def load_rooms(self):
        self.room_combo.clear()
        for r in Room.get_all():
            self.room_combo.addItem(f"{r[8]}, эт.{r[7]}, комн.{r[1]}", r[0])

    def load_data(self):
        data = Resident.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                text = str(value) if value else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(text))

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()

    def add_record(self):
        student_id = self.student_combo.currentData()
        room_id = self.room_combo.currentData()

        if not student_id or not room_id:
            QMessageBox.warning(self, "Ошибка", "Выберите студента и комнату")
            return

        if not self.bed_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите номер кровати")
            return

        if Resident.add(student_id, room_id, int(self.bed_input.text()),
                       self.checkin_date.date().toString('yyyy-MM-dd'),
                       self.contract_input.text() or None,
                       self.checkin_date.date().toString('yyyy-MM-dd')):
            QMessageBox.information(self, "Успех", "Студент заселен")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось заселить студента")

    def checkout_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите проживающего")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Выселить студента?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if Resident.checkout(self.selected_id):
            QMessageBox.information(self, "Успех", "Студент выселен")
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось выселить студента")

    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите проживающего")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Удалить запись?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if Resident.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Запись удалена")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить запись")

    def clear_inputs(self):
        self.bed_input.clear()
        self.contract_input.clear()
