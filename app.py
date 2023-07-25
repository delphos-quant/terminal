import sys
import traceback

import pandas as pd
from PyQt6 import QtWidgets, QtWebEngineWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QPushButton, QTableWidgetItem, QMessageBox,
    QLineEdit, QHBoxLayout, QTextEdit
)
from plotly import express as px


class QTextEditStream:
    def __init__(self, text_edit, color):
        self.text_edit = text_edit
        self.color = color

    def write(self, text):
        self.text_edit.setTextColor(self.color)
        self.text_edit.insertPlainText(text)
        self.text_edit.setTextColor(QColor("black"))


# noinspection PyUnresolvedReferences
class TableWidget1(QTableWidget):
    def __init__(self):
        super().__init__()
        self.hide()
        self.itemChanged.connect(self.item_changed)
        self.data = None

    def display_table(self, data):
        self.data = data
        self.setRowCount(data.shape[0])
        self.setColumnCount(data.shape[1])

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = str(data.iloc[i, j])
                self.setItem(i, j, QTableWidgetItem(item))

        self.show()

    def item_changed(self, _):
        print("Table 1 Data:")
        for i in range(self.rowCount()):
            row_data = [self.item(i, j).text() for j in range(self.columnCount()) if self.item(i, j)]
            print(", ".join(row_data))


# noinspection PyUnresolvedReferences
class TableWidget2(QTableWidget):
    def __init__(self):
        super().__init__()
        self.hide()
        self.itemChanged.connect(self.item_changed)
        self.data = None

    def display_table(self, data):
        self.data = data
        self.setRowCount(data.shape[0])
        self.setColumnCount(data.shape[1])

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = str(data.iloc[i, j])
                self.setItem(i, j, QTableWidgetItem(item))

        self.show()

    def item_changed(self, _):
        if not self.data.empty:
            dxlib.data.append_to_csv(self.data)

        print("Table 2 Data:")
        for i in range(self.rowCount()):
            row_data = [self.item(i, j).text() for j in range(self.columnCount()) if self.item(i, j)]
            print(", ".join(row_data))


class TableDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("dxlib - Terminal")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.namespace = {}

        data_dict = {
            "Name": ["AAPL", "GOOGL", "PETR4.SA", "ABEV3.SAO", "ITUB4.SAO", "VIX.US", "VIXX.US", "NYSE: GOLD"],
            "Details": ["load", "load", "load", "load", "load", "load", "load", "load"]
        }

        self.data = pd.DataFrame(data_dict)
        self.top_results = []

        self.data_window = QWidget(self)

        self.search_bar = QLineEdit(self)
        self.search_bar.textChanged.connect(self.update_results)
        self.layout.addWidget(self.search_bar)

        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Name", "Details"])
        self.layout.addWidget(self.result_table)

        self.console_layout = QHBoxLayout()
        self.layout.addLayout(self.console_layout)

        self.console_input = QLineEdit(self)
        self.console_layout.addWidget(self.console_input)

        self.console_input.returnPressed.connect(self.run_console_code)

        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_console_code)
        self.console_layout.addWidget(self.run_button)

        self.console_text_edit = QTextEdit(self)
        self.layout.addWidget(self.console_text_edit)

        self.button1 = QPushButton("Show Table 1")
        self.button2 = QPushButton("Show Table 2")

        # noinspection PyUnresolvedReferences
        self.button1.clicked.connect(self.show_table1)
        # noinspection PyUnresolvedReferences
        self.button2.clicked.connect(self.show_table2)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)

        self.table1_data = pd.DataFrame()
        self.table2_data = pd.DataFrame()

        self.table_widget1 = TableWidget1()
        self.table_widget2 = TableWidget2()

        self.layout.addWidget(self.table_widget1)
        self.layout.addWidget(self.table_widget2)

        self.plotly_button = QPushButton("Show Plotly Graph")
        # noinspection PyUnresolvedReferences
        self.plotly_button.clicked.connect(self.show_plotly_graph)
        self.layout.addWidget(self.plotly_button)
        self.plot = Widget(self)
        self.plot.hide()

        self.close_button = QPushButton("Close Application")
        # noinspection PyUnresolvedReferences
        self.close_button.clicked.connect(self.close_application)
        self.layout.addWidget(self.close_button)

    def show_plotly_graph(self):
        self.plot.show()
        self.table_widget1.hide()
        self.table_widget2.hide()

    def show_table1(self):
        data = {
            "Column A": [1, 2, 3],
            "Column B": [4, 5, 6],
        }
        self.table1_data = pd.DataFrame(data)

        self.table_widget1.display_table(self.table1_data)

        self.table_widget2.hide()
        self.plot.hide()

    def show_table2(self):
        data = {
            "Column X": ["A", "B", "C"],
            "Column Y": ["D", "E", "F"],
        }
        self.table2_data = pd.DataFrame(data)

        self.table_widget2.display_table(self.table2_data)

        self.table_widget1.hide()
        self.plot.hide()

    def update_results(self, text):
        search_text = text.lower()
        filtered_data = self.data[self.data["Name"].str.lower().str.startswith(search_text)]
        self.top_results = filtered_data.head(5)

        self.result_table.setRowCount(0)

        for index, row in self.top_results.iterrows():
            self.result_table.insertRow(self.result_table.rowCount())
            self.result_table.setItem(self.result_table.rowCount() - 1, 0, QTableWidgetItem(row["Name"]))
            self.result_table.setItem(self.result_table.rowCount() - 1, 1, QTableWidgetItem(row["Details"]))

    def run_console_code(self):
        code = self.console_input.text()
        try:
            self.append_console_output(f">>> {code}\n", is_input=True, color=QColor("gray"))

            from io import StringIO
            output_buffer = StringIO()

            stdout = sys.stdout
            sys.stdout = output_buffer
            exec(code, self.namespace)
            sys.stdout = stdout

            output_buffer.seek(0)
            output = output_buffer.getvalue()

            if output:
                self.append_console_output(f"\nOutput:\n", is_input=False, color=QColor("green"))
                self.console_text_edit.insertPlainText(output)

        except Exception as e:
            error_traceback = traceback.format_exc()
            self.append_console_output(f"Error: {e}\n{error_traceback}", is_input=False, color=QColor("red"))

    def append_console_output(self, output, is_input=False, color=QColor("black")):
        self.console_input.clear()
        self.console_input.setFocus()
        self.console_input.setPlaceholderText("Enter Python code here...")
        self.console_input.setToolTip("Press 'Run' button or hit Enter to execute.")

        self.console_text_edit.setTextColor(color)
        self.console_text_edit.insertPlainText(output)
        self.console_text_edit.setTextColor(QColor("white"))

    def close_application(self):
        reply = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button)
        vlayout.addWidget(self.browser)

        # noinspection PyUnresolvedReferences
        self.button.clicked.connect(self.show_graph)
        self.resize(1000, 800)

    def show_graph(self):
        df = px.data.tips()
        fig = px.box(df, x="day", y="total_bill", color="smoker")
        fig.update_traces(quartilemethod="exclusive")  # or "inclusive", or "linear" by default
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    style = """
        QWidget {
            background-color: #181818;
            color: white;
            font-size: 14px;
            font-family: Arial;
        }

        QLineEdit {
            background-color: #2c2c2c;
            color: white;
            border: 1px solid #303030;
            border-radius: 10px;
            padding: 5px;
        }

        QLineEdit:focus {
            background-color: #4d4d4d;
        }

        QTableWidget {
            background-color: #2c2c2c;
            color: white;
            border: 1px solid #303030;
            border-radius: 10px;
            padding: 5px;
        }

        QTableWidget::item {
            padding: 5px;
        }

        QTextEdit {
            background-color: #2c2c2c;
            color: white;
            border: 1px solid #303030;
            border-radius: 10px;
            padding: 5px;
        }

        QPushButton {
            background-color: #00CED1;
            color: black;
            border: 1px solid #00CED1;
            border-radius: 10px;
            padding: 5px;
        }
        """

    app.setStyleSheet(style)

    window = TableDisplay()
    window.show()
    sys.exit(app.exec())
