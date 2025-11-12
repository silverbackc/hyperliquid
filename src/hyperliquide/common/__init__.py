import sys
import os

sys.path.append(os.path.dirname(__file__))

from setup import setup
from hyperliquid.utils import constants

QDB_CONF = "http::addr=localhost:9000;"

hl_setup = setup(base_url=constants.MAINNET_API_URL, skip_ws=False)
