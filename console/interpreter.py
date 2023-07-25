import sys
import traceback
from io import StringIO

import dxlib
import numpy
import pandas


from .handlers import GraphHandler, DataHandler, ProcessHandler


class Interpreter:
    def __init__(self):
        self.namespace = {
            'pandas': pandas,
            'numpy': numpy,
            'dxlib': dxlib
        }

        self.graph_handler = GraphHandler()
        self.data_handler = DataHandler()
        self.process_handler = ProcessHandler()
        self.handlers = [self.graph_handler, self.data_handler, self.process_handler]

        self.reserved_commands = {}
        self._register_reserved_commands()
        print("Initialized interpreter")

        self.graph_element = None

    def execute_python_code(self, code):
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

    def run(self, command):
        query = command.replace(" ", ",").split(",")[0]

        match query:
            case "<SET_GRAPH_DATA>":
                return self.graph_handler.set_graph_data(command, self.graph_element, self.namespace.get("data"))
            case "<FETCH_STOCK_DATA>":
                output = self.data_handler.fetch_stock_data(command)
                self.namespace["data"] = output
                return output
            case "<CALCULATE_EMA>":
                return self.process_handler.calculate_ema(command)
            case _:
                return self.execute_python_code(command)

    def _register_reserved_commands(self):
        for handler in self.handlers:
            for attr_name in dir(handler):
                func = getattr(handler, attr_name)
                if callable(func) and getattr(func, "is_reserved", False):
                    formatted_name = f"<{attr_name.upper()}>"

                    description = func.description if func.description else "No description"  # type: ignore

                    self.reserved_commands[formatted_name] = description

    def get_reserved_commands(self):
        return pandas.DataFrame(self.reserved_commands.items(), columns=["Command", "Function"])
