from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget


class TableWidget(QTableWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent=parent)
        self.hide()
        # noinspection PyUnresolvedReferences
        self.itemChanged.connect(self.item_changed)
        self.data = data

    def display_table(self):
        self.setRowCount(self.data.shape[0])
        self.setColumnCount(self.data.shape[1])

        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                item = str(self.data.iloc[i, j])
                self.setItem(i, j, QTableWidgetItem(item))

        self.show()

    def item_changed(self, _):
        print("Table Data Changed:")
        for i in range(self.rowCount()):
            row_data = [self.item(i, j).text() for j in range(self.columnCount()) if self.item(i, j)]
            print(", ".join(row_data))


class TableManagerWidget(QWidget):
    def __init__(self, parent, tables=None):
        super().__init__(parent=parent)

        if tables is None:
            tables = []
        self.tables = tables

    def show_table(self, table_idx) -> None:
        for idx, table in self.tables:
            if idx == table_idx:
                table.show()
            else:
                table.hide()
