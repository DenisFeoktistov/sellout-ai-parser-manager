import asyncio

import aiohttp


async def response_stable(*args, call_function=None,
                          return_value=False,
                          connection_failed_timeout=60,
                          **kwargs):
    while True:
        try:
            async with call_function(*args, **kwargs) as response:
                if response.status == 200:
                    if return_value:
                        result = await response.json()

                        return result

                if response.status in [502, 503, 504]:
                    await asyncio.sleep(connection_failed_timeout)

                    continue

                return None
        except aiohttp.ClientError as e:
            await asyncio.sleep(connection_failed_timeout)
