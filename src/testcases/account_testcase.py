from settings.logger_config import logger
from src.testcases.abstract_common_testcase import AbstractTestCase
from src.pages.base_page_a import BaseTestSteps
from src.pages.account_page_a import AccountTestSteps
from src.pages.assets_page_a import AssetsTestSteps

class TestCaseCheckLogout(AbstractTestCase):
    def __init__(self):
        super().__init__("로그 아웃 기능 확인")

    def run_testcase(self):
        try:
            AssetsTestSteps.login_google()
            AccountTestSteps.logout()
        except Exception as error:
            logger.error(f"[ERROR] {super().description}\n{error}")
            raise Exception(f"[ERROR] {super().description}")

class TestCaseCheckChatbotPageTransition(AbstractTestCase):
    def __init__(self):
        super().__init__("문의하기 페이지 노출 및 앱 전환")

    def run_testcase(self):
        try:
            AccountTestSteps.logout()
            AccountTestSteps.check_chatbot_page_transition()
        except Exception as error:
            logger.error(f"[ERROR] {super().description}\n{error}")
            raise Exception(f"[ERROR] {super().description}")
