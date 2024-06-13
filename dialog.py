from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QDialogButtonBox
from widgets import InputWidget, ComboBox, LineEdit, DateEdit


class AddDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Добавление конференции')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        self.init_fields(layout)
        self.init_buttons(layout)
        self.setLayout(layout)

    def init_fields(self, layout):
        self.organizer = InputWidget("Организатор", ComboBox(self.controller.get_organizers()))
        self.conferenceName = InputWidget("Название коференции", LineEdit())
        self.status = InputWidget("Статус", LineEdit())
        self.start_date = InputWidget("Дата начала", DateEdit())
        self.cooperator = InputWidget("Кооператор", LineEdit())
        layout.addWidget(self.organizer)
        layout.addWidget(self.conferenceName)
        layout.addWidget(self.status)
        layout.addWidget(self.start_date)
        layout.addWidget(self.cooperator)

    def init_buttons(self, layout):
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(self.buttons)
        buttonsLayout.addStretch(1)
        layout.addLayout(buttonsLayout)

        self.buttons.accepted.connect(self.get_data)
        self.buttons.rejected.connect(self.close)


    def get_data(self):
        self.accept()
        return {
            "organizer_id": self.organizer.data(),
            "conf_name": self.conferenceName.data(),
            "conf_status": self.status.data(),
            "conf_date": self.start_date.data(),
            "conf_organizer": self.cooperator.data()
        }

class EditDialog(AddDialog):
    def __init__(self, controller, parent=None):
        super().__init__(controller, parent)
