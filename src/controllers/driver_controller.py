from appium import webdriver
from settings.logger_config import logger
import os
import shutil
import json
import chromedriver_autoinstaller
from datasets.base_capabilites import get_and_capability, get_ios_capability
from src.reports.report import send_result
from src.controllers.device_controller import get_device_type

global driver

class Remote:
    """
    드라이버 리모트 수행을 위한 클래스.

    Attributes:
        device_info (dict): 테스트 단말 정보

    Methods:
        set_device_info(device_info): 단말 정보 설정
        run_device_remote(): 드라이버 리모트 수행
        context_switch(context_name) : 하이브리드 앱 context 전환 수행
        start_activity(app_name, app_intro): 앱 실행 (app activity 로 바로 이동)
        activate_app(app_name): 앱 실행 (백그라운드에 실행되어 있는 앱 실행)
        close_app(): 앱 종료 (앱을 백그라운드로 종료하고 다시 실행상태 유지)
        terminate_app(app_name): 앱 종료 (앱을 메모리에서 완전히 종료)
        get_context(): 현재 context 값 반환
        get_currentPackage(): 현재 앱 package 값 반환
        get_currentActivity(): 현재 앱 activity 값 반환
        press_keycode(key_type): 안드로이드 하드웨어 키 입력
    """

    def __init__(self):
        self.device_info = {}
        self.remove_screenshot_dir = True

    def set_device_info(self, device_info):
        self.device_info = device_info

    def run_device_remote(self):
        """
        테스트 단말 리모트 실행
        """
        try:
            global driver
            logger.info(f"[RUNNING] Remote device info : {self.device_info}")
            if self.device_info["device_type"] == "ios":
                option_capability = get_ios_capability()
            else:
                option_capability = get_and_capability()
            # 테스트 단말 uuid 설정
            option_capability.udid = self.device_info["device_uuid"]
            # 드라이버 리모트 수행
            remote_address = f"http://127.0.0.1:{self.device_info['appium_port']}"
            logger.info(f"[RUNNING] Remote Driver Address    : {remote_address}")
            driver = webdriver.Remote(remote_address, options=option_capability)
        except Exception as error:
            logger.info(f"[ERROR] Remote Error : {error}")

    def context_switch(self, context_name: str):
        """
        하이브리드 앱 context switch 수행 (native / webview 전환)

        Args:
            context_name (str): NATIVE_APP, WEBVIEW
        """
        logger.info(f"[RUNNING] Context switch : {driver.contexts} ({context_name})")
        logger.info(f"[RUNNING] Context before : {driver.context}")
        driver.switch_to.context(context_name)
        logger.info(f"[RUNNING] Context after  : {driver.context}")

    def screenshot(self, file_name: str):
        path_screenshot = os.getcwd() + "/report/screenshot/"
        file_name_screenshot = self.device_info["device_name"] + "-" + file_name + ".png"
        save_file_fullname = path_screenshot + file_name_screenshot
        logger.info(f"[RUNNING] Save ScreenShot : {file_name}")
        if self.remove_screenshot_dir and os.path.exists(path_screenshot):
            shutil.rmtree(path_screenshot)
        if os.path.exists(path_screenshot) == False:
            os.makedirs(path_screenshot)
        driver.save_screenshot(save_file_fullname)
        self.remove_screenshot_dir = False

    def start_activity(self, app_package:str=None, app_activity:str=None):
        """
        앱 activity 로 바로 실행
        
        Args:
            app_package (str): 앱 패키지 명
            app_activity (str): 앱 activity 명
        """
        if app_package == None:
            if self.device_info["device_type"] == "android":
                capability = get_and_capability()
                app_package = capability.app_package
                app_activity = capability.app_activity
                driver.start_activity(app_package, app_activity)
                send_result("teststep", "[Start Activity App] 앱 실행", f"[Android] 앱 실행 ({app_package}, {app_activity})", "pass")
            else:
                capability = get_ios_capability()
                app_bundle_id = capability.bundle_id
                driver.activate_app(app_bundle_id)
                send_result("teststep", "[Start Activity App] 앱 실행", f"[iOS] 앱 실행 ({app_bundle_id})", "pass")

    def activate_app(self, app_package:str=None):
        """
        앱 실행 (백그라운드에 있는 앱 실행)
        
        Args:
            app_package (str): 앱 패키지 명
        """
        if app_package == None:
            capability = get_and_capability()
            app_package = capability.app_package
        driver.activate_app(app_package)
        send_result("teststep", "[Active App] 앱 실행", f"앱 실행 ({app_package})", "pass")

    def close_app(self):
        """
        앱 종료 (백그라운드에 종료)
        """
        driver.close_app
        send_result("teststep", "[Close App] 앱 종료", f"앱 백그라운드 종료", "pass")


    def terminate_app(self, app_package:str=None):
        """
        앱 종료 (앱 메모리에 완전히 종료)
                
        Args:
            app_package (str): 앱 패키지 명
        """
        if app_package == None:
            if self.device_info["device_type"] == "android":
                capability = get_and_capability()
                app_package = capability.app_package
            else:
                capability = get_ios_capability()
                app_package = capability.bundle_id
        driver.terminate_app(app_package)
        send_result("teststep", "[Terminate App] 앱 종료", f"앱 종료 ({app_package})", "pass")

    def get_context(self):
        """
        현재 context 값 반환
        
        Retruns:
            contexts(List) : 현재 앱 context 전체 리스트 반환
        """
        contexts = driver.contexts
        return contexts

    def get_currentPackage(self):
        """
        현재 package 값 반환
        
        Retruns:
            package(str) : 현재 package 값 반환
        """
        package = driver.current_package
        return package

    def get_currentActivity(self):
        """
        현재 activity 값 반환
        
        Retruns:
            activity(str) : 현재 activity 값 반환
        """
        activity = driver.current_activity
        return activity

    def press_keycode(self, key_type):
        """
        안드로이드 단말 하드키 누르기
        Args:
            key_type (int): enter, back
        Retruns:
            None
        """
        if key_type == "enter":
            driver.press_keycode(66)
        if key_type == "back":
            driver.press_keycode(4)

remote = Remote()
