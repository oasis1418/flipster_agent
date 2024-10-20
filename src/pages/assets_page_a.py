import time
from src.controllers.element_controller import Element
from settings.logger_config import logger
from src.controllers.device_controller import get_device_type
import src.controllers.driver_controller as DC

class AssetsElements:
    """
    assets 페이지에서 사용하는 엘리먼트 정의.
    """
    def google_login_button():
        """assets 페이지에 google 로그인 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="Continue with Google"]'
        return '//android.widget.TextView[@text="Continue with Google"]'

    def google_login_continue_button():
        """google 계정으로 다시로그인 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="계속"]'
        return '//android.widget.Button[@resource-id="com.google.android.gms:id/continue_button"]'

    def google_login_id_button():
        """google 계정 로그인 id 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeOther[@name="로그인 - Google 계정"]/XCUIElementTypeOther[4]/XCUIElementTypeOther[1]'

    def passkey_deny_button():
        """Passkey 사용여부 팝업 Deny 버튼"""
        if get_device_type() == "ios":
            return """//XCUIElementTypeButton[@name="Don't allow"]"""
        return '//android.widget.TextView[@text="Deny"]'



class AssetsTestSteps:
    """
    assets 사용할 수 있는 기능 정의.
    """
    def login_google():
        from src.pages.base_page_a import BaseTestSteps
        from src.pages.account_page_a import AccountElements
        teststep_description = "assets 페이지에서 google 로그인 수행"
        try:
            BaseTestSteps.move_to_footer("Assets")
            if Element(AssetsElements.google_login_button()).isVisible(3, False) == True:
                Element(AssetsElements.google_login_button()).click()
                if get_device_type() == "ios":
                    DC.driver.execute_script('mobile: alert', {'action': 'accept', 'buttonLabel': '계속'})
                    Element(AssetsElements.google_login_id_button()).click()
                    Element(AssetsElements.google_login_continue_button()).click()
                else:
                    Element(AssetsElements.google_login_continue_button()).click()
                if Element(AssetsElements.passkey_deny_button()).isVisible(20, False) == True:
                    Element(AssetsElements.passkey_deny_button()).click(5, 0)
                BaseTestSteps.move_to_account()
                Element(AccountElements.nickname_text()).isVisible()
        except Exception as error:
            raise Exception(f"[ERROR] {teststep_description}\n{error}")
    