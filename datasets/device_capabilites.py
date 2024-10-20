"""
    테스트를 위해 아래 단말 정보 등록 필요
    - device_type : 단말 타입 (안드로이드 - android, 아이폰 - ios)
    - device_name : 단말 명칭 (자유롭게 가능 - 중복 불가)
    - device_uuid : 단말 uuid (명령어 : adb devices)
    - device_version : 단말 os 버전
    - appium_port : appium 실행 port (명령어 : appium --port 4724 -U 26bab32081217ece)
"""
device_list = [
    {
        "device_type": "android",
        "device_name": "ANDv10",
        "device_uuid": "26bab32081217ece",
        "device_version": "10",
        "appium_port": 4724,
    },
    {
        "device_type": "ios",
        "device_name": "IOSv16",
        "device_uuid": "00008110-001439C00C28201E",
        "device_version": "16.0.1",
        "appium_port": 4723,
    },
]
