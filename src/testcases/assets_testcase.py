from settings.logger_config import logger
from src.testcases.abstract_common_testcase import AbstractTestCase
from src.pages.base_page_a import BaseTestSteps
from src.pages.assets_page_a import AssetsTestSteps
from src.pages.account_page_a import AccountTestSteps

class TestCaseCheckLogin(AbstractTestCase):
    def __init__(self):
        super().__init__("로그인 기능 확인")

    def run_testcase(self):
        try:
            AccountTestSteps.logout()
            AssetsTestSteps.login_google()
        except Exception as error:
            logger.error(f"[ERROR] {super().description}\n{error}")
            raise Exception(f"[ERROR] {super().description}")