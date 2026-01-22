import asyncio
import datetime

import aiohttp

from MainApp.MainProcesses.process_batches import process_spus
from functions.fetch_functions.get_response_stable import response_stable
from logger import passive_update_logger


PASSIVE_UPDATE_LIST = "https://sellout.su/api/v1/product/popular_spu_id"


async def wait_until_parse_api():
    passive_update_logger.info("Waiting for parse time")

    now = datetime.datetime.now()
    target_time = datetime.datetime(now.year, now.month, now.day, 0, 20)

    if now > target_time:
        target_time += datetime.timedelta(days=1)

    delta_second = (target_time - now).total_seconds()
    await asyncio.sleep(delta_second)


async def main():
    async with aiohttp.ClientSession() as session:
        passive_update_list = await response_stable(PASSIVE_UPDATE_LIST, call_function=session.get,
                                                    return_value=True)

    await process_spus(passive_update_list, number_of_workers=3)
    await wait_until_parse_api()


def start_passive_update_cycle():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    passive_update_logger.info("Starting new products update process")

    loop.run_until_complete(main())
