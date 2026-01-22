import logging


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


user_update_logger = logging.getLogger('UserParse')
user_update_logger.setLevel(logging.INFO)
user_update_handler = logging.FileHandler('logs/user_parse.log')
user_update_handler.setFormatter(formatter)
user_update_logger.addHandler(user_update_handler)

passive_update_logger = logging.getLogger('PassiveParse')
passive_update_logger.setLevel(logging.INFO)
passive_update_handler = logging.FileHandler('logs/passive_parse.log')
passive_update_handler.setFormatter(formatter)
passive_update_logger.addHandler(passive_update_handler)

relevance_update_logger = logging.getLogger('RelevanceParse')
relevance_update_logger.setLevel(logging.INFO)
relevance_update_handler = logging.FileHandler('logs/relevance_update.log')
relevance_update_handler.setFormatter(formatter)
relevance_update_logger.addHandler(relevance_update_handler)

reprocess_logger = logging.getLogger('ReprocessAllParse')
reprocess_logger.setLevel(logging.INFO)
reprocess_handler = logging.FileHandler('logs/reprocess_all_parse.log')
reprocess_handler.setFormatter(formatter)
reprocess_logger.addHandler(reprocess_handler)

process_exceptions_logger = logging.getLogger('ProcessExceptions')
process_exceptions_logger.setLevel(logging.ERROR)
process_exceptions_handler = logging.FileHandler('logs/process_exceptions.log')
process_exceptions_handler.setFormatter(formatter)
process_exceptions_logger.addHandler(process_exceptions_handler)
