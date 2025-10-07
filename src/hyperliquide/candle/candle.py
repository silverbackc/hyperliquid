from common import hl_setup, QDB_CONF
import time
from questdb.ingress import Sender, TimestampNanos



def candle_callback(*args):
    if len(args) > 0:
        try:
            with Sender.from_conf(QDB_CONF) as sender:
                sender.row(
                    "candles",
                    symbols={"symbol": "BTC-USD"},
                    columns=args[0]["data"],
                    at=TimestampNanos.now(),
                )
                sender.flush()
        except Exception as e:
            print(e)


def collect_candles(duration=60):
    """
    Collect BTC perp price candles
    """
    print("collecting candle data")
    address, info, _ = hl_setup

    sub_id = info.subscribe(
        {"type": "candle", "coin": "BTC", "interval": "1m"}, candle_callback
    )  # Order Book
    time.sleep(duration)
    info.unsubscribe({"type": "candle", "coin": "BTC", "interval": "1m"}, sub_id)


if __name__ == "__main__":
    collect_candles()
