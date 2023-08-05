import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QKeyEvent
from PyQt6.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout

from .interpreter import Interpreter


class QTextEditStream:
    def __init__(self, text_edit, color):
        self.text_edit = text_edit
        self.color = color

    def write(self, text):
        self.text_edit.setTextColor(self.color)
        self.text_edit.insertPlainText(text)
        self.text_edit.setTextColor(QColor("black"))


class ConsoleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        with open('style/app.qss', 'r') as file:
            style = file.read()

        self.setStyleSheet(style)

        self.interpreter = Interpreter()
        self.command_history = []
        self.history_index = -1

        self.console_text_edit = QTextEdit(self)
        self.console_text_edit.setAcceptRichText(False)
        self.min_height = 75
        self.max_height = 150

        # noinspection PyUnresolvedReferences
        self.console_text_edit.document().documentLayout().documentSizeChanged.connect(self.update_text_edit_height)

        self.layout.addWidget(self.console_text_edit)
        self.console_text_edit.setStyleSheet("background-color: #000000; color: #ffffff; font-family: Consolas; "
                                             "font-size: 12px;")

        self.output_text_edit = QTextEdit(self)
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setMinimumHeight(300)
        self.output_text_edit.setStyleSheet("background-color: #000000; color: #ffffff; font-family: Consolas; "
                                            "font-size: 12px;")
        self.layout.addWidget(self.output_text_edit)

        self.console_text_edit.installEventFilter(self)

        self.run_button = QPushButton("Run", self)
        # noinspection PyUnresolvedReferences
        self.run_button.clicked.connect(self.run_console_code)
        self.layout.addWidget(self.run_button)

    def eventFilter(self, obj, event):
        if obj is self.console_text_edit and event.type() == QKeyEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
                if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                    self.console_text_edit.insertPlainText("\n")
                else:
                    self.run_console_code()
                return True
            elif event.key() == Qt.Key.Key_Up:
                self.handle_up_arrow_press()
                return True
        return super().eventFilter(obj, event)

    def handle_up_arrow_press(self):
        if self.command_history:
            if self.history_index == -1:
                self.history_index = len(self.command_history) - 1
            else:
                self.history_index = max(0, self.history_index - 1)
            self.set_console_input(self.command_history[self.history_index])

    def set_console_input(self, text):
        self.console_text_edit.setPlainText(text)

    def get_console_field(self):
        return self.console_text_edit

    def update_text_edit_height(self):
        doc_height = self.console_text_edit.document().size().height()
        self.console_text_edit.setMinimumHeight(min(max(int(doc_height), self.min_height), self.max_height))

    def run_console_code(self):
        code = self.console_text_edit.toPlainText()
        try:
            self.append_console_output(f">>> {code}\n", is_input=True, color=QColor("gray"))
            output = self.interpreter.run(code)

            self.append_console_output(f"\nOutput:\n{str(output)}", is_input=False, color=QColor("green"))

        except Exception as e:
            error_traceback = traceback.format_exc()
            self.append_console_output(f"Error: {e}\n{error_traceback}", is_input=False, color=QColor("red"))

        self.command_history.append(code)
        self.command_history = self.command_history[-10:]  # Keep only the last 10 commands
        self.history_index = -1  # Reset history index
        self.console_text_edit.clear()

    def append_console_output(self, output, is_input=False, color=QColor("black")):
        self.output_text_edit.setTextColor(color)
        self.output_text_edit.insertPlainText(output)
        self.output_text_edit.setTextColor(QColor("white"))
