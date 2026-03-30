from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox)
from gui.section_base import SectionBase
from models.floor import Floor
from models.building import Building


class FloorSection(SectionBase):

    def __init__(self):
        super().__init__("📶 Этажи")
        self.selected_id = None
        self.init_content()
        self.load_data()

    def init_content(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Корпус', 'Этаж', 'Комнат', 'Действия'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Корпус:"))
        self.building_combo = QComboBox()
        self.load_buildings()
        form_layout.addWidget(self.building_combo)

        form_layout.addWidget(QLabel("Номер этажа:"))
        self.floor_num_input = QLineEdit()
        form_layout.addWidget(self.floor_num_input)

        form_layout.addWidget(QLabel("Кол-во комнат:"))
        self.rooms_input = QLineEdit()
        form_layout.addWidget(self.rooms_input)

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Изменить")
        self.update_btn.clicked.connect(self.edit_record)
        btn_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_record)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)
        self.get_content_layout().addLayout(layout)

    def load_buildings(self):
        self.building_combo.clear()
        for b in Building.get_all():
            self.building_combo.addItem(b[1], b[0])

    def load_data(self):
        data = Floor.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                text = str(value) if value else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(text))

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        building_name = self.table.item(row, 2).text()
        index = self.building_combo.findText(building_name)
        self.building_combo.setCurrentIndex(index if index >= 0 else 0)
        self.floor_num_input.setText(self.table.item(row, 3).text() or "")
        self.rooms_input.setText(self.table.item(row, 4).text() or "")

    def add_record(self):
        building_id = self.building_combo.currentData()
        if not self.floor_num_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите номер этажа")
            return

        if Floor.add(building_id, int(self.floor_num_input.text()),
                    int(self.rooms_input.text()) if self.rooms_input.text() else 0):
            QMessageBox.information(self, "Успех", "Этаж добавлен")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить этаж")

    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите этаж")
            return

        if Floor.update(self.selected_id, self.building_combo.currentData(),
                       int(self.floor_num_input.text()),
                       int(self.rooms_input.text()) if self.rooms_input.text() else 0):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")

    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите этаж")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Удалить этаж?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if Floor.delete(self.selected_id):
            QMessageBox.information(self, "Успех", "Этаж удален")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить этаж")

    def clear_inputs(self):
        self.floor_num_input.clear()
        self.rooms_input.clear()
