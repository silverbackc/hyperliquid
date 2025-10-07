from pydantic import BaseModel, Field, field_validator
from typing import List, Union, Dict
from questdb.ingress import Sender, TimestampNanos

conf = f"http::addr=localhost:9000;"


class OrderBookLevel(BaseModel):
    price: str = Field(description="price", alias="px")
    size: str = Field(description="size", alias="sz")
    number_of_orders: int = Field(
        description="number of orders at this price level", alias="n"
    )


class OrderBook(BaseModel):
    coin: str = Field(description="coin symbol")
    time: int = Field(description="timestamp of the order book")
    levels: List[List[Dict]] = Field(description="order book levels")

    @field_validator("levels")
    @classmethod
    def _validate_levels(cls, v):
        levels = []
        for level in v:
            new_level = []
            for d in level:
                new_level.append(OrderBookLevel(**d))
            levels.append(new_level)
        return levels

    def print_order_book(self):
        print("Price | Size | Number of Orders")
        for level in self.levels:
            for order in level:
                print(f"{order.price} {order.size} {order.number_of_orders}")
            print("--------------------------------")


class Subscription(BaseModel):
    channel: str = Field(description="channel subscribed to")
    data: Union[OrderBook] = Field(description="data received from the channel")


def order_book_callback(*args, **kwargs):
    try:
        if len(args) > 0:
            order_book = Subscription(**args[0])
            # depth = 0
            ts = TimestampNanos.now()
            with Sender.from_conf(conf) as sender:
                i = 0
                for level in order_book.data.levels:
                    for rec in level:
                        sender.row(
                            "order_book",
                            symbols={
                                "symbol": "BTC-USD",
                                "side": "buy" if i == 0 else "sell",
                            },
                            columns=rec.dict(),
                            at=ts,
                        )
                    i += 1
                sender.flush()
        else:
            print("Subscription returned empty message")
    except Exception as e:
        print(e)
