# UI 테스트 자동화

- 테스트 자동화를 수행하기 용도로 사용 됩니다.
- UI 테스트 자동화를 수행하는 Appium 기반의 Platform 입니다.

### Environment

- Python version : 3.13.0
- Poetry version : 1.8.3
- Appium version : 2.0.1
  - uiautomator2 : 3.8.0
  - xcuitest : 7.27.1
- Java version : 17.0.12
- node version : 22.9.0
- npm version : 10.8.3

### Settings

- 단말 설정
  - datasets/device_capabilites.py 파일에 테스트 대상 정보 입력
    - device_type : os 입력 (android, ios)
    - device_name : device 명 입력 (자유롭게 단말 구분 될 수 있도록)
    - device_uuid : 단말 uuid 입력
    - device_version : 단말 os 버전 입력
    - appium_port : Appium Port 입력 (Appium 실행 시 일치하는 port 지정하여 실행, ex. appium -p 4723)

---

### Install

```
# 자바 설치
brew install --cask semeru-jdk-open@17
```

```
# node 설치
brew install node
```

```
# appium 설치
npm install -g appium@next
# uiautomator2 설치
appium driver install uiautomator2
# xcuitest 설치
appium driver install xcuitest
```

```
# 패키지 설치
poetry install
```

### Command

```
poetry run startup -device device_name -suit suit_name
```

### Example

```
poetry run startup -device ios16 -suit flipster_total_test
```

처음 시작 파일 위치 : src/run.py

- device : 테스트 대상 단말 명
- suit : 테스트 스윗 명
