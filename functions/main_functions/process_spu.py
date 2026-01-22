from constants import BACKEND_UPDATE_URL
from functions.fetch_functions.get_from_api_async import get_from_api_async
from functions.fetch_functions.get_response_stable import response_stable
from functions.process_data_functions.preprocess_dewu_api import preprocess_dewu_api
from functions.process_data_functions.process_preprocessed_api_data import process_preprocessed_api_data


async def process_spu(spu_id, session):
    dewu_api_data = await get_from_api_async(spu_id)
    dewu_preprocessed_data = preprocess_dewu_api(dewu_api_data)
    dewu_processed_data = process_preprocessed_api_data(dewu_preprocessed_data)

    result = await response_stable(BACKEND_UPDATE_URL, call_function=session.post, json=dewu_processed_data)

    return result
