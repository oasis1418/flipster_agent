from src.controllers.element_controller import Element
from settings.logger_config import logger
from src.controllers.device_controller import get_device_type


class BaseElements:
    """
    공통으로 사용할 수 있는 엘리먼트 정의.
    """
    def header_account_button():
        """header 위치에 account 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="menu_icon"]'
        return '//*[@content-desc="menu_icon"]'
    
    def header_back_button():
        """header 위치에 back 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeButton[@name="back_icon"]'
        return '//android.widget.Button[@content-desc="back_icon"]'
    
    def footer_market_button():
        """footer 위치에 market 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="Market"]'
        return '//*[@content-desc="tab_market"]'

    def footer_challenge_button(): 
        """footer 위치에 challenge 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="Challenge"]'
        return '//*[@content-desc="tab_challenge"]'
    
    def footer_trade_button(): 
        """footer 위치에 trade 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="Trade"]'
        return '//*[@content-desc="tab_fast_trade"]'
    
    def footer_earn_button(): 
        """footer 위치에 earn 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="Earn"]'
        return '//*[@content-desc="tab_earn"]'
    
    def footer_assets_button():
        """footer 위치에 assets 버튼"""
        if get_device_type() == "ios":
            return '//XCUIElementTypeStaticText[@name="Assets"]'
        return '//*[@content-desc="tab_assets"]'

class BaseTestSteps:
    """
    공통으로 사용할 수 있는 기능 정의.
    """
    def move_to_account():
        """
        메인 화면에서 account 페이지 이동
        """
        from src.pages.account_page_a import AccountElements
        from src.pages.base_page_a import BaseTestSteps
        teststep_description = "헤더 영역에 있는 account 버튼 클릭하여 페이지 이동"
        try:
            BaseTestSteps.move_to_footer("Market")
            if Element(BaseElements.header_account_button()).isVisible(3, False) == False:
                Element(BaseElements.header_back_button()).click()
            Element(BaseElements.header_account_button()).click()
            Element(AccountElements.title_account_text()).isVisible()
        except Exception as error:
            raise Exception(f"[ERROR] {teststep_description}\n{error}")

    def move_to_footer(footer_name:str):
        """
        메인 화면 푸터 이동

        Args:
            footer_name(str) : footer 버튼 이름 입력 (Market, Challenge, Trade, Earn, Assets)
        """
        teststep_description = "헤더 영역에 있는 account 버튼 클릭하여 페이지 이동"
        try:
            match footer_name:
                case "Market":
                    footer_element = BaseElements.footer_market_button()
                case "Challenge":
                    footer_element = BaseElements.footer_challenge_button()
                case "Trade":
                    footer_element = BaseElements.footer_trade_button()
                case "Earn":
                    footer_element = BaseElements.footer_earn_button()
                case "Assets":
                    footer_element = BaseElements.footer_assets_button()
                case _:
                    raise ValueError(f"Invalid footer name: {footer_name}")

            if Element(footer_element).isVisible(3, False) == False:
                Element(BaseElements.header_back_button()).click()
            Element(footer_element).click()
        except Exception as error:
            raise Exception(f"[ERROR] {teststep_description}\n{error}")