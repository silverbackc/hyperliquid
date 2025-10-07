import time
from questdb.ingress import Sender, TimestampNanos

from common import hl_setup, QDB_CONF


def bbo_callback(*args, **kwargs):
    try:
        if len(args) > 0:
            bbo = args[0]["data"]
            ts = TimestampNanos.now()
            with Sender.from_conf(QDB_CONF) as sender:
                i = 0
                for rec in bbo["bbo"]:
                    sender.row(
                        "bbo",
                        symbols={
                            "symbol": "BTC-USD",
                            "side": "buy" if i == 0 else "sell",
                        },
                        columns=rec,
                        at=ts,
                    )
                    i += 1
                sender.flush()
        else:
            print("Subscription returned empty message")
    except Exception as e:
        print(e)


def collect_bbo(duration=60):
    """
    Collect BBO data for BTC perp
    """
    print("collecting bbo data")
    address, info, _ = hl_setup

    sub_id = info.subscribe({"type": "bbo", "coin": "BTC"}, bbo_callback)  # Order Book
    time.sleep(duration)
    info.unsubscribe({"type": "bbo", "coin": "BTC"}, sub_id)


if __name__ == "__main__":
    collect_bbo(1)
