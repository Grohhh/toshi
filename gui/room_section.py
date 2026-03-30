from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QComboBox)
from gui.section_base import SectionBase
from models.room import Room
from models.floor import Floor
from models.building import Building


class RoomSection(SectionBase):

    def __init__(self):
        super().__init__("🚪 Комнаты")
        self.selected_id = None
        self.init_content()
        self.load_data()

    def init_content(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'Комната', 'Мест', 'Занято', 'Тип', 'Статус', 'Площадь', 'Этаж', 'Корпус'])
        self.table.cellClicked.connect(self.select_row)
        layout.addWidget(self.table)

        form_layout1 = QHBoxLayout()

        form_layout1.addWidget(QLabel("Корпус:"))
        self.building_combo = QComboBox()
        self.load_buildings()
        self.building_combo.currentIndexChanged.connect(self.on_building_changed)
        form_layout1.addWidget(self.building_combo)

        form_layout1.addWidget(QLabel("Этаж:"))
        self.floor_combo = QComboBox()
        form_layout1.addWidget(self.floor_combo)

        form_layout1.addWidget(QLabel("Номер комнаты:"))
        self.room_num_input = QLineEdit()
        form_layout1.addWidget(self.room_num_input)

        layout.addLayout(form_layout1)

        form_layout2 = QHBoxLayout()

        form_layout2.addWidget(QLabel("Всего мест:"))
        self.beds_input = QLineEdit()
        form_layout2.addWidget(self.beds_input)

        form_layout2.addWidget(QLabel("Тип:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(['стандарт', 'комфорт', 'люкс'])
        form_layout2.addWidget(self.type_combo)

        form_layout2.addWidget(QLabel("Статус:"))
        self.status_combo = QComboBox()
        for status in Room.STATUSES:
            self.status_combo.addItem(status)
        form_layout2.addWidget(self.status_combo)

        form_layout2.addWidget(QLabel("Площадь:"))
        self.area_input = QLineEdit()
        form_layout2.addWidget(self.area_input)

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

    def load_buildings(self):
        self.building_combo.clear()
        for b in Building.get_all():
            self.building_combo.addItem(b[1], b[0])

    def on_building_changed(self):
        building_id = self.building_combo.currentData()
        self.floor_combo.clear()
        for f in Floor.get_all():
            if f[1] == building_id:
                self.floor_combo.addItem(f"Этаж {f[3]}", f[0])

    def load_data(self):
        data = Room.get_all()
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                text = str(value) if value else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(text))

    def select_row(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.room_num_input.setText(self.table.item(row, 1).text() or "")
        self.beds_input.setText(self.table.item(row, 2).text() or "")
        self.type_combo.setCurrentText(self.table.item(row, 4).text() or "стандарт")
        self.status_combo.setCurrentText(self.table.item(row, 5).text() or "свободна")
        self.area_input.setText(self.table.item(row, 6).text() or "")
        
        # Сохраняем floor_id из данных
        building_name = self.table.item(row, 8).text() if self.table.item(row, 8) else ""
        floor_number = self.table.item(row, 7).text() if self.table.item(row, 7) else ""
        
        # Находим нужный корпус
        building_index = self.building_combo.findText(building_name)
        if building_index >= 0:
            self.building_combo.setCurrentIndex(building_index)
            self.on_building_changed()
            
            # Находим нужный этаж
            floor_text = f"Этаж {floor_number}"
            floor_index = self.floor_combo.findText(floor_text)
            if floor_index >= 0:
                self.floor_combo.setCurrentIndex(floor_index)

    def add_record(self):
        floor_id = self.floor_combo.currentData()
        if not floor_id:
            QMessageBox.warning(self, "Ошибка", "Выберите этаж")
            return

        if not self.room_num_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите номер комнаты")
            return

        if Room.add(floor_id, self.room_num_input.text(),
                   int(self.beds_input.text()) if self.beds_input.text() else 1,
                   self.type_combo.currentText(),
                   self.status_combo.currentText(),
                   float(self.area_input.text()) if self.area_input.text() else None):
            QMessageBox.information(self, "Успех", "Комната добавлена")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить комнату")

    def edit_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите комнату")
            return

        if Room.update(self.selected_id, self.floor_combo.currentData(),
                      self.room_num_input.text(),
                      int(self.beds_input.text()) if self.beds_input.text() else 1,
                      self.type_combo.currentText(),
                      self.status_combo.currentText(),
                      float(self.area_input.text()) if self.area_input.text() else None):
            QMessageBox.information(self, "Успех", "Данные обновлены")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить данные")

    def delete_record(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите комнату")
            return

        reply = QMessageBox.question(self, "Подтверждение", "Деактивировать комнату?\n\nВнимание: Если есть активные договоры, комната будет помечена как 'в ремонте' вместо удаления.", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        # Пробуем изменить статус на "в ремонте" вместо удаления
        if Room.change_status(self.selected_id, 'в ремонте'):
            QMessageBox.information(self, "Успех", "Комната переведена в статус 'в ремонте'")
            self.clear_inputs()
            self.selected_id = None
            self.load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось изменить статус комнаты")

    def clear_inputs(self):
        self.room_num_input.clear()
        self.beds_input.clear()
        self.area_input.clear()
