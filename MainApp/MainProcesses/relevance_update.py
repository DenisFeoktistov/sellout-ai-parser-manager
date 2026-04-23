import asyncio
import datetime
import aiohttp

from MainApp.MainProcesses.process_batches import process_spus
from logger import relevance_update_logger

from constants import DEWU_API_GET_NEW_PRODUCTS


async def wait_until_parse_api():
    relevance_update_logger.info("Waiting for parse time")

    now = datetime.datetime.now()
    target_time = datetime.datetime(now.year, now.month, now.day, 21, 20)

    if now > target_time:
        target_time += datetime.timedelta(days=1)

    delta_second = (target_time - now).total_seconds()
    await asyncio.sleep(delta_second)


async def main():
    while True:
        await wait_until_parse_api()

        relevance_update_logger.info("Initializing updating cycle")

        async with aiohttp.ClientSession(timeout=None) as session:
            async with session.get(DEWU_API_GET_NEW_PRODUCTS) as response:
                await response.json()

        await wait_until_parse_api()
        await wait_until_parse_api()


def start_relevance_update_cycle():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    relevance_update_logger.info("Starting new products update process")

    loop.run_until_complete(main())
