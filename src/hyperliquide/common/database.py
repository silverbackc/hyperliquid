import asyncio
import os
import time

import asyncpg

# Set the timezone to UTC
os.environ["TZ"] = "UTC"
if hasattr(time, "tzset"):
    # tzset is only available on Unix-like systems
    time.tzset()


async def connect_to_questdb():
    conn = await asyncpg.connect(
        host="127.0.0.1", port=8812, user="admin", password="quest", database="qdb"
    )

    version = await conn.fetchval("SELECT version()")
    print(f"Connected to QuestDB version: {version}")

    await conn.close()


async def query_questdb():
    """
    Fetches maximum timestamp for existing funding data
    """
    conn = await asyncpg.connect(
        host="127.0.0.1", port=8812, user="admin", password="quest", database="qdb"
    )
    max_timestamp = await conn.fetchval("SELECT max(time) FROM funding_history")
    print(f"max_timestamp: {max_timestamp}")

    await conn.close()
    return max_timestamp


if __name__ == "__main__":
    asyncio.run(query_questdb())
