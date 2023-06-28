import os

from binance.spot import Spot
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient


class Client(Spot):
    """
    Customising Spot client
    """

    def __init__(self, key=None, secret=None, test_mode=True, **kwargs):
        if test_mode:
            kwargs["base_url"] = 'https://testnet.binance.vision'
        else:
            kwargs["base_url"] = self._server_choice()
            if key is None:
                key = os.getenv("BINANCE_API_KEY")
            if secret is None:
                secret = os.getenv("BINANCE_API_SECRET")

        super().__init__(key, secret, **kwargs)

    def _server_choice(self):
        """
        Server choice

        ! Implement later
        """
        return "https://api2.binance.com"

    def margin_account(self):
        """
        Clear margin_account report. Remove don't using assets
        """
        margin = super().margin_account()
        assets = [el for el in margin["userAssets"] if (el['free'] != '0' or \
                                                        el['locked'] != '0' or \
                                                        el['borrowed'] != '0' or \
                                                        el['interest'] != '0' or \
                                                        el['netAsset'] != '0')]
        margin["userAssets"] = assets

        return margin


class ClientWS(SpotWebsocketStreamClient):
    """
    Customising Spot client
    """
    def __init__(self, test_mode=True):
        if test_mode:
            stream_url = "wss://testnet.binance.vision"
        else:
            stream_url = "wss://stream.binance.com:9443"

        super().__init__(stream_url)


if __name__ == '__main__':
    from binanceTrade.autotrader.logger import logger
    from binance.lib.utils import config_logging

    from dotenv import load_dotenv

    load_dotenv()
    # load_dotenv('/home/jb/PycharmProjects/binanceTradeDj/binanceTrade/.env')

    client = Client(test_mode=False)
    logger.info(client.margin_all_pairs())
