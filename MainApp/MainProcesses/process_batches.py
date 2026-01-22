import asyncio

import aiohttp

from Processing.process_spu import process_spu


async def process_main_batch(spus):
    async with aiohttp.ClientSession() as session:
        for spu_id in spus:
            await process_spu(spu_id)


async def process_spus(spus, number_of_workers=1):
    batches = [[spus[i] for i in
               range(j, len(spus), number_of_workers)] for j in range(number_of_workers)]

    tasks = [process_main_batch(batch) for batch in batches]

    await asyncio.gather(*tasks)
