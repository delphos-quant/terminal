from typing import Callable


def is_reserved(description: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        func.is_reserved = True
        func.description = description
        return func
    return decorator


class GraphHandler:
    @is_reserved(description="Sets the graph data to the local variable 'data'")
    def set_graph_data(self, command, graph_element, data):
        graph = graph_element.create_graph(data)
        graph_element.set_graph(graph)

        return "Successfully set graph data"


class DataHandler:
    def __init__(self):
        self.api_key = None

    @is_reserved(description="Fetches stock data from an API or database, and saves to the local variable 'data'")
    def fetch_stock_data(self, command):
        from dxlib.api import AlphaVantageAPI as av
        params = command.replace(", ", ",").split(",")[1:]
        if not self.api_key:
            self.api_key = params[0]
            symbols = params[1:]
        else:
            symbols = params

        alpha_vantage = av(self.api_key)
        data = alpha_vantage.fetch_currency_exchange_rates(symbols)

        return data


class ProcessHandler:
    @is_reserved(description="Calculates Exponential Moving Average (EMA) for the given local variable 'data'")
    def calculate_ema(self, command):
        # Parse the command to extract necessary parameters
        # For example, if the command is "<CALCULATE_EMA>data,period",
        # extract 'data' and 'period' from the command string.

        # Implement logic to calculate Exponential Moving Average (EMA) for the given data

        # Return the calculated EMA values as a custom string or pandas Series for display
        return "Custom string with calculated EMA"
