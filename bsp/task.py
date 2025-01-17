import asyncio
from bsp.functions import generate_random_data_for_multiple_drones

async def periodic_task():
    while True:
        generate_random_data_for_multiple_drones()
        await asyncio.sleep(30)
