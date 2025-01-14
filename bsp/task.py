import asyncio
from bsp.functions import add_random_data_from_drone_to_db

async def periodic_task():
    while True:
        add_random_data_from_drone_to_db()
        await asyncio.sleep(30)
