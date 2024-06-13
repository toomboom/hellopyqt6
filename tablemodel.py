from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from datetime import date


class ConferencesTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._headers = ["ID Конференции", "Конференция", "Организатор", "Статус", "Дата начала", "Координатор"]
        self._data = data
        self.sort(0)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, float):
                return "%.2f" % value
            elif isinstance(value, date):
                return value.strftime("%d.%m.%Y")
            return value

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]

    def delete_rows(self, row_ids):
        row_ids_set = set(row_ids)
        for row_index in range(len(self._data) - 1, -1, -1):
            if self._data[row_index][0] in row_ids_set:
                self.beginRemoveRows(QModelIndex(), row_index, row_index)
                del self._data[row_index]
                self.endRemoveRows()

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def appendRow(self, data, parent=QModelIndex()):
        position = self.rowCount(parent)
        self.beginInsertRows(parent, position, position)
        self._data.append(data)
        self.endInsertRows()

    def sort(self, column, order=Qt.SortOrder.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=order == Qt.SortOrder.DescendingOrder)
        self.layoutChanged.emit()

    def get_selected_rows(self, selection_model):
        selected_indexes = selection_model.selectedRows()
        return [self._data[index.row()] for index in selected_indexes]


    # def update_row_by_id(self, record_id, new_values):
    #     row_index = next((index for (index, d) in enumerate(self._data) if d[0] == record_id), None)
    #     if row_index is not None:
    #         updated_row = new_values
    #         self._data[row_index] = updated_row
    #         self.dataChanged.emit(self.index(row_index, 0), self.index(row_index, len(new_values) - 1))

    # def update_row_by_id(self, record_id, values):
    #     row_to_update = next((index for index, row in enumerate(self._data) if row[0] == record_id), None)
    #     if row_to_update is not None:
    #         for col, value in enumerate(values):
    #             self._data[row_to_update][col] = value
    #
    #         self.dataChanged.emit(self.createIndex(row_to_update, 0), self.createIndex(row_to_update, len(values) - 1))
    #         return True
    #     return False

    def update_row_by_id(self, values):
        record_id = values[0]
        row_to_update = next((index for index, row in enumerate(self._data) if row[0] == record_id), None)
        if row_to_update is not None:
            self._data[row_to_update] = values
            self.dataChanged.emit(self.createIndex(row_to_update, 0), self.createIndex(row_to_update, len(values) - 1))
            return True
        return False
