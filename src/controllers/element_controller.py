import time
import src.controllers.driver_controller as DC
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from settings.logger_config import logger
from src.reports.report import send_result
from src.controllers.device_controller import get_device_type

global CONTEXT
global WINDOW_COUNT


class Element:
    """
    _엘리먼트 클래스_
        Args:
            resource_id (str): id 또는 xpath 입력
        Retruns:
            엘리먼트 클래스 인스턴스
    """

    def __init__(self, resource_id: str=None):
        self.resource_id = resource_id

    def find(self, retry: int = 10):
        """
        _엘리먼트 찾기_
            Args:
                retry (int): Find Element 재 실행 횟수 (기본 재실행 retry = 10) - 10초 동안 찾기
            Retruns:
                WebElement (List): 엘리멘트 리스트 반환 (이후 action 을 위해 index 선택 필요)
        """
        try:
            elements = self.get_element(retry)
            if len(elements) > 0:
                send_result("teststep", "[Find] 엘리먼트 리스트 반환", f"{self.resource_id} 엘리먼트 리스트 반환 (size : {len(elements)})", "pass")
            else:
                send_result("teststep", "[Find] 엘리먼트 리스트 반환", f"{self.resource_id} 엘리먼트 리스트 반환 (size : {len(elements)})", "pass")
            return elements
        except Exception as error:
            send_result("teststep", "[Find] 엘리먼트 리스트 반환", f"{self.resource_id} 엘리먼트 리스트 반환 \n {error}", "fail")
            raise Exception(f"[ERROR] Find Element - {self.resource_id}\n{error}")

    def get_element(self, retry: int = 10):
        """_엘리멘트 가져오기_"""
        try:
            logger.info(f"resource_id : {self.resource_id}")
            global CONTEXT
            global WINDOW_COUNT
            element_type = "xpath"
            # Element Type 결정
            if "//" not in self.resource_id:
                element_type = "id"
            # 요소를 저장할 리스트 초기화
            elements = []
            # 엘리멘트를 찾을 때 까지 retry 만큼 재시도
            for i in range(retry):
                elements = DC.driver.find_elements(element_type, self.resource_id)
                logger.info(f"[ELEMENT] Find Element #Retry({i}) | (context : {CONTEXT}) | ({element_type} : {self.resource_id}) | (size : {len(elements)})")
                if len(elements) > 0: #elements[0].is_displayed()
                    break
                time.sleep(1)
            return elements
        except Exception as error:
            raise Exception(f"[ERROR] Get Element\n{error}")

    def click(self, retry:int=10, element_index:int=0):
        """
        엘리먼트 클릭
        Args:
            retry (int): 엘리먼트 찾기 대기 시간 (기본 retry = 10) - 10초
            element_index (int): 찾은 엘리먼트가 여러개 있을 경우 입력한 index 엘리먼트 클릭 (기본 index = 0)
        """
        try:
            elements = self.get_element(retry)
            isDisplayed = elements[element_index].is_displayed()
            if isDisplayed == False:
                if get_device_type() == "ios":
                    # 엘리먼트의 위치 가져오기
                    location = elements[element_index].location
                    size = elements[element_index].size
                    # 엘리먼트의 중앙 좌표 계산
                    x = location['x'] + size['width'] / 2
                    y = location['y'] + size['height'] / 2
                    # 해당 좌표로 스와이프
                    DC.driver.execute_script("mobile: swipe", {"direction": "up", "duration": 1000, "x": x, "y": y})
                    time.sleep(1)
            elements[element_index].click()
            send_result("teststep", "[Click] 화면 요소 클릭", f"{self.resource_id} 엘리먼트 클릭 성공", "pass")
        except Exception as error:
            send_result("teststep", "[Click] 화면 요소 클릭", f"{self.resource_id} 엘리먼트 클릭 실패 \n {error}", "fail")
            raise Exception(f"[ERROR] Click Element\n{error}")

    def click_element_location(self, plus_x:int=0, plus_y:int=0, retry:int=10, element_index:int=0):
        """
        엘리먼트 좌표 계산하여 클릭
        - 엘리먼트 클릭 시 기본 적으로 왼쪽 위쪽 좌표를 클릭함, 클릭 범위가 일치하지 않을 경우 plus_x, plus_y 좌표로 계산하여 좌표 클릭.

        Args:
            plus_x (int): 찾은 엘리먼트 좌표에 x 값 더하기
            plus_y (int): 찾은 엘리먼트 좌표에 y 값 더하기
            retry (int): 엘리먼트 찾기 대기 시간 (기본 retry = 10) - 10초
            element_index (int): 찾은 엘리먼트가 여러개 있을 경우 입력한 index 엘리먼트 클릭 (기본 index = 0)
        """
        try:
            elements = self.get_element(retry)
            location = elements[0].location
            x = location['x']
            y = location['y']
            x = x + plus_x
            y = y + plus_y
            DC.driver.tap([(x, y)])
            send_result("teststep", "[Click] 엘리먼트 location 클릭", f"{self.resource_id} (x: {x}, y: {y}) 엘리먼트 클릭 성공", "pass")
        except Exception as error:
            send_result("teststep", "[Click] 엘리먼트 location 클릭", f"{self.resource_id} (x: {x}, y: {y}) 엘리먼트 클릭 실패 \n {error}", "fail")
            raise Exception(f"[ERROR] Click Element\n{error}")
    
    
    def isVisible(self, wait_time:int=5, stop_on_failure:bool=True):
        """
        엘리먼트 클릭
        Args:
            wait_time (int): 대기 시간 설정, (기본 wait_time = 5, 5초 동안 retry)
            stop_on_failure (bool): 화면요소 못찾을 경우 결과 처리, (기본 True = 케이스 동작 멈춤, False = 무시하고 수행)
        
        Returns:
            is_visible (bool) : 찾는 화면 요소가 있으면 True, 없으면 False.
        """
        try:
            elements = self.get_element(wait_time)
            if len(elements) > 0:
                send_result("teststep", "[IsVisible] 화면 요소 찾기", f"{self.resource_id} 엘리먼트 찾기 성공", "pass")
                return True
            else:
                if stop_on_failure:
                    send_result("teststep", "[IsVisible] 화면 요소 찾기", f"{self.resource_id} 엘리먼트 찾기 실패", "fail")
                    raise Exception(f"[ERROR] Is Visible Element \n{error}")
                else:
                    send_result("teststep", "[IsVisible] 화면 요소 찾기", f"{self.resource_id} 엘리먼트 찾기 실패 (화면 요소 못찾을 경우에도 계속 수행)", "pass")
                    return False
        except Exception as error:
            send_result("teststep", "[IsVisible] 화면 요소 찾기", f"{self.resource_id} 엘리먼트 찾기 에러 \n {error}", "fail")
            raise Exception(f"[ERROR] Is Visible Element \n{error}")

    def coordinates_swipe(self, press_x, press_y, move_x, move_y):
        """
        좌표 스크롤

        Args:
            press_x (int): 10 (스크롤 시작 부분 x 값)
            press_y (int): 50 (스크롤 시작 부분 y 값)
            move_x (int): 10 (스크롤 끝 부분 x 값)
            move_y (int): 100 (스크롤 끝 부분 y 값)
        Retruns:
            None
        """
        try:
            logger.info(f"[ELEMENT] location swipe - press_x:{press_x}, press_y:{press_y}, move_x:{move_x}, move_y:{move_y}")
            DC.driver.swipe(press_x, press_y, move_x, move_y, 1000)
            # TouchAction(DC.driver).long_press(x=press_x, y=press_y).move_to(x=move_x, y=move_y).release().perform()
            send_result("teststep", "[Swipe] 좌표 Swipe 수행", f"좌표 Swipe 성공 ({press_x}, {press_y} | {move_x}, {move_y})", "pass")
            time.sleep(1)
        except Exception as error:
            send_result("teststep", "[Swipe] 좌표 Swipe 수행", f"좌표 Swipe 실패 ({press_x}, {press_y} | {move_x}, {move_y}) \n {error}", "fail")
            raise Exception(f"[ERROR] Location swipe\n{error}")

    def element_swipe(self, swipe_direction: str = "down"):
        """
        엘리먼트 찾을 때 까지 스크롤
        - 최대 10번 swipe 수행 
        Args:
            swipe_direction (str): 화면 이동 방향 (up = 위로 이동, down = 아래로 이동, right = 오른쪽 이동, left = 왼쪽 이동)
        """
        try:
            i = 0
            elements = []
            while i < 10:
                i += 1
                elements = self.get_element(1)
                logger.info(f"[ELEMENT] Element swipe ({i}) | {swipe_direction} | {self.resource_id} | {len(elements)}")
                time.sleep(1)
                if len(elements) > 0:
                    send_result("teststep", "[Swipe] 엘리먼트 Swipe 수행", f"엘리먼트 Swipe 성공 ({i}) | {swipe_direction} | {self.resource_id} | {len(elements)})", "pass")
                    return
                else:
                    if get_device_type() == "ios":
                        if swipe_direction == "up":
                            DC.driver.swipe(200, 190, 200, 780, 1000)
                        elif swipe_direction == "down":
                            DC.driver.swipe(200, 780, 200, 190, 1000)
                        elif swipe_direction == "right":
                            DC.driver.swipe(350, 400, 50, 400, 1000)
                        elif swipe_direction == "left":
                            DC.driver.swipe(50, 400, 350, 400, 1000)
                    else:
                        if swipe_direction == "up":
                            DC.driver.swipe(500, 500, 500, 1800, 1000)
                        elif swipe_direction == "down":
                            DC.driver.swipe(500, 1800, 500, 500, 1000)
                        elif swipe_direction == "right":
                            DC.driver.swipe(900, 1000, 200, 1000, 1000)
                        elif swipe_direction == "left":
                            DC.driver.swipe(200, 1000, 900, 1000, 1000)
            send_result("teststep", "[Swipe] 엘리먼트 Swipe 수행", f"엘리먼트 Swipe 실패 ({i}) | {swipe_direction} | {self.resource_id} | {len(elements)})", "fail")
        except Exception as error:
            send_result("teststep", "[Swipe] 엘리먼트 Swipe 수행", f"엘리먼트 Swipe 에러 ({i}) | {swipe_direction} | {self.resource_id} | {len(elements)}) \n {error}", "fail")
            raise Exception(f"[ERROR] Element swipe\n{error}")

    def element_list_find_text_click(self, text: str):
        """_엘리멘트를 찾고 리스트 중 일치하는 Text 클릭_"""
        try:
            elements = self.get_element()
            for i in range(len(elements)):
                logger.info(f"[ELEMENT] Element Text Click ({i}) | {text} | {self.resource_id} | {len(elements)}")
                if elements[i].text == text:
                    elements[i].click()
                    return
        except Exception as error:
            raise Exception(f"[ERROR] Element Text Click\n{error}")

    def hide_keyboard(self):
        """_키보드 닫기_"""
        try:
            is_keyboard_show = DC.driver.is_keyboard_shown()
            logger.info(f"[ELEMENT] Hide Keyboard - {is_keyboard_show}")

            if is_keyboard_show:
                DC.driver.hide_keyboard()
        except Exception as error:
            raise Exception(f"[ERROR] Hide Keyboard\n{error}")


def set_context(context):
    global CONTEXT
    CONTEXT = context

def set_window_count(count):
    global WINDOW_COUNT
    WINDOW_COUNT = count
