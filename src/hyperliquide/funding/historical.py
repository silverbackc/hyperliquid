import requests as req
import asyncio
from questdb.ingress import Sender, TimestampNanos
from common.database import query_questdb
from common import QDB_CONF


async def get_historical_funding():
    url = "https://api.hyperliquid.xyz/info"
    try:
        start_time = await query_questdb()
    except Exception as e:
        print(e)
        start_time = 1756861200000
    res = req.post(
        url, json={"type": "fundingHistory", "coin": "BTC", "startTime": start_time + 1}
    )
    with Sender.from_conf(QDB_CONF) as sender:
        for funding_data in res.json():
            sender.row(
                "funding_history",
                symbols={"symbol": "BTC"},
                columns=funding_data,
                at=TimestampNanos(funding_data["time"] * 1000000),
            )
        sender.flush()


def get_predicted_funding():
    url = "https://api.hyperliquid.xyz/info"
    res = req.post(url, json={"type": "predictedFundings"})
    with Sender.from_conf(QDB_CONF) as sender:
        for funding_data in res.json():
            coin = funding_data[0]
            for exchange in funding_data[1]:
                if exchange[0] == "HlPerp":
                    sender.row(
                        "predicted_funding",
                        symbols={"symbol": coin},
                        columns=exchange[1],
                        at=TimestampNanos.now(),
                    )
        sender.flush()


if __name__ == "__main__":
    asyncio.run(get_historical_funding())
