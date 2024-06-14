from datetime import date

from PyQt6.QtCore import QDateTime, QDate
from PyQt6.QtWidgets import QDateEdit, QComboBox, QWidget, QVBoxLayout, QLabel, QLineEdit, QTableView, QHeaderView, \
    QMessageBox


class DateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat('dd.MM.yyyy')
        self.setDateTime(QDateTime.currentDateTime())

    def data(self):
        qtdate = self.date()
        return date.fromisoformat(qtdate.toString('yyyy-MM-dd'))

    def set(self, value):
        self.setDate(QDate.fromString(value.strftime("%Y-%m-%d"), "yyyy-MM-dd"))


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self):
        return self.text()

    def set(self, value):
        self.setText(value)


class ComboBox(QComboBox):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        for id, value in data:
            self.addItem(value, id)

    def data(self):
        return self.currentData()

    def set(self, value):
        self.setCurrentText(value)


class InputWidget(QWidget):
    def __init__(self, labelName, input, parent=None):
        super().__init__(parent)
        self.label = QLabel(labelName)
        self.input = input

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        self.setLayout(layout)


class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.verticalHeader().setVisible(False)
        self.setStyleSheet("""
            QTableView {
                background-color: #FFFFFF;
                color: #000000;
                gridline-color: #99CC99;
            }
            QHeaderView::section {
                background-color: #99CC99;
                padding: 4px;
                border: 1px solid #66CC66;
                font-size: 10pt;
            }
            QTableView::item {
                padding: 4px;
                border: 1px solid #66CC66;
            }
            QTableView::item:selected {
                background-color: #E6FFE6;
                color: #003300;
            }
        """)

    def confirm_deletion(self):
        reply = QMessageBox.question(
            self, 'Подтверждение удаления',
            'Вы уверены, что хотите удалить выделенные записи?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)

        return reply == QMessageBox.StandardButton.Yes
