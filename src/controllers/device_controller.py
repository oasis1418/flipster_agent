from settings.logger_config import logger
from datasets.device_capabilites import device_list

g_device_info: dict[str, any]

def get_device_info(device_name: str):
    """
    단말 정보 반환
    - datasets/device_capabilites.py 에 저장되어 있는 단말 정보 반환.

    Args:
        device_name (str): 테스트 대상 단말 명 입력.

    Returns:
        device_info (dict) : 테스트 대상 단말 정보 반환.

    Example:
        >>> device_info = get_device_info("device_name") : 테스트 단말 정보 반환.
    """
    try:
        global g_device_info
        for i in range(len(device_list)):
            if device_list[i]["device_name"] == device_name:
                g_device_info = device_list[i]
                return device_list[i]
        raise Exception(f"[ERROR] Device Not Found - {device_name}")
    except Exception as error:
        raise Exception(f"[ERROR] Device Not Found - {device_name}\n{error}")

def get_device_type():
    return g_device_info['device_type']