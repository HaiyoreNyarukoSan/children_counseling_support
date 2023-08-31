# Permission 등록 방법

1. shell 실행

> python manage.py shell

2. Python shell에 코드 입력

> from users.permissions import set_permission\
> set_permission()

# Chatting 실행 방법

## Channels와 Daphne 설치

> python -m pip install -U channels["daphne"]

## Docker 실행

> docker run --rm -p 6379:6379 redis:7

# YOLO 설치 방법

1. YOLO 모듈을 다운 받을 페이지로 이동
2. GitHub에서 모듈 다운 받기

> git clone https://github.com/ultralytics/ultralytics.git

3. ultralytics 폴더로 이동하기

> cd ./ultralytics

4. 설치하기

> pip install -e . 