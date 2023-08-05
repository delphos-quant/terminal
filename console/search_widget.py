from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout, QHeaderView, QTextEdit


class SearchWidget(QWidget):
    def __init__(self, parent, search_bar: QTextEdit = None, data=None, search_filter=None):
        super().__init__(parent=parent)
        self.data = data
        self.results = []

        self.layout = QVBoxLayout(self)

        if search_bar is None:
            self.search_bar = QTextEdit(self)
            self.layout.addWidget(self.search_bar)

        else:
            self.search_bar = search_bar

        if search_filter:
            self.search_filter = search_filter
        else:
            self.search_filter = lambda strings, query: [string.lower().startswith(query.lower()) for string in strings]

        # noinspection PyUnresolvedReferences
        self.search_bar.textChanged.connect(self.update_results)

        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(len(self.data.columns))
        self.results_table.setHorizontalHeaderLabels(list(self.data.columns))
        self.results_table.setMinimumHeight(250)

        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        vertical_header = self.results_table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.results_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.layout.addWidget(self.results_table)

    @classmethod
    def default_filter_function(cls, strings, query):
        return [string.lower().startswith(query.lower()) for string in strings]

    def update_results(self):
        if self.data is None:
            return

        query = self.search_bar.toPlainText()
        if query == "":
            self.results_table.setRowCount(0)
            return

        filtered_data = self.data[self.search_filter(self.data[self.data.columns[0]].values, query)]
        self.results = filtered_data.head(5)
        self.results_table.setRowCount(0)

        for index, row in self.results.iterrows():
            self.results_table.insertRow(self.results_table.rowCount())

            for idx, column in enumerate(self.data.columns):
                self.results_table.setItem(self.results_table.rowCount() - 1, idx, QTableWidgetItem(str(row[column])))
