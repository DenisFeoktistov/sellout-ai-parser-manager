import aiohttp


async def get_from_api_async(spu_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://spucdn.dewu.com/dewu/commodity/detail/simple/{spu_id}.json") as response:
            if response.status == 200:
                return await response.json()
            else:
                return False


# async def add_new_product(self, spu_id):
#     for i in range(MainApp.NEW_TRY_CNT):
#         result = await fetch(MainApp.ADD_NEW_LINK(spu_id), self.get_random_proxy())
#
#         if not result:
#             await asyncio.sleep(1)
#         else:
#             return True
#
#     return False
