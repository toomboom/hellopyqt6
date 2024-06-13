from view import View
from model import DatabaseModel
from tablemodel import ConferencesTableModel


class Controller:
    def __init__(self):
        self.model = DatabaseModel()
        self.view = View(self)
        self.table_model = ConferencesTableModel(self.model.get_conferences())
        self.view.set_table_model(self.table_model)
        self.view.show()

    def edit_conf(self):
        dialog = self.view.edit_dialog
        try:
            if not dialog.exec():
                return
            data = dialog.get_data()

            self.model.update_conference(
                data["conf_id"], data["organizer_id"], data["conf_name"],
                data["conf_status"], data["conf_date"], data["cooperator"]
            )
            self.table_model.update_row_by_id((
                data["conf_id"], data["organizer_name"], data["conf_name"],
                data["conf_status"], data["conf_date"], data["cooperator"]
            ))
        except Exception as e:
            self.view.show_error(str(e))

    def add_conf(self):
        try:
            dialog = self.view.add_dialog
            if not dialog.exec():
                return

            data = dialog.get_data()
            record_id = self.model.add_conference(
                organizer_id=data["organizer_id"],
                conf_name=data["conf_name"],
                conf_status=data["conf_status"],
                conf_date=data["conf_date"],
                conf_organizer=data["cooperator"]
            )
            self.table_model.appendRow((
                record_id, data["conf_name"], data["organizer_name"],
                data["conf_status"], data["conf_date"], data["cooperator"]
            ))
        except Exception as e:
            self.view.show_error(str(e))

    def delete_conf(self):
        try:
            selected_ids = [row[0] for row in self.get_selected_rows()]
            if (len(selected_ids) == 0) or (not self.view.table.confirm_deletion()):
                return

            self.model.delete_conferences_by_ids(selected_ids)
            self.table_model.delete_rows(selected_ids)
        except Exception as e:
            self.view.show_error(str(e))

    def get_organizers(self):
        return self.model.get_organizers()

    def get_selected_rows(self):
        table_view = self.view.table
        table_model = self.table_model
        return table_model.get_selected_rows(table_view.selectionModel())
