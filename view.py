from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QPushButton
from dialog import AddDialog, EditDialog
from widgets import TableView


class View(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        self.add_dialog = AddDialog(self.controller)
        self.edit_dialog = EditDialog(self.controller)

    def init_ui(self):
        self.setWindowTitle('Конференции')
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(800, 400)
        layout = QVBoxLayout()

        self.init_table(layout)
        self.init_buttons(layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_table(self, layout):
        self.table = TableView()
        layout.addWidget(self.table)

    def init_buttons(self, layout):
        self.addButton = QPushButton('Добавить')
        self.editButton = QPushButton('Редактировать')
        self.deleteButton = QPushButton('Удалить')
        self.addButton.clicked.connect(self.controller.add_conf)
        self.editButton.clicked.connect(self.controller.edit_conf)
        self.deleteButton.clicked.connect(self.controller.delete_conf)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.addButton)
        buttonsLayout.addWidget(self.editButton)
        buttonsLayout.addWidget(self.deleteButton)
        layout.addLayout(buttonsLayout)

    def set_table_model(self, model):
        self.table.setModel(model)

    def show_error(self, message):
        QMessageBox.critical(self, 'Error', message)
