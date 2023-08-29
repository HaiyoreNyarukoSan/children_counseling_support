# Permission 등록 방법

## shell 실행

> python manage.py shell

## 코드 입력

> from users.permissions import set_permission\
> set_permission()

# Chatting 실행 방법

## Channels와 Daphne 설치

> python -m pip install -U channels["daphne"]

## Docker 실행

> docker run --rm -p 6379:6379 redis:7