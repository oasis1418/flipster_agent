import argparse

def get_argument(argument: str):
    """
    Test 수행 시 옵션 Argument 값 반환.
    - Test 수행 시 device, suit 을 옵션으로 입력한 값을 반환하는 용도.
    - "poetry run startup -device IOS16 -suit testsuit" 명령어로 옵션 입력시 해당하는 device, suit 으로 수행 가능.

    Args:
        argument (str): Argument option key (device, suit)

    Returns:
        device_name (str) : 테스트 수행 시 옵션으로 입력한 단말 명
        suit_name (str) : 테스트 수행 시 옵션으로 입력한 suit 명

    Example:
        >>> device_name = get_argument("device_name") : 수행 시 입력한 device name 반환.
    """
    parser = argparse.ArgumentParser(description="테스트 수행 argument")
    parser.add_argument("-device", "--arg1")  # device_name
    parser.add_argument("-suit", "--arg2")  # suit_name

    if argument == "device_name":
        return parser.parse_args().arg1
    if argument == "suit_name":
        return parser.parse_args().arg2
