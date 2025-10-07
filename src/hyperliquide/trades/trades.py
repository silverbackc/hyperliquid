from common import hl_setup, QDB_CONF
import time
from questdb.ingress import Sender, TimestampNanos


def trades_callback(*args):
    if len(args) > 0:
        try:
            with Sender.from_conf(QDB_CONF) as sender:
                trades_data = args[0]["data"]
                for trade in trades_data:
                    del trade["users"]
                    sender.row(
                        "trades",
                        symbols={"symbol": "BTC-USD"},
                        columns=trade,
                        at=TimestampNanos.now(),
                    )
                sender.flush()
        except Exception as e:
            print(e)


def collect_trades(duration=60):
    print("collecting trades data")
    address, info, _ = hl_setup

    sub_id = info.subscribe(
        {"type": "trades", "coin": "BTC"}, trades_callback
    )  # Order Book
    time.sleep(duration)
    info.unsubscribe({"type": "trades", "coin": "BTC"}, sub_id)


if __name__ == "__main__":
    collect_trades()
