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


async def main(new_products_list):
    relevance_update_logger.info("Starting updating cycle")
    relevance_update_logger.info(len(new_products_list))

    await process_spus(new_products_list, number_of_workers=5)

    relevance_update_logger.info("Updating cycle finished")


def start_relevance_update_worker_cycle(new_products_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    relevance_update_logger.info("Starting new products update process")

    loop.run_until_complete(main(new_products_list))
