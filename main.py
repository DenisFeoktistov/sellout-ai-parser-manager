import asyncio
import requests
from urllib.parse import urlparse, parse_qs

from multiprocessing import freeze_support

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from MainApp.MainAppClass import MainApp

main_app = MainApp()
api_app = FastAPI()


def get_spu_id(url):
    response = requests.head(url, allow_redirects=False)
    if 'location' in response.headers:
        redirect_url = response.headers['location']
        parsed_url = urlparse(redirect_url)

        if 'spuId' in parse_qs(parsed_url.query):
            spu_id = int(parse_qs(parsed_url.query)['spuId'][0])
            return spu_id
        else:
            return None
    else:
        return None


@api_app.get("/intermediate_parser/process_spu_id")
async def process_spu(spu_id: int):
    asyncio.create_task(MainApp.process_spu(spu_id))

    return JSONResponse(status_code=200, content={"message": "Product will be updated in nearest time"})


@api_app.post("/intermediate_parser/process_link")
async def process_link(request: Request):
    data = await request.json()
    url = data.get("url")
    spu_id = get_spu_id(url)

    result = await MainApp.process_spu(spu_id)

    return result


@api_app.get("/intermediate_parser/reprocess")
async def reprocess():
    main_app.reprocess_all_products()

    return JSONResponse(status_code=200, content={"message": "Reprocess has been started"})


if __name__ == "__main__":
    # freeze_support()
    # main_app.start()

    uvicorn.run(api_app, host='0.0.0.0', port=5000)
