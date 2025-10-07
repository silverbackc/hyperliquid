import threading
import asyncio

from order_book.listener import collect_order_book
from order_book.bbo import collect_bbo
from candle.candle import collect_candles
from trades.trades import collect_trades
from funding.historical import get_historical_funding

# Polling duration
DURATION = 6


async def main():
    await get_historical_funding()
    candles_thread = threading.Thread(
        target=collect_candles, kwargs={"duration": DURATION}
    )
    order_book_thread = threading.Thread(
        target=collect_order_book, kwargs={"duration": DURATION}
    )
    trades_thread = threading.Thread(
        target=collect_trades, kwargs={"duration": DURATION}
    )
    bbo_thread = threading.Thread(target=collect_bbo, kwargs={"duration": DURATION})
    candles_thread.start()
    order_book_thread.start()
    trades_thread.start()
    bbo_thread.start()
    candles_thread.join()
    order_book_thread.join()
    trades_thread.join()
    bbo_thread.join()
    print("Done with data collection!")


if __name__ == "__main__":
    asyncio.run(main())
