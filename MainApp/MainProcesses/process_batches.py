import asyncio

import aiohttp

from Processing.process_spu import process_spu
from logger import process_exceptions_logger


async def process_main_batch(spus):
    # process_exceptions_logger.info(f"SPUS")
    # process_exceptions_logger.info(f"{spus}")

    for spu_id in spus:
        try:
            await process_spu(spu_id)
        except Exception as e:
            # process_exceptions_logger.info(e)
            # process_exceptions_logger.info(f"Exception spu id {spu_id}")
            pass


async def process_spus(spus, number_of_workers=1):
    batches = [[spus[i] for i in
               range(j, len(spus), number_of_workers)] for j in range(number_of_workers)]

    # process_exceptions_logger.info(f"{batches}")
    process_exceptions_logger.info("Batches are done")
    tasks = [process_main_batch(batch) for batch in batches]

    await asyncio.gather(*tasks)

