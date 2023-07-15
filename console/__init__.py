import time
import logging

from rich.console import Console
from rich.logging import RichHandler

from dxlib.api import AlphaVantageAPI
from dxlib.data import append_to_csv


class CustomLogger:
    def _init_(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(RichHandler(show_time=True))
        self.logger = logger

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_exception(self, message):
        self.logger.exception(message)


class EmbededConsole(Console):
    def _init_(self):
        self.console = Console()

    def print(self, *objects, **kwargs):
        super().print(*objects, **kwargs)

    def input(self, prompt="", **kwargs):
        return super().input(prompt=prompt, **kwargs)

    def clear(self, home=True):
        super().clear()

def main():
    logger = CustomLogger()
    console = EmbededConsole()
    api_key = ''
    api = AlphaVantageAPI(api_key)

    try:
        for i in range(5):
            currencies_to_query = ['JPY', 'EUR', 'GBP', 'CAD', 'AUD']
            exchange_rates_df = api.fetch_currency_exchange_rates(currencies_to_query)
            append_to_csv(exchange_rates_df, 'currency_exchange_rates.csv')
            EmbededConsole.print(exchange_rates_df)
            time.sleep(60)
        logger.log_info(f"Fetched data for symbol")

    except Exception as e:
        logger.log_exception(f"Error fetching data: {str(e)}")
