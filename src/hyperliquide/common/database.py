import asyncio
import os
import time

import asyncpg

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 8812)
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "quest")
DB_NAME = os.getenv("DB_NAME", "qdb")

# Set the timezone to UTC
os.environ["TZ"] = "UTC"
if hasattr(time, "tzset"):
    # tzset is only available on Unix-like systems
    time.tzset()


async def connect_to_questdb():
    conn = await asyncpg.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )

    version = await conn.fetchval("SELECT version()")
    print(f"Connected to QuestDB version: {version}")

    await conn.close()


async def query_questdb():
    """
    Fetches maximum timestamp for existing funding data
    """
    conn = await asyncpg.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    max_timestamp = await conn.fetchval("SELECT max(time) FROM funding_history")
    print(f"max_timestamp: {max_timestamp}")

    await conn.close()
    return max_timestamp


if __name__ == "__main__":
    asyncio.run(query_questdb())
