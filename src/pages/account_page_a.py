import time
from src.controllers.element_controller import Element
from settings.logger_config import logger
from src.reports.report import send_result
from src.controllers.device_controller import get_device_type
import src.controllers.driver_controller as DC

class AccountElements:
    """
    account 페이지에서 사용하는 엘리먼트 정의.
    """
    def title_account_text():
        """account 페이지 타이틀 문구"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="account_main_title"]'
        return '//android.widget.TextView[@content-desc="account_main_title" and @text="Account"]'

    def sign_out_button():
        """account 페이지 Sign out 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="account_sign_out"]'
        return '//android.view.View[@content-desc="account_sign_out"]'

    def nickname_text():
        """account 페이지 nick name 텍스트"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="account_nick_value_01"]'
        return '//android.widget.TextView[@content-desc="account_nick_value_01"]'

    def leader_board_button():
        """account 페이지 leader board 버튼"""
        if get_device_type() == "ios":
            return '(//XCUIElementTypeImage[@name="Icon_24"])[1]'
        return '//android.view.View[@content-desc="tab_account_lb_wv"]'

    def vip_benefits_button():
        """account 페이지 vip benefits 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="tab_view_vip_benefits"]'
        return '//android.widget.TextView[@content-desc="tab_view_vip_benefits"]'

    def support_announcement_button():
        """account 페이지 announcement 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="Setting_Announcement"]'
        return '//android.widget.TextView[@text="Announcement"]'

    def chatbot_button():
        """account 페이지 chatbot 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="Open messaging window"]'
        return '//android.widget.Button[@text="Open messaging window"]'

    def chatbot_collapse_button():
        """chatbot 페이지 접기 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="Close"]'
        return '//android.widget.Button[@text="Toggle navigation menu"]'

class AccountTestSteps:
    """
    account 사용할 수 있는 기능 정의.
    """
    def logout():
        from src.pages.base_page_a import BaseTestSteps
        teststep_description = "account 페이지에서 sign out 버튼 클릭하여 로그아웃 수행"
        try:
            BaseTestSteps.move_to_footer("Market")
            BaseTestSteps.move_to_account()
            if Element(AccountElements.nickname_text()).isVisible(3, False) == False:
                send_result("teststep", "로그 아웃 기능 수행", f"현재 로그 아웃 상태 (로그 아웃 수행 Skip)", "pass")
                return
            else:
                Element(AccountElements.sign_out_button()).element_swipe("down")
                Element(AccountElements.sign_out_button()).click()
            BaseTestSteps.move_to_account()
            if Element(AccountElements.nickname_text()).isVisible(3, False) == True:
                send_result("teststep", "로그 아웃 기능 수행", f"로그 아웃 기능 실패", "fail")
        except Exception as error:
            send_result("teststep", "로그 아웃 기능 수행", f"로그 아웃 기능 에러 \n {error}", "fail")
            raise Exception(f"[ERROR] {teststep_description}\n{error}")
    
    def check_chatbot_page_transition():
        from src.pages.base_page_a import BaseTestSteps
        teststep_description = "문의하기 페이지 노출 및 앱 전환"
        try:
            BaseTestSteps.move_to_account()
            Element(AccountElements.support_announcement_button()).element_swipe("down")
            Element(AccountElements.support_announcement_button()).click()
            if get_device_type() == "ios":
                Element(AccountElements.chatbot_button()).click_element_location(30, 30, 20, 0)
            else:
                Element(AccountElements.chatbot_button()).click(20, 0)
            Element(AccountElements.chatbot_collapse_button()).click()
            if Element(AccountElements.title_account_text()).isVisible(3, False) == True:
                send_result("teststep", "쳇봇 화면에서 Account 페이지 앱 전환 성공", "쳇봇 화면에서 collapse 버튼 클릭 시 Account 페이지 앱 전환 정상 확인", "pass")
            else:
                raise Exception(f"[ERROR] 쳇봇 화면에서 collapse 버튼 클릭 시 Account 페이지 앱 전환 실패")
        except Exception as error:
            send_result("teststep", f"{teststep_description} 에러", f"{teststep_description} 에러 \n {error}", "fail")
            raise Exception(f"[ERROR] {teststep_description}\n{error}")


        