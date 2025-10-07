from common import hl_setup
import time
from .order_book import order_book_callback


def collect_order_book(duration=60):
    print("collecting order book data")
    address, info, _ = hl_setup

    sub_id_l2book = info.subscribe(
        {"type": "l2Book", "coin": "BTC", "nSigFigs": 5}, order_book_callback
    )
    time.sleep(duration)
    info.unsubscribe({"type": "l2Book", "coin": "BTC", "nSigFigs": 5}, sub_id_l2book)


if __name__ == "__main__":
    collect_order_book(1)
