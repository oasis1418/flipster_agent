from settings.logger_config import logger
from src.testcases.abstract_common_testcase import AbstractTestCase
from src.pages.base_page_a import BaseTestSteps
from src.pages.assets_page_a import AssetsTestSteps
from src.pages.market_page_a import MarketTestSteps
from src.pages.challenge_page_a import ChallengeTestSteps

class TestCaseCheckChallengeEventInfo(AbstractTestCase):
    def __init__(self):
        super().__init__("Challenge 페이지에 Launch Airdrop 이벤트 정보 확인")

    def run_testcase(self):
        try:
            AssetsTestSteps.login_google()
            BaseTestSteps.move_to_footer("Challenge")
            ChallengeTestSteps.check_challenge_event_info()
        except Exception as error:
            logger.error(f"[ERROR] {super().description}\n{error}")
            raise Exception(f"[ERROR] {super().description}")