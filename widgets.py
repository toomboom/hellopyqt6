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
        return self.date().toString('yyyy-MM-dd')

    def set(self, value):
        self.setDate(QDate.fromString(value.strftime("%d.%m.%Y"), "dd.MM.yyyy"))


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
        self.setStyleSheet("""
            QTableView {
                selection-background-color: #D3D3D3;
                selection-color: black;
            }
            QHeaderView::section {
                background-color: #F0F0F0;
                padding: 4px;
                border: 1px solid #D3D3D3;
                font-size: 10pt;
            }
            QTableView::item {
                padding: 4px;
                border: 1px solid #D3D3D3;
            }
        """)

    def confirm_deletion(self):
        reply = QMessageBox.question(
            self, 'Подтверждение удаления',
            'Вы уверены, что хотите удалить выделенные записи?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)

        return reply == QMessageBox.StandardButton.Yes
