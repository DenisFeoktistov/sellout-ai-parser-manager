import multiprocessing

import aiohttp

from MainApp.MainProcesses.relevance_update import start_relevance_update_cycle
from MainApp.MainProcesses.relevance_update_worker import start_relevance_update_worker_cycle
from Processing.process_spu import process_spu
from MainApp.MainProcesses.reprocess import start_reprocess_cycle
from MainApp.MainProcesses.passive_update import start_passive_update_cycle


class MainApp:
    def __init__(self):
        self.relevance_update_process = None
        self.relevance_update_worker_process = None
        self.passive_update_process = None
        self.reprocess_process = None

    def start_relevance_update_worker_process(self, new_products_list):
        if self.relevance_update_worker_process:
            self.relevance_update_worker_process.terminate()
            self.relevance_update_worker_process.close()

        self.relevance_update_worker_process = multiprocessing.Process(target=start_relevance_update_worker_cycle,
                                                                       args=(new_products_list,))
        self.relevance_update_worker_process.start()

    def start(self):
        self.relevance_update_process = multiprocessing.Process(target=start_relevance_update_cycle)
        self.relevance_update_process.start()

        # self.passive_update_process = multiprocessing.Process(target=start_passive_update_cycle)
        # self.passive_update_process.start()

    def reprocess_all_products(self):
        if self.reprocess_process:
            self.reprocess_process.terminate()
            self.reprocess_process.close()

        self.reprocess_process = multiprocessing.Process(target=start_reprocess_cycle)
        self.reprocess_process.start()

    @staticmethod
    async def process_spu(spu_id):
        result = await process_spu(spu_id)

        return result
