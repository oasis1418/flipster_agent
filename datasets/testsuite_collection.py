from src.testcases.abstract_common_testcase import AbstractTestCase
import src.testcases.account_testcase as ACCOUNT
import src.testcases.assets_testcase as ASSETS
import src.testcases.market_testcase as MARKET
import src.testcases.challenge_testcase as CHALLENGE

"""
    테스트 스윗 정의
    - 테스트 스윗 대상과 수행에 포함되어 있는 테스트 케이스들을 작성한다.
    - 수행 명령어에 옵션값으로 입력한 -suit "suit 명" 으로 원하는 suit 선택하여 실행 시킬 수 있다.
    
    Example:
        suit_list(dict)에 suit에 수행 할 테스트 케이스 리스트 등록 ("suit 명": [ testcase 명, AbstractTestCase 클래스])
        - suit 명칭 : 자유롭게 사용 가능 (중복 불가)
        - testcase 명칭 : 테스트 케이스 클래스 이름 사용.
        - AbstractTestCase 클래스 : src/testcases/ 에 AbstractTestCase 클래스.

    ToDo:
        추후에 API 구현 할 경우 아래 suit_list 데이터 호출로 실시간 테스트 수행 할 수 있도록 확장 가능.
"""
suit_list: dict[str, list[dict[str, AbstractTestCase]]] = {
    "account_test": [
        {"testcase": "로그 아웃 확인", "class": ACCOUNT.TestCaseCheckLogout()},
        {"testcase": "로그 인 확인", "class": ASSETS.TestCaseCheckLogin()},
        {"testcase": "문의하기 챗봇 페이지 노출 및 앱 전환 확인", "class": ACCOUNT.TestCaseCheckChatbotPageTransition()},
    ],
    "market_test": [
        {"testcase": "High volume 코인 정보 확인", "class": MARKET.TestCaseCheckHighVolumeCoinInfo()},
    ],
    "challenge_test": [
        {"testcase": "Challenge 이벤트 정보 확인", "class": CHALLENGE.TestCaseCheckChallengeEventInfo()},
    ],
    "flipster_total_test": [
        {"testcase": "로그 아웃 확인", "class": ACCOUNT.TestCaseCheckLogout()},
        {"testcase": "로그 인 확인", "class": ASSETS.TestCaseCheckLogin()},
        {"testcase": "High volume 코인 정보 확인", "class": MARKET.TestCaseCheckHighVolumeCoinInfo()},
        {"testcase": "Challenge 이벤트 정보 확인", "class": CHALLENGE.TestCaseCheckChallengeEventInfo()},
        {"testcase": "문의하기 챗봇 페이지 노출 및 앱 전환 확인", "class": ACCOUNT.TestCaseCheckChatbotPageTransition()},
    ],
}

