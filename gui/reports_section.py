from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
                             QGridLayout, QFileDialog, QMessageBox)
from gui.section_base import SectionBase
from database.connection import get_connection
import csv


class ReportsSection(SectionBase):

    def __init__(self):
        super().__init__("📊 Отчеты")
        self.init_content()

    def init_content(self):
        layout = QVBoxLayout()

        group = QGroupBox("Формирование отчетов")
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Тип отчета:"), 0, 0)
        self.report_type = QComboBox()
        self.report_type.addItems([
            "Список проживающих по комнатам",
            "Наличие свободных мест",
            "Очередь на заселение",
            "Все договоры"
        ])
        self.report_type.currentIndexChanged.connect(self.update_params)
        form_layout.addWidget(self.report_type, 0, 1)

        form_layout.addWidget(QLabel("Корпус:"), 1, 0)
        self.building_combo = QComboBox()
        self.building_combo.addItem("Все корпуса", None)
        self.load_buildings()
        form_layout.addWidget(self.building_combo, 1, 1)

        btn_layout = QHBoxLayout()

        btn_generate = QPushButton("Сформировать")
        btn_generate.clicked.connect(self.generate_report)
        btn_layout.addWidget(btn_generate)

        btn_export = QPushButton("Экспорт в CSV")
        btn_export.clicked.connect(self.export_to_csv)
        btn_layout.addWidget(btn_export)

        form_layout.addLayout(btn_layout, 2, 0, 1, 2)
        group.setLayout(form_layout)
        layout.addWidget(group)

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.update_params()
        self.get_content_layout().addLayout(layout)

    def update_params(self):
        pass

    def load_buildings(self):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT building_id, name FROM buildings ORDER BY name")
            for row in cursor.fetchall():
                self.building_combo.addItem(row[1], row[0])
            cursor.close()
            conn.close()

    def generate_report(self):
        report_index = self.report_type.currentIndex()
        building_id = self.building_combo.currentData()

        conn = get_connection()
        if not conn:
            QMessageBox.critical(self, "Ошибка", "Нет подключения к БД")
            return

        try:
            cursor = conn.cursor()

            if report_index == 0:
                if building_id:
                    cursor.execute("""
                        SELECT s.student_code, s.last_name, s.first_name,
                               b.name, f.floor_number, r.room_number, res.bed_number
                        FROM residents res
                        JOIN students s ON res.student_id = s.student_id
                        JOIN rooms r ON res.room_id = r.room_id
                        JOIN floors f ON r.floor_id = f.floor_id
                        JOIN buildings b ON f.building_id = b.building_id
                        WHERE b.building_id = %s
                        ORDER BY b.name, f.floor_number, r.room_number
                    """, (building_id,))
                    headers = ['Код', 'Фамилия', 'Имя', 'Корпус', 'Этаж', 'Комната', 'Кровать']
                else:
                    cursor.execute("""
                        SELECT s.student_code, s.last_name, s.first_name,
                               b.name, f.floor_number, r.room_number, res.bed_number
                        FROM residents res
                        JOIN students s ON res.student_id = s.student_id
                        JOIN rooms r ON res.room_id = r.room_id
                        JOIN floors f ON r.floor_id = f.floor_id
                        JOIN buildings b ON f.building_id = b.building_id
                        ORDER BY b.name, f.floor_number, r.room_number
                    """)
                    headers = ['Код', 'Фамилия', 'Имя', 'Корпус', 'Этаж', 'Комната', 'Кровать']

            elif report_index == 1:
                cursor.execute("""
                    SELECT b.name, f.floor_number, r.room_number,
                           r.total_beds, r.occupied_beds,
                           (r.total_beds - r.occupied_beds) as available
                    FROM rooms r
                    JOIN floors f ON r.floor_id = f.floor_id
                    JOIN buildings b ON f.building_id = b.building_id
                    WHERE r.status = 'свободна' OR (r.total_beds - r.occupied_beds) > 0
                    ORDER BY b.name, f.floor_number, r.room_number
                """)
                headers = ['Корпус', 'Этаж', 'Комната', 'Всего', 'Занято', 'Свободно']

            elif report_index == 2:
                cursor.execute("""
                    SELECT s.student_code, s.last_name, s.first_name,
                           s.group_name, w.application_date, w.priority
                    FROM waiting_list w
                    JOIN students s ON w.student_id = s.student_id
                    WHERE w.status = 'в очереди'
                    ORDER BY w.priority, w.application_date
                """)
                headers = ['Код', 'Фамилия', 'Имя', 'Группа', 'Дата заявки', 'Приоритет']

            else:
                cursor.execute("""
                    SELECT c.contract_number, c.contract_date,
                           s.last_name || ' ' || s.first_name,
                           r.room_number, c.start_date, c.end_date, c.monthly_fee
                    FROM contracts c
                    JOIN students s ON c.student_id = s.student_id
                    JOIN rooms r ON c.room_id = r.room_id
                    ORDER BY c.contract_date DESC
                """)
                headers = ['Номер', 'Дата', 'Студент', 'Комната', 'Начало', 'Окончание', 'Плата']

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            self.result_table.setColumnCount(len(headers))
            self.result_table.setHorizontalHeaderLabels(headers)
            self.result_table.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx,
                                            QTableWidgetItem(str(value) if value else ""))

            QMessageBox.information(self, "Успех", f"Отчет сформирован ({len(rows)} записей)")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def export_to_csv(self):
        if self.result_table.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Сначала сформируйте отчет")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "CSV файлы (*.csv)")
        if not filename:
            return

        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')

                headers = [self.result_table.horizontalHeaderItem(i).text()
                          for i in range(self.result_table.columnCount())]
                writer.writerow(headers)

                for row in range(self.result_table.rowCount()):
                    row_data = [self.result_table.item(row, col).text()
                               for col in range(self.result_table.columnCount())]
                    writer.writerow(row_data)

            QMessageBox.information(self, "Успех", f"Отчет сохранен в {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
