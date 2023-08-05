import re
import sys
import traceback
from io import StringIO

import dxlib
import numpy
import pandas

from .handlers import GraphHandler, DataHandler, ProcessHandler


class Interpreter:
    command_regex = r"<([^>]+)>\(([^)]+)\)"

    def __init__(self):
        self.graph_handler = GraphHandler()
        self.data_handler = DataHandler()
        self.process_handler = ProcessHandler()
        self.handlers = [self.graph_handler, self.data_handler, self.process_handler]

        self.namespace = {
            'pandas': pandas,
            'numpy': numpy,
            'dxlib': dxlib,
            'HELP': self.show_help,
        }

        for handler in self.handlers:
            self.namespace.update(handler.reserved_commands)

        print("Initialized interpreter")

        self.graph_element = None

    @property
    def graph_element(self):
        return self.graph_handler.graph_element

    @graph_element.setter
    def graph_element(self, graph_element):
        self.graph_handler.graph_element = graph_element

    def show_help(self):
        help_message = f"Available commands: {self.get_descriptions()}"
        return help_message

    def run(self, code):
        try:
            output_buffer = StringIO()
            stdout = sys.stdout
            sys.stdout = output_buffer

            exec(code, self.namespace)
            sys.stdout = stdout

            output_buffer.seek(0)
            output = output_buffer.getvalue()

            return output
        except Exception as e:
            error_traceback = traceback.format_exc()
            return f"Error: {e}\n{error_traceback}"

    def get_descriptions(self):
        commands = []

        for handler in self.handlers:
            handler_commands = handler.get_descriptions()
            formatted_commands = {f"{command_name}": description for command_name, description in
                                  handler_commands.items()}

            commands.append(pandas.DataFrame(formatted_commands.items(), columns=["Command", "Description"]))

        return pandas.concat(commands)
