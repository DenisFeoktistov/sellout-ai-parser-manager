import json

from constants import (DEWU_API_PARSER_URL,
                       BACKEND_PRODUCT_BY_SPU_URL,
                       BACKEND_UPDATE_URL,
                       HK_API_PARSER_URL
                       )
import aiohttp

from functions.fetch_functions.get_response_stable import response_stable
from logger import user_update_logger


async def process_spu(spu_id):
    async with aiohttp.ClientSession() as session:
        dewu_data = await response_stable(DEWU_API_PARSER_URL(spu_id), call_function=session.get, return_value=True)
        # async with session.get(DEWU_API_PARSER_URL(spu_id)) as response:
        #     dewu_data = await response.json()

        sku = dewu_data["manufacturer_sku"]

        # hk_data = await response_stable(HK_API_PARSER_URL(sku), call_function=session.get, return_value=True)
        hk_data = dict()

        # merge_data
        result = merge_data(dewu_data, hk_data)

        with open("result.json", "w") as file:
            file.write(json.dumps(result, indent=4, ensure_ascii=False))

        # print(json.dumps(result, ensure_ascii=False))
        # print(BACKEND_UPDATE_URL)
        async with session.post(BACKEND_UPDATE_URL, json=result) as response:
            data = await response.text()

            # user_update_logger.info("Data sent")
            # print("REQUEST SENT", data)

            # print(data)

        # print(1)

        return result


def merge_data(dewu_data, hk_data):
    result = dict()

    for key in list(dewu_data.keys()) + list(hk_data.keys()):

        if key in ["model", "colorway", "lines", "images"] and key in dewu_data:
            result[key] = dewu_data[key]
        elif key in dewu_data and key in hk_data:
            if len(str(hk_data[key])) > len(str(dewu_data[key])):
                result[key] = hk_data[key]
            else:
                result[key] = dewu_data[key]
        else:
            if key in dewu_data:
                result[key] = dewu_data[key]
            elif key in hk_data:
                result[key] = hk_data[key]

    if "deliveries_indent" in dewu_data:
        for sku in result["skus"]:
            sku["delivery_info"]["min_platform_delivery"] += dewu_data["deliveries_indent"]
            sku["delivery_info"]["max_platform_delivery"] += dewu_data["deliveries_indent"]

    if ("many_sku_api_price" in dewu_data and not hk_data["many_colors"]) or "one_sku_api_price" in dewu_data:
        if "many_sku_api_price" in dewu_data:
            result["skus"][0]["zh_price"] = dewu_data["many_sku_api_price"]
        else:
            result["skus"][0]["zh_price"] = dewu_data["one_sku_api_price"]

        result["skus"] = result["skus"][:1]

    return result
