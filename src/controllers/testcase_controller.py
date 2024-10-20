from settings.logger_config import logger
from src.testcases.abstract_common_testcase import AbstractTestCase
from src.controllers.driver_controller import remote
from datasets.testsuite_collection import suit_list
from src.reports.report import send_result

g_testsuit: str
g_testcase: str
g_device_info: dict[str, any]
g_retry: str

class TestCaseRun:
    """
    테스트 케이스 수행.
    - 테스트 스윗에 해당하는 테스트 케이스 

    Attributes:
        retry (bool): 테스트 케이스 실패 시 다시 시도에 대한 설정
        test_suit (str) : 실행 할 테스트 스윗
        testcase_class (AbstractTestCase) : 테스트 케이스 대상 클래스
        device_info : 테스트 단말 정보

    Methods:
        run_test(test_device_info, suit_name_list): 테스트 케이스 수행
        retry_test(testcase_class_name): 테스트 케이스 실패 시 재 실행
    """

    def __init__(self):
        self.retry = True
        self.test_suit: str
        self.testcase_class: AbstractTestCase
        self.device_info: dict[str, any]

    def run_test(self, test_device_info:dict[str, any], suit_name_list_str: str):
        """
        테스트 케이스 수행
        Args:
            test_device_info (dict[str, any]): 테스트 단말 정보
            suit_name_list_str (str): 테스트 수행 명령어에 입력하였던 옵션 테스트 스윗 리스트
        """
        try:
            global g_testsuit
            global g_testcase
            global g_device_info

            self.device_info = test_device_info
            g_device_info = self.device_info
            suit_name_list = suit_name_list_str.split(",")
            for i in range(len(suit_name_list)):
                self.test_suit = suit_name_list[i]
                g_testsuit = self.test_suit
                testcases = suit_list[g_testsuit]
                # testcases = get_suit(suit_name_list[i])
                for i in range(len(testcases)):
                    g_testcase = testcases[i]["testcase"]
                    self.testcase_class: AbstractTestCase = testcases[i]["class"]
                    logger.info(f"[RUNNING] ==========  TestCase Start (description : {self.testcase_class.description} ) ==========")
                    self.retry_test(testcases[i])
        except Exception as error:
            logger.error(f"[Error] Test Case - ({g_testsuit} : {self.testcase_class.description})\n{error}")

    def retry_test(self, testcase_class_name):
        try:
            global g_retry
            remote.start_activity()
            self.testcase_class.before_testcase()
            self.testcase_class.run_testcase()
            self.testcase_class.after_testcase()
            remote.terminate_app()
            send_result("testcase", f"[Finished] {self.testcase_class.description} 정상 수행", f"{self.testcase_class.description} 정상 수행. Test Case is Finished.", "pass")
        except Exception as error:
            self.testcase_class.exception_testcase()
            if self.retry == True:
                self.retry = False
                logger.info(f"[RUNNING] ========== TestCase Retry ( description : {self.testcase_class.description} ) ==========")
                self.retry_test(testcase_class_name)
                return
            self.retry = True
            send_result("testcase", f"[Error] {self.testcase_class.description} 재시도 에러", f"{self.testcase_class.description} 재시도 에러 메시지 \n {error}", "fail")
            logger.info(f"[RUNNING] Retry Error : {self.testcase_class.description} \n {error}")
            remote.screenshot(testcase_class_name)

