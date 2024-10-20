from abc import *
from settings.logger_config import logger

class AbstractTestCase(metaclass=ABCMeta):
    """
    TestCase 작성 시 AbstractTestCase 추상 클래스로 필수로 작성해야 될 메소드 정의.
    - run_testcase 메소드를 반드시 구현해야 하며, 테스트 케이스 수행에 대한 기능 구현을 해야함.

    Attributes:
        description (str): 테스트 케이스에 대한 설명을 작성한다

    Methods:
        run_testcase(): 테스트 케이스 수행에 대한 스크립트 작성 (필수)
        before_testcase() : 테스트 케이스 수행 전 기능 구현에 사용
        after_testcase() : 테스트 케이스 수행 후 기능 구현에 사용
    """
    def __init__(self, description: str):
        self.__description = description

    @property
    def description(self):
        # 테스트 케이스에 대한 설명 작성.
        return self.__description

    @abstractmethod
    def run_testcase(self):
        # testcase 공통으로 run 을 수행하기 위한 메소드 구현에 필요.
        pass
    def before_testcase(self):
        # testcase 수행 전 수행해야할 기능 구현에 필요.
        try:
            pass
        except Exception as error:
            logger.error(f"[Error] Before Test Case - ({self.description})\n{error}")

    def after_testcase(self):
        # testcase 수행 후 수행해야할 기능 구현에 필요.
        try:
            pass
        except Exception as error:
            logger.error(f"[Error] After Test Case - ({self.description})\n{error}")

    def exception_testcase(self):
        try:
            pass
        except Exception as error:
            logger.error(f"[Error] Exception Test Case - ({self.description})\n{error}")
