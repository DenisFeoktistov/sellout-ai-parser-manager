import json

from constants import (DEWU_API_PARSER_URL,
                       BACKEND_PRODUCT_BY_SPU_URL,
                       BACKEND_UPDATE_URL,
                       HK_API_PARSER_URL
                       )
import aiohttp


async def process_spu(spu_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(DEWU_API_PARSER_URL(spu_id)) as response:
            dewu_data = await response.json()

        sku = dewu_data["manufacturer_sku"]

        async with session.get(HK_API_PARSER_URL(sku)) as response:
            hk_data = await response.json()

        # merge_data
        result = merge_data(dewu_data, hk_data)

        with open("result.json", "w") as file:
            file.write(json.dumps(result, indent=4, ensure_ascii=False))

        return result

        # async with session.post(BACKEND_UPDATE_URL(spu_id), data=result) as response:
        #     data = await response.json()


def merge_data(dewu_data, hk_data):
    result = dict()

    for key in list(dewu_data.keys()) + list(hk_data.keys()):
        if key in dewu_data and key in hk_data:
            if len(str(hk_data[key])) > len(str(dewu_data[key])):
                result[key] = hk_data[key]
            else:
                result[key] = dewu_data[key]
        else:
            if key in dewu_data:
                result[key] = dewu_data[key]
            elif key in hk_data:
                result[key] = hk_data[key]

    return result
