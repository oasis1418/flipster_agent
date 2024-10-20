
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options

def get_and_capability():
    """
    기본 android capability 정보
    - default 값으로 설정되는 capability 정보.
    """
    and_capability = UiAutomator2Options()
    and_capability.platform_name = "Android"
    and_capability.automation_name = "uiautomator2"
    and_capability.app_package = "com.prestolabs.android.prex"
    and_capability.app_activity = "com.prestolabs.android.prex.presentations.ui.MainActivity"
    and_capability.new_command_timeout = 360000
    and_capability.no_reset = True
    return and_capability

def get_ios_capability():
    """
    기본 ios capability 정보
    - default 값으로 설정되는 capability 정보.
    """
    ios_capability = XCUITestOptions()
    ios_capability.platform_name = "ios"
    ios_capability.automation_name = "XCUITest"
    ios_capability.udid = "00008110-001439C00C28201E"
    ios_capability.bundle_id = "com.aqx.prex"
    ios_capability.wda_connection_timeout = 360000
    ios_capability.new_command_timeout = 120
    ios_capability.safari_ignore_fraud_warning = True
    ios_capability.auto_web_view = True
    return ios_capability

