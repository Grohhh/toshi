from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox)
from gui.section_base import SectionBase
from models.building import Building


class BuildingSection(SectionBase):

    def __init__(self):
        super().__init__("🏢 Корпуса")
        self.selected_id = None
        self.init_content()
        self.load_data()

    def init_content(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Адрес', 'Этажей', 'Год', 'Активен'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input)

        form_layout.addWidget(QLabel("Адрес:"))
        self.address_input = QLineEdit()
        form_layout.addWidget(self.address_input)

        form_layout.addWidget(QLabel("Этажей:"))
        self.floors_input = QLineEdit()
        form_layout.addWidget(self.floors_input)

        form_layout.addWidget(QLabel("Год постройки:"))
        self.year_input = QLineEdit()
        form_layout.addWidget(self.year_input)

        layout.addLayout(form_layout)

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
        data = Building.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                if col_idx == 5:
                    text = "Да" if value else "Нет"
                else:
                    text = str(value) if value else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(text))

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.name_input.setText(self.table.item(row, 1).text() or "")
        self.address_input.setText(self.table.item(row, 2).text() or "")
        self.floors_input.setText(self.table.item(row, 3).text() or "")
        self.year_input.setText(self.table.item(row, 4).text() or "")

    def add_record(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название корпуса")
            return

        if Building.add(name, self.address_input.text() or None,
                       int(self.floors_input.text()) if self.floors_input.text() else 1,
                       int(self.year_input.text()) if self.year_input.text() else None):
            QMessageBox.information(self, "Успех", "Корпус добавлен")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить корпус")

    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите корпус")
            return

        if Building.update(self.selected_id, self.name_input.text(),
                          self.address_input.text() or None,
                          int(self.floors_input.text()) if self.floors_input.text() else 1,
                          int(self.year_input.text()) if self.year_input.text() else None):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")

    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите корпус")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Деактивировать корпус?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if Building.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Корпус деактивирован")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось деактивировать корпус")

    def clear_inputs(self):
        self.name_input.clear()
        self.address_input.clear()
        self.floors_input.clear()
        self.year_input.clear()
