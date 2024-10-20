import json
import time
import src.controllers.driver_controller as DC
from src.controllers.element_controller import Element
from settings.logger_config import logger
from src.reports.report import send_result
from src.controllers.device_controller import get_device_type

class MarketElements:
    """
    Market 페이지에서 사용하는 엘리먼트 정의.
    """
    def new_listings_see_all_button():
        """Market 페이지에 New listings 영역에 See all 버튼"""
        if get_device_type() == "ios":
            return '(//*[@value="New listings"]/following-sibling::*[@label="See all"])[1]'
        return '(//*[@text="New listings"]/following-sibling::*[@text="See all"])[1]'

    def top_movers_see_all_button():
        """Market 페이지에 Top movers 영역에 See all 버튼"""
        if get_device_type() == "ios":
            return '(//*[@value="Top movers"]/following-sibling::*[@label="See all"])[1]'
        return '(//*[@text="Top movers"]/following-sibling::*[@text="See all"])[1]'

    def your_frequent_trades_see_all_button():
        """Market 페이지에 Your frequent trades 영역에 See all 버튼"""
        if get_device_type() == "ios":
            return '(//*[@value="Your frequent trades"]/following-sibling::*[@label="See all"])[1]'
        return '(//*[@text="Your frequent trades"]/following-sibling::*[@text="See all"])[1]'

    def high_volume_see_all_button():
        """Market 페이지에 Your frequent trades 영역에 See all 버튼"""
        if get_device_type() == "ios":
            return '(//*[@value="High volume"]/following-sibling::*[@label="See all"])[1]'
        return '(//*[@text="High volume"]/following-sibling::*[@text="See all"])[1]'

    def high_funding_rates_see_all_button():
        """Market 페이지에 Your frequent trades 영역에 See all 버튼"""
        if get_device_type() == "ios":
            return '(//*[@value="High funding rates"]/following-sibling::*[@label="See all"])[1]'
        return '(//*[@text="High funding rates"]/following-sibling::*[@text="See all"])[1]'

class MarketTestSteps:
    """
    Market 사용할 수 있는 기능 정의.
    """
    def check_high_volume_coin_info():
        """
        High Volume 영역에 코인 정보 확인
        """
        teststep_description = "High Volume 페이지 이동하여 코인 정보 정상 확인"
        try:
            Element(MarketElements.high_volume_see_all_button()).element_swipe("down")
            Element(MarketElements.high_volume_see_all_button()).click()
            time.sleep(1)
            coin_infos = []
            for i in range(3):
                if get_device_type() == "ios":
                    coin_info_views = Element('//*[contains(@name, "ticker") and contains(@name, "price") and contains(@name, "fluctuation")]').find()
                else:
                    coin_info_views = Element('//*[contains(@content-desc, "ticker")]/..').find()
                for j in range(len(coin_info_views) - 1):
                    if get_device_type() == "ios":
                        coin_info = {
                            'ticker' : coin_info_views[j].find_element('xpath','//XCUIElementTypeStaticText[@index=1]').text,
                            'volume' : coin_info_views[j].find_element('xpath','//XCUIElementTypeStaticText[@index=3]').text,
                            'price' : coin_info_views[j].find_element('xpath','//XCUIElementTypeStaticText[@index=4]').text,
                            'fluctuation' : coin_info_views[j].find_element('xpath','//XCUIElementTypeStaticText[@index=6]').text,
                        }
                    else:
                        coin_info = {
                            'ticker' : coin_info_views[j].find_element('xpath','//*[contains(@content-desc, "ticker")]').text,
                            'volume' : coin_info_views[j].find_element('xpath','//android.widget.TextView[@index=3]').text,
                            'price' : coin_info_views[j].find_element('xpath','//*[contains(@content-desc, "price")]').text,
                            'fluctuation' : coin_info_views[j].find_element('xpath','//*[contains(@content-desc, "fluctuation")]').text,
                        }
                    coin_infos.append(coin_info)
                    # 코인 정보 정상 노출 확인
                    if any(coin_info[key] is None for key in ['ticker', 'volume', 'price', 'fluctuation']):
                        raise Exception(f"[FAIL] {teststep_description} 케이스 실패")
                if i < 2:
                    if get_device_type() == "ios":
                        Element('//*[contains(@name, "ticker") and contains(@name, "price") and contains(@name, "fluctuation")]').coordinates_swipe(200, 750, 200, 200)
                    else:
                        Element('//*[contains(@content-desc, "ticker")]/..').coordinates_swipe(500, 1900, 500, 500)
            # 중복 제거 후 20개만 추출
            coin_infos = list({item['ticker']: item for item in coin_infos}.values())[:20]
            send_result("teststep", "High Volume 페이지 코인 정보 정상 확인", f"정상 확인 한 코인 정보 : {json.dumps(coin_infos, indent=4)}", "pass")
        except Exception as error:
            send_result("teststep", "High Volume 페이지 코인 정보 에러", f"에러 발생 코인 정보 : {json.dumps(coin_infos, indent=4)} \n Error Message : {error}", "fail")
            raise Exception(f"[ERROR] {teststep_description}\nError Message : {error}")
    