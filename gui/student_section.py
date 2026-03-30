from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDateEdit)
from PyQt5.QtCore import QDate
from gui.section_base import SectionBase
from models.student import Student


class StudentSection(SectionBase):

    def __init__(self):
        super().__init__("👨‍🎓 Студенты")
        self.selected_id = None
        self.init_content()
        self.load_data()

    def init_content(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'Код', 'Фамилия', 'Имя', 'Дата рождения', 'Группа', 'Курс', 'Факультет', 'Активен'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        form_layout1 = QHBoxLayout()
        form_layout1.addWidget(QLabel("Код студента:"))
        self.code_input = QLineEdit()
        form_layout1.addWidget(self.code_input)

        form_layout1.addWidget(QLabel("Фамилия:"))
        self.last_name_input = QLineEdit()
        form_layout1.addWidget(self.last_name_input)

        form_layout1.addWidget(QLabel("Имя:"))
        self.first_name_input = QLineEdit()
        form_layout1.addWidget(self.first_name_input)

        form_layout1.addWidget(QLabel("Дата рождения:"))
        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setDate(QDate(2005, 1, 1))
        self.birth_date.setDisplayFormat('yyyy-MM-dd')
        form_layout1.addWidget(self.birth_date)

        layout.addLayout(form_layout1)

        form_layout2 = QHBoxLayout()
        form_layout2.addWidget(QLabel("Группа:"))
        self.group_input = QLineEdit()
        form_layout2.addWidget(self.group_input)

        form_layout2.addWidget(QLabel("Курс:"))
        self.course_input = QLineEdit()
        form_layout2.addWidget(self.course_input)

        form_layout2.addWidget(QLabel("Факультет:"))
        self.faculty_input = QLineEdit()
        form_layout2.addWidget(self.faculty_input)

        layout.addLayout(form_layout2)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Изменить")
        self.update_btn.clicked.connect(self.edit_record)
        btn_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Деактивировать")
        self.delete_btn.clicked.connect(self.delete_record)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)

    def load_data(self):
        data = Student.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            # row_data: (student_id, student_code, last_name, first_name, middle_name, birth_date, gender, phone, email, group_name, course, faculty, is_active)
            # table cols: ID, Код, Фамилия, Имя, Дата рождения, Группа, Курс, Факультет, Активен
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0]) if row_data[0] else ""))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row_data[1]) if row_data[1] else ""))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data[2]) if row_data[2] else ""))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row_data[3]) if row_data[3] else ""))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row_data[5]) if row_data[5] else ""))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(row_data[9]) if row_data[9] else ""))
            self.table.setItem(row_idx, 6, QTableWidgetItem(str(row_data[10]) if row_data[10] else ""))
            self.table.setItem(row_idx, 7, QTableWidgetItem(str(row_data[11]) if row_data[11] else ""))
            self.table.setItem(row_idx, 8, QTableWidgetItem("Да" if row_data[12] else "Нет"))

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.code_input.setText(self.table.item(row, 1).text() or "")
        self.last_name_input.setText(self.table.item(row, 2).text() or "")
        self.first_name_input.setText(self.table.item(row, 3).text() or "")
        birth_date = self.table.item(row, 4).text() or ""
        if birth_date:
            self.birth_date.setDate(QDate.fromString(birth_date, 'yyyy-MM-dd'))
        self.group_input.setText(self.table.item(row, 5).text() or "")
        self.course_input.setText(self.table.item(row, 6).text() or "")
        self.faculty_input.setText(self.table.item(row, 7).text() or "")

    def add_record(self):
        if not self.code_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите код студента")
            return

        if Student.add(self.code_input.text(), self.last_name_input.text(),
                      self.first_name_input.text(), None,
                      self.birth_date.date().toString('yyyy-MM-dd'), 'м',
                      None, None, self.group_input.text(),
                      int(self.course_input.text()) if self.course_input.text() else None,
                      self.faculty_input.text()):
            QMessageBox.information(self, "Успех", "Студент добавлен")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить студента")

    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите студента")
            return

        if Student.update(self.selected_id, self.code_input.text(),
                         self.last_name_input.text(), self.first_name_input.text(),
                         None, self.birth_date.date().toString('yyyy-MM-dd'), 'м',
                         None, None,
                         self.group_input.text(),
                         int(self.course_input.text()) if self.course_input.text() else None,
                         self.faculty_input.text()):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")

    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите студента")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Деактивировать студента?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if Student.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Студент деактивирован")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось деактивировать студента")

    def clear_inputs(self):
        self.code_input.clear()
        self.last_name_input.clear()
        self.first_name_input.clear()
        self.group_input.clear()
        self.course_input.clear()
        self.faculty_input.clear()
