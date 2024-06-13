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
        self.conference_name = InputWidget("Название коференции", LineEdit())
        self.status = InputWidget("Статус", LineEdit())
        self.start_date = InputWidget("Дата начала", DateEdit())
        self.cooperator = InputWidget("Кооператор", LineEdit())
        layout.addWidget(self.organizer)
        layout.addWidget(self.conference_name)
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
            "organizer_id": self.organizer.input.currentData(),
            "organizer_name": self.organizer.input.currentText(),
            "conf_name": self.conference_name.input.data(),
            "conf_status": self.status.input.data(),
            "conf_date": self.start_date.input.data(),
            "cooperator": self.cooperator.input.data()
        }


class EditDialog(AddDialog):
    def __init__(self, controller, parent=None):
        super().__init__(controller, parent)
        self.conf_id = None

    def set_data(self, name, organizer, status, date, cooperator):
        self.conference_name.input.set(name)
        self.organizer.input.set(organizer)
        self.status.input.set(status)
        self.start_date.input.set(date)
        self.cooperator.input.set(cooperator)

    def get_data(self):
        data = super().get_data()
        data["conf_id"] = self.conf_id
        return data

    def exec(self):
        row = self.get_selected_row()
        if len(row) == 0:
            return False

        self.conf_id = row[0]
        self.set_data(
            name=row[1],
            organizer=row[2],
            status=row[3],
            date=row[4],
            cooperator=row[5]
        )

        return super().exec()

    def get_selected_row(self):
        selected_rows = self.controller.get_selected_rows()
        if len(selected_rows) == 0:
            return []
        if len(selected_rows) > 1:
            raise Exception("Нельзя редактировать несколько строк")

        return selected_rows[0]
