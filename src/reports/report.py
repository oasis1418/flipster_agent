import requests
import random
import string
from settings.logger_config import logger


g_result_id:str

def send_result(test_type:str, summary:str, description:str, result:str):
    """
    테스트 결과 전송
    - 테스트 결과 정보 정의 (API 호출하여 DB 저장)

    Args:
        type (str): 결과 타입 지정 (ex. testsuit, testcase, teststep)
            - testsuit : 테스트 스윗 수행하는 공통 함수에서 자동 입력됨.
            - testcase : 테스트 케이스에서 결과 처리 할 경우 testcase 타입 지정
            - teststep : pom 방식에서 pages에서 결과 처리나 이외 함수에서 결과 처리 할 경우 step 타입 지정
        summary (str): 테스트 결과 요약
        description (str): 테스트 결과에 대한 내용 정의
        result (str): 테스트 결과 저장 (pass, fail)
    """
    from src.controllers.testcase_controller import g_device_info, g_testsuit, g_testcase
    try:
        url = "http://127.0.0.1:8092/autotest/auto/test/result/"
        
        result_info = {
            "result_id": g_result_id,
            "device_type": g_device_info["device_type"],
            "device_name": g_device_info["device_name"],
            "device_uuid": g_device_info["device_uuid"],
            "device_version": g_device_info["device_version"],
            # "app_version": g_app_version,
            "testsuit": g_testsuit,
            "testcase": g_testcase,
            "type": test_type,
            "summary": summary,
            "description": description,
            "result": result,
        }
        response = requests.post(url, json=result_info)

        if response.status_code == 201:
            logger.info(f"[Result] 테스트 결과 전송 성공 ({summary}, {description}) - {result}")
        else:
            logger.info(f"[Result] 테스트 결과 전송 실패 (error code : {response.status_code}, )")
    except Exception as error:
        raise Exception(f"[ERROR] 테스트 결과 전송 에러 \n{error}")

def set_result_id():
    """
    테스트 결과 id 생성
    """
    global g_result_id
    random_digits = ''.join(random.choices(string.digits, k=6))
    g_result_id = f"TEST{random_digits}"
    logger.info(f"[Result] set result (result id : {g_result_id})")

    