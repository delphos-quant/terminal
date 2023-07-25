import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QGridLayout

from .console.console_widget import ConsoleWidget
from .console.search_widget import SearchWidget
from .dashboard.plotly_widget import PlotlyWidget


class TableDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("dxlib - Terminal")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        self.console_widget = ConsoleWidget(self)
        self.search_widget = SearchWidget(self,
                                          search_bar=self.console_widget.get_console_field(),
                                          data=self.console_widget.interpreter.get_reserved_commands())
        self.plotly_widget = PlotlyWidget(self)
        self.console_widget.interpreter.graph_element = self.plotly_widget

        self.layout.addWidget(self.console_widget, 0, 0)
        self.layout.addWidget(self.search_widget, 1, 0)
        self.layout.addWidget(self.plotly_widget, 0, 1)

        self.resize(1000, 700)

    def close_application(self):
        reply = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open('terminal/style/app.qss', 'r') as file:
        style = file.read()

    app.setStyleSheet(style)

    window = TableDisplay()
    window.show()
    sys.exit(app.exec())
