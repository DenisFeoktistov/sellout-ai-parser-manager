import asyncio
import datetime
import aiohttp

from MainApp.MainProcesses.process_batches import process_spus
from logger import relevance_update_logger

from constants import DEWU_API_GET_NEW_PRODUCTS


async def wait_until_parse_api():
    relevance_update_logger.info("Waiting for parse time")

    now = datetime.datetime.now()
    target_time = datetime.datetime(now.year, now.month, now.day, 0, 20)

    if now > target_time:
        target_time += datetime.timedelta(days=1)

    delta_second = (target_time - now).total_seconds()
    await asyncio.sleep(delta_second)


async def main():
    while True:
        relevance_update_logger.info("Starting updating cycle")

        relevance_update_logger.info("Getting current product in db")
        async with aiohttp.ClientSession(timeout=0) as session:
            new_products_spus = session.get(DEWU_API_GET_NEW_PRODUCTS)

        await process_spus(new_products_spus)
        await wait_until_parse_api()


def start_relevance_update_cycle():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    relevance_update_logger.info("Starting new products update process")

    loop.run_until_complete(main())
