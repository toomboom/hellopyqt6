from view import View
from model import DatabaseModel
from tablemodel import ConferencesTableModel
from dialog import AddDialog


class Controller:
    def __init__(self):
        self.model = DatabaseModel()
        self.view = View(self)
        self.table_model = ConferencesTableModel(self.model.get_conferences())
        self.view.set_table_model(self.table_model)
        self.view.show()

    def edit_conf(self):
        selected_ids = self.get_selected_ids()
        if len(selected_ids) > 1:
            self.view.show_error("Нельзя редактировать несколько строк")

    def add_conf(self):
        dialog = self.view.add_dialog
        if not dialog.exec():
            return

        data = dialog.get_data()
        try:
            record_id = self.model.add_conference(
                data["organizer_id"], data["conf_name"], data["conf_status"],
                data["conf_date"], data["conf_organizer"]
            )
            self.table_model.appendRow(self.model.find_conference(record_id)[0])
        except Exception as e:
            self.view.show_error(str(e))

    def delete_conf(self):
        if self.view.table.confirm_deletion():
            selected_ids = self.get_selected_ids()
            self.table_model.delete_rows(selected_ids)

    def get_organizers(self):
        return self.model.get_organizers()

    def get_selected_ids(self):
        selected_rows = self.view.table.get_selected_rows()
        return [self.table_model.index(row, 0).data() for row in selected_rows]
