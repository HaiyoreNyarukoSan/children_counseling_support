from django.shortcuts import render
from ultralytics import YOLO

from children_counseling_support.settings import STATICFILES_DIRS


# Create your views here.
def fetcher(category):
    model_path = f'model/checkpoint_{category}.pt'
    for static_dir in STATICFILES_DIRS:
        if (fullpath := static_dir / model_path).exists():
            return YOLO(fullpath)


def update(category):
    models[category] = fetcher(category)


DATA_CATEGORY = ['나무', '남자사람', '여자사람', '집']

model_path = STATICFILES_DIRS
models = dict((category, fetcher(category)) for category in DATA_CATEGORY)

LABELS = {
    '나무': ['나무전체', '기둥', '수관', '가지', '뿌리', '나뭇잎', '꽃', '열매', '그네', '새', '다람쥐', '구름', '달', '별'],
    '남자사람': ['사람전체', '머리', '얼굴', '눈', '코', '입', '귀', '머리카락', '목', '상체', '팔', '손', '다리', '발', '단추', '주머니', '운동화',
             '남자구두'],
    '여자사람': ['사람전체', '머리', '얼굴', '눈', '코', '입', '귀', '머리카락', '목', '상체', '팔', '손', '다리', '발', '단추', '주머니', '운동화',
             '여자구두'],
    '집': ['집전체', '지붕', '집벽', '문', '창문', '굴뚝', '연기', '울타리', '길', '연못', '산', '나무', '꽃', '잔디', '태양']
}


def analyzer(images):
    boxes_dict = dict()
    for category, image in zip(DATA_CATEGORY, images):
        label = LABELS[category]
        model = models[category]
        if not (image and model): continue
        result = model.predict(image.path)[0]
        boxes = result.boxes
        boxes_dict[category] = boxes
    # TODO : (가칭)stat_evaluater 함수 만들기
    # * parameter : boxes_dict : category별로 boxes가 들어있는 dict 변수
    # * 반환값 : 심리 상태를 나타내는 Model
    stat_evaluater = lambda bd: bd
    return stat_evaluater(boxes_dict)
