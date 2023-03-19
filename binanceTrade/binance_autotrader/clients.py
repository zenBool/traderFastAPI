import os

from binance.spot import Spot
from binance.websocket.spot.websocket_client import SpotWebsocketClient


class Client(Spot):
    """
    It's custom Spot client
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


class ClientWS(SpotWebsocketClient):
    def __init__(self, test_mode=True):
        if test_mode:
            stream_url = "wss://testnet.binance.vision"
        else:
            stream_url = "wss://stream.binance.com:9443"

        super().__init__(stream_url)


if __name__ == '__main__':
    import logging
    from binance.lib.utils import config_logging

    from dotenv import load_dotenv

    config_logging(logging, logging.DEBUG)
    load_dotenv()
    # load_dotenv('/home/jb/PycharmProjects/binanceTradeDj/binanceTrade/.env')

    client = Client(test_mode=False)
    logging.info(client.margin_all_pairs())
