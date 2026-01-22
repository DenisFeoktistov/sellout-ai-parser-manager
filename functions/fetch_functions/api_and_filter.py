import time

from functions.process_data_functions.filter_api import filter_api
from constants import DEWU_API_URL


async def api_and_filter(i, session):
    start = time.time()

    try:
        async with session.get(DEWU_API_URL(i)) as response:
            end = time.time()
            # print(i, response.status, end - start)

            if response.status == 200:
                data = await response.json()

                if filter_api(data):
                    return i, True
    except Exception:
        pass

    return i, False
