from settings.logger_config import logger
from datasets.testsuite_collection import suit_list

def get_suit(suit_name: str):
    try:
        test_suit_list = suit_list[suit_name]
        return test_suit_list
    except Exception as e:
        logger.error(f"Suit Not Found (suit name : {suit_name}) : ", e)
