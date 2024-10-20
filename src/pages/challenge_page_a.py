import json
import time
import src.controllers.driver_controller as DC
from src.controllers.element_controller import Element
from settings.logger_config import logger
from src.reports.report import send_result
from src.controllers.device_controller import get_device_type

class ChallengeElements:
    """
    Challenge 페이지에서 사용하는 엘리먼트 정의.
    """
    def launch_airdrop_button():
        """Challenge 페이지에 Launch Airdrop 버튼"""
        if get_device_type() == "ios":
            return '(//XCUIElementTypeStaticText[@name="Launch Airdrop"])[2]'
        return '//android.widget.TextView[@text="Launch Airdrop"]'

class ChallengeTestSteps:
    """
    Challenge 사용할 수 있는 기능 정의.
    """
    def check_challenge_event_info():
        """
        Challenge 이벤트 정보 확인
        """
        teststep_description = "Challenge 이벤트 기간 및 종료여부 데이터 수집"
        try:
            
            Element(ChallengeElements.launch_airdrop_button()).click()
            time.sleep(1)
            event_infos = []
            check_first_test = True
            for i in range(10):
                if get_device_type() == "ios":
                    if check_first_test == True:
                        event_info = {
                            'ticker' : DC.driver.find_element('xpath','(//XCUIElementTypeButton[@name="Learn more"]/..//XCUIElementTypeStaticText[@visible="true"])[3]').text,
                            'period' : DC.driver.find_element('xpath','(//XCUIElementTypeButton[@name="Learn more"]/..//XCUIElementTypeStaticText[@visible="true"])[1]').text,
                            'Status' : DC.driver.find_element('xpath','(//XCUIElementTypeButton[@name="Learn more"]/..//XCUIElementTypeStaticText[@visible="true"])[2]').text,
                        }
                    else:
                        ticker = DC.driver.find_element('xpath','(//XCUIElementTypeButton[@name="Learn more"]/..//XCUIElementTypeStaticText[@visible="true"])[5]').text
                        if any(event['ticker'] == ticker for event in event_infos):
                            break
                        event_info = {
                            'ticker' : ticker,
                            'period' : DC.driver.find_element('xpath','(//XCUIElementTypeButton[@name="Learn more"]/..//XCUIElementTypeStaticText[@visible="true"])[3]').text,
                            'Status' : DC.driver.find_element('xpath','(//XCUIElementTypeButton[@name="Learn more"]/..//XCUIElementTypeStaticText[@visible="true"])[4]').text,
                        }
                else:
                    event_info_views = Element('//android.widget.TextView[@text="Learn more"]/../..').find()
                    ticker = event_info_views[0].find_element('xpath','//android.widget.TextView[@index=0]').text
                    if any(event['ticker'] == ticker for event in event_infos):
                        break
                    event_info = {
                        'ticker' : ticker,
                        'period' : event_info_views[0].find_element('xpath','//android.widget.TextView[@index=3]').text,
                        'Status' : event_info_views[0].find_element('xpath','//android.widget.TextView[@index=4]').text,
                    }
                event_infos.append(event_info)
                # Challenge 이벤트 정상 노출 확인
                if any(event_info[key] is None for key in ['ticker', 'period', 'Status']):
                    raise Exception(f"[FAIL] {teststep_description} 케이스 실패")
                else:
                    if get_device_type() == "ios":
                        Element('//XCUIElementTypeButton[@name="Learn more"]').coordinates_swipe(350, 400, 50, 400)
                    else:
                        Element('//android.widget.TextView[@text="Learn more"]/../..').coordinates_swipe(900, 1000, 200, 1000)
                check_first_test = False
            send_result("teststep", "Challenge 이벤트 정보 정상 확인", f"정상 확인 한 이벤트 정보 : {json.dumps(event_infos, indent=4)}", "pass")
        except Exception as error:
            send_result("teststep", "Challenge 이벤트 정보 에러", f"에러 발생 이벤트 정보 : {json.dumps(event_infos, indent=4)} \n Error Message : {error}", "fail")
            raise Exception(f"[ERROR] {teststep_description}\nError Message : {error}")
    