import asyncio

import aiohttp

from MainApp.MainProcesses.process_batches import process_spus
from functions.fetch_functions.get_response_stable import response_stable
from logger import reprocess_logger


async def main():
    async with aiohttp.ClientSession() as session:
        processed_spus = set(
            await response_stable("https://sellout.su/api/v1/product/dewu_info_list", call_function=session.get,
                                  return_value=True))

    await process_spus(processed_spus, number_of_workers=2)


def start_reprocess_cycle():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    reprocess_logger.info("Starting new products update process")

    loop.run_until_complete(main())
