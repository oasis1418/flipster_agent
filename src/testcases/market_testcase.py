from settings.logger_config import logger
from src.testcases.abstract_common_testcase import AbstractTestCase
from src.pages.base_page_a import BaseTestSteps
from src.pages.assets_page_a import AssetsTestSteps
from src.pages.market_page_a import MarketTestSteps

class TestCaseCheckHighVolumeCoinInfo(AbstractTestCase):
    def __init__(self):
        super().__init__("Perpetual Selections 페이지에 High volume 영역에 코인 정보 정상 노출되는지 확인")

    def run_testcase(self):
        try:
            AssetsTestSteps.login_google()
            BaseTestSteps.move_to_footer("Market")
            MarketTestSteps.check_high_volume_coin_info()
        except Exception as error:
            logger.error(f"[ERROR] {super().description}\n{error}")
            raise Exception(f"[ERROR] {super().description}")