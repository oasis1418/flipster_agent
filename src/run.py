import sys
from .controllers.driver_controller import remote
from .controllers.element_controller import set_context, set_window_count, Element
from settings.argument_config import get_argument
from src.controllers.testcase_controller import TestCaseRun
from .controllers.device_controller import get_device_info
from settings.logger_config import logger
from src.reports.report import set_result_id

g_device_name: str = get_argument("device_name")
g_suit_name_list: list = get_argument("suit_name")
g_slack_channel_id: list = get_argument("slack_channel_id")
g_install_app_build_number: list = get_argument("install_app_build_number")



def startup():
    """
    테스트 자동화 시작
    - 테스트 자동화 수행에 대한 정의
    """
    try:
        logger.info("============================================================================================================")
        logger.info("[Running] Test Automation Start")
        logger.info(f" | device        : {g_device_name}")
        logger.info(f" | suit          : {g_suit_name_list}")
        logger.info("============================================================================================================")
        # 테스트 결과 id 설정
        set_result_id()
        # 단말 정보 입력
        device_info = get_device_info(g_device_name)
        remote.set_device_info(device_info)
        set_context("NATIVE_APP")
        set_window_count(1)
        # Device Remote 수행
        run_remote()
        # Test Suit 수행
        run_suit(device_info)
        logger.info("[Finished] Test Automation")
    except Exception as error:
        logger.error(f"[ERROR] startup - {g_device_name}\n {error}")

def run_remote():
    """_드라이버 리모트_"""
    try:
        logger.info(f"[Running] Remote Device Start")
        remote.run_device_remote()
    except Exception as error:
        logger.error(f"[ERROR] Remote Device - {g_device_name}\n {error}")
        raise Exception(f"[Error Message] {error}")

def run_suit(device_info: dict[str, any]):
    """_테스트 스윗 수행_"""
    try:
        testcase = TestCaseRun()
        testcase.run_test(device_info, g_suit_name_list)
    except Exception as error:
        logger.error(f"[ERROR] Run Test Suit - {g_suit_name_list}\n {error}")
        raise Exception(f"[Error Message] {error}")

