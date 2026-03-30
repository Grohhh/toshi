from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox, QDateEdit)
from PyQt5.QtCore import QDate
from gui.section_base import SectionBase
from models.contract import Contract
from models.student import Student
from models.room import Room


class ContractSection(SectionBase):

    def __init__(self):
        super().__init__("📄 Договоры")
        self.selected_id = None
        self.init_content()
        self.load_data()

    def init_content(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'Номер', 'Дата', 'Студент', 'Комната', 'Начало', 'Окончание', 'Плата', 'Статус'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        form_layout1 = QHBoxLayout()

        form_layout1.addWidget(QLabel("Номер договора:"))
        self.contract_num_input = QLineEdit()
        form_layout1.addWidget(self.contract_num_input)

        form_layout1.addWidget(QLabel("Студент:"))
        self.student_combo = QComboBox()
        self.load_students()
        form_layout1.addWidget(self.student_combo)

        form_layout1.addWidget(QLabel("Комната:"))
        self.room_combo = QComboBox()
        self.load_rooms()
        form_layout1.addWidget(self.room_combo)

        layout.addLayout(form_layout1)

        form_layout2 = QHBoxLayout()

        form_layout2.addWidget(QLabel("Дата начала:"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setDisplayFormat('yyyy-MM-dd')
        form_layout2.addWidget(self.start_date)

        form_layout2.addWidget(QLabel("Дата окончания:"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate().addYears(1))
        self.end_date.setDisplayFormat('yyyy-MM-dd')
        form_layout2.addWidget(self.end_date)

        form_layout2.addWidget(QLabel("Плата в месяц:"))
        self.fee_input = QLineEdit()
        form_layout2.addWidget(self.fee_input)

        layout.addLayout(form_layout2)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)

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
        data = Contract.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                text = str(value) if value else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(text))

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.contract_num_input.setText(self.table.item(row, 1).text() or "")

    def add_record(self):
        student_id = self.student_combo.currentData()
        room_id = self.room_combo.currentData()

        if not self.contract_num_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите номер договора")
            return

        if not student_id or not room_id:
            QMessageBox.warning(self, "Ошибка", "Выберите студента и комнату")
            return

        if Contract.add(self.contract_num_input.text(), student_id, room_id,
                       self.start_date.date().toString('yyyy-MM-dd'),
                       self.end_date.date().toString('yyyy-MM-dd'),
                       float(self.fee_input.text()) if self.fee_input.text() else 0):
            QMessageBox.information(self, "Успех", "Договор добавлен")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить договор")

    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите договор")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Удалить договор?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if Contract.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Договор удален")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить договор")

    def clear_inputs(self):
        self.contract_num_input.clear()
        self.fee_input.clear()
