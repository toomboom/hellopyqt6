from PyQt6.QtCore import QDateTime
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


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self):
        return self.text()

class ComboBox(QComboBox):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        for id, value in data:
            self.addItem(value, id)

    def data(self):
        return self.currentData()

class InputWidget(QWidget):
    def __init__(self, labelName, inputWidget, parent=None):
        super().__init__(parent)
        self.label = QLabel(labelName)
        self.inputWidget = inputWidget

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.inputWidget)

        self.setLayout(layout)

    def data(self):
        return self.inputWidget.data()


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

    def get_selected_rows(self):
        selected_indexes = self.selectionModel().selectedRows()
        return [index.row() for index in selected_indexes]
