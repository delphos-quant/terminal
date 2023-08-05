from typing import Callable


def is_reserved(description: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        func.is_reserved = True
        func.description = description
        return func
    return decorator


class Handler:
    def __init__(self):
        self.reserved_commands: dict[str, callable] = {}
        self.reserved_commands_description: dict[str, str] = {}

        self._register_reserved_commands()

    def _register_command(self, command_name: str, command_callable: Callable):
        self.reserved_commands[command_name] = command_callable

    def _register_reserved_commands(self):
        for attr_name in dir(self):
            func = getattr(self, attr_name)
            if callable(func) and getattr(func, "is_reserved", False):
                formatted_name = f"{attr_name.upper()}"
                description = func.description if func.description else "No description"  # type: ignore

                self.reserved_commands[formatted_name] = func
                self.reserved_commands_description[formatted_name] = description

    def match_command(self, query):
        if query in self.reserved_commands:
            return self.reserved_commands[query]

    def get_descriptions(self):
        return self.reserved_commands_description


class GraphHandler(Handler):
    def __init__(self, graph_element=None):
        super().__init__()
        self.graph_element = graph_element

    @is_reserved(description="Sets the graph data to the local variable 'data'")
    def set_graph_data(self, data):
        graph = self.graph_element.create_graph(data)
        self.graph_element.set_graph(graph)

        return "Successfully set graph data"


class DataHandler(Handler):
    def __init__(self):
        super().__init__()
        self.api_key = None
        self.api_secret = None

    @is_reserved(description="Fetches currency exchange data from the AlphaVantage API, "
                             "and saves to the local variable 'data'")
    def fetch_currency_data(self, command):
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

    @is_reserved(description="Fetches stock data from the Alpaca Market API, and saves to the local variable 'data'")
    def fetch_stock_data(self, api_key, api_secret=None, symbol=None):
        from dxlib.api import AlpacaMarketsAPI as am
        if not self.api_key or not self.api_secret:
            self.api_key = api_key
            self.api_secret = api_secret
            symbol = symbol
        else:
            symbol = api_key

        alpaca_markets = am(self.api_key, self.api_secret)
        data = alpaca_markets.get_historical(symbol)

        data = [entry['p'] for entry in data['trades'][symbol]]

        return data


class ProcessHandler(Handler):
    @is_reserved(description="Calculates Exponential Moving Average (EMA) for the given local variable 'data'")
    def calculate_ema(self, command):
        # Parse the command to extract necessary parameters
        # For example, if the command is "<CALCULATE_EMA>data,period",
        # extract 'data' and 'period' from the command string.

        # Implement logic to calculate Exponential Moving Average (EMA) for the given data

        # Return the calculated EMA values as a custom string or pandas Series for display
        return "Custom string with calculated EMA"

