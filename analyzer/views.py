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


def person_stat(boxes, labels):
    necks = [box for box in boxes if labels[int(box.cls)] == '목']
    shoulders = [box for box in boxes if labels[int(box.cls)] == '어깨']
    bodys = [box for box in boxes if labels[int(box.cls)] == '사람전체']
    chests = [box for box in boxes if labels[int(box.cls)] == '상체']
    arms = [box for box in boxes if labels[int(box.cls)] == '팔']
    hands = [box for box in boxes if labels[int(box.cls)] == '손']
    legs = [box for box in boxes if labels[int(box.cls)] == '다리']
    foots = [box for box in boxes if labels[int(box.cls)] == '발']
    shoes = [box for box in boxes if labels[int(box.cls)] == '발']

    stat = {
        '의존성': 0,
        '불안감': 0,
        '소심함': 0,
        '이기적인': 0,
        '공격성': 0,
        '독립성': 0,
    }

    def get_wh(box):
        _, _, w, h = map(int, box.xyxy[0])
        return w, h

    def get_area(box):
        w, h = get_wh(box)
        return w * h

    if len(necks) > 50:
        stat["소심함"] += 30

    if sum(get_area(box) for box in shoulders) > 50:
        stat["이기적인"] += 60

    if sum(get_wh(box)[1] for box in bodys) > 50:
        stat["이기적인"] += 10

    if sum(get_wh(box)[0] for box in bodys) > 50:
        stat["이기적인"] += 10

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in chests) > 50:
        stat["불안감"] += 20

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in arms) > 50:
        stat["공격성"] += 30
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in arms) < 50:
        stat["소심함"] += 40
    else:
        stat["불안감"] += 20

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in hands) > 50:
        stat["이기적인"] += 10
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in hands) < 50:
        stat["소심함"] += 30
    else:
        stat["불안감"] += 10

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in legs) > 50:
        stat["불안감"] += 50
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in legs) < 50:
        stat["소심함"] += 20

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in foots) > 50:
        stat["독립성"] += 20
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in foots) < 50:
        stat["불안감"] += 10
    else:
        stat["이기적인"] += 30

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in shoes) > 50:
        stat["의존성"] += 40
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in shoes) < 50:
        stat["소심함"] += 10
    else:
        stat["이기적인"] += 10

    return stat


def woman_stat(boxes, labels):
    return person_stat(boxes, labels)


def man_stat(boxes, labels):
    return person_stat(boxes, labels)


def tree_stat(boxes, labels):
    stat = {
        '의존성': 0,
        '우울감': 0,
        '불안감': 0,
        '사회성': 0,
    }

    root_count = len([box for box in boxes if labels[int(box.cls)] == '뿌리'])
    branch_count = len([box for box in boxes if labels[int(box.cls)] == '가지'])
    leaves = [box for box in boxes if labels[int(box.cls)] == '나뭇잎']
    cloud_count = len([box for box in boxes if labels[int(box.cls)] == '구름'])

    if root_count == 0 >= 50:
        stat["불안감"] += 20

    if not root_count:
        stat["불안감"] += 20

    if branch_count == 0:
        stat['우울감'] += 30

    if leaves:
        stat["사회성"] += 50

    if cloud_count > 0:
        stat["의존성"] += 60

    if len(leaves) > branch_count:
        stat['불안감'] += 20

    return stat


def house_stat(boxes, labels):
    stat = {
        '우울감': 0,
        '의존성': 0,
        '사회성': 0,
        '이기적인': 0,
        '불안감': 0,
        '소심함': 0
    }

    door_area = [box for box in boxes if labels[int(box.cls)] == '문']
    door_count = len(door_area)

    roofs = [box for box in boxes if labels[int(box.cls)] == '창문']
    windows = [box for box in boxes if labels[int(box.cls)] == '지붕']
    window_count = len(windows)

    smokes = [box for box in boxes if labels[int(box.cls)] == '굴뚝']
    chimneys = [box for box in boxes if labels[int(box.cls)] == '연기']

    houses = [box for box in boxes if labels[int(box.cls)] == '집전체']

    obj = [box for box in boxes if labels[int(box.cls)] in ['태양', '나무', '꽃', '잔디']]

    paths = [box for box in boxes if labels[int(box.cls)] == '길']
    path_count = len(paths)

    mountain = [box for box in boxes if labels[int(box.cls)] == '산']
    mountain_count = len(mountain)

    # 문이 없는 경우
    if not door_area:
        stat['우울감'] += 20

    # 문의 넓이가 전체 이미지의 넓이의 50% 이상인지 확인
    if sum([box.area for box in door_area]) >= 50:
        stat['의존성'] += 30
    else:
        stat['사회성'] += 30

    if window_count == sum(1 for box in boxes if labels[int(box.cls)] == '창문'):
        stat['이기적인'] += 10
    elif window_count > 0 and door_count == 0:
        stat['의존성'] += 40
    elif window_count == 0 and door_count == 0:
        stat['사회성'] += 20

    [window.xyxy[0] for window in windows]
    roofs_xyxy = [roof.xyxy[0] for roof in roofs]

    [tuple(map(int, window.xyxy[0])) for window in windows]
    [tuple(map(int, roof.xyxy[0])) for roof in roofs]

    list(
        map(
            lambda window: tuple(map(int, window.xyxy[0])),
            windows
        )
    )
    # 줄바꿈 없애보자
    list(map(lambda window: tuple(map(int, window.xyxy[0])), windows))
    list(map(lambda roof: tuple(map(int, roof.xyxy[0])), roofs))

    # list(map(lambda window: tuple(map(int,window.xyxy[0])), windows ))는 너무길어
    # 매번 이걸 입력하면 손가락 아파
    # 함수로 만들어서, 함수 이름으로 편하게 쓸래
    def extractor(boxes):
        return map(lambda box: tuple(map(int, box.xyxy[0])), boxes)

    # 창문이 지붕 안에 있는지 계산하는 것도 함수로 만들자
    def window_in_roof(windows_x1, windows_y1, windows_x2, windows_y2, roof_x1, roof_y1, roof_x2, roof_y2):
        return windows_x1 >= roof_x1 and windows_y1 >= roof_y1 and windows_x2 <= roof_x2 and windows_y2 <= roof_y2

    # 함수를 써서, 창문이 지붕 속에 있는지 알아보자
    [
        window_in_roof(x1, y1, x2, y2, roof_x1, roof_y1, roof_x2, roof_y2)
        for (x1, y1, x2, y2, roof_x1, roof_y1, roof_x2, roof_y2)
        # in map(lambda window: tuple(map(int,window.xyxy[0])), windows )
        in extractor(windows)
    ]
    # 창문이지붕속=[창문1은지붕속,창문2는지붕밖]
    window_roof = [True, False]

    # 심화편
    # x1,y1,x2,y2를 일일히 입력하는 건 힘들어
    # box의 범위를 알려주는 숫자니까, 범위를 하나의 변수로 받으면 안될까?
    def window_in_roof_improvement(window_xyxy, roof_xyxy):
        windows_x1, windows_y1, windows_x2, windows_y2 = window_xyxy  # =(0,0,1,1)
        roof_x1, roof_y1, roof_x2, roof_y2 = roof_xyxy
        return windows_x1 >= roof_x1 and windows_y1 >= roof_y1 and windows_x2 <= roof_x2 and windows_y2 <= roof_x2

    # 지붕이 여러개라면 어떻게 하지?
    def window_in_roof_improvement_roofs(window_xyxy, roofs_xyxy):
        for roof_xyxy in roofs_xyxy:
            if window_in_roof_improvement(window_xyxy, roof_xyxy):
                return True
        return False

    [
        window_in_roof_improvement(window_xyxy, roof_xyxy)
        for window_xyxy, roof_xyxy
        in map(lambda window: tuple(map(int, window.xyxy[0])), windows)
    ]
    stat['이기적인'] += 10 * sum(window_roof) / len(window_roof)

    # 창문과 문이 없는 경우
    if window_count == 0 and door_count == 0:
        stat['사회성'] += 50

    # 굴똑에연기
    smokes_xyxy = [smoke.xyxy[0] for smoke in smokes]
    chimneys_xyxy = [chimney.xyxy[0] for chimney in chimneys]
    [tuple(map(int, smoke.xyxy[0])) for smoke in smokes]
    [tuple(map(int, chimney.xyxy[0])) for chimney in chimneys]

    list(map(lambda smoke: tuple(map(int, smoke.xyxy[0])), smokes))
    list(map(lambda chimney: tuple(map(int, chimney.xyxy[0])), chimneys))

    # 굴뚝에 연기가 나는 경우
    for smoke_x1, smoke_y1, smoke_x2, smoke_y2 in smokes_xyxy:
        for chimney_x1, chimney_y1, chimney_x2, chimney_y2 in chimneys_xyxy:
            if smoke_x1 >= chimney_x1 and smoke_y1 >= chimney_y1:
                stat['불안감'] += 20

    # w, h = x2 - x1, y2 - y1
    houses_xyxy = [house.xyxy[0] for house in houses]
    [tuple(map(int, house.xyxy[0])) for house in houses]
    list(map(lambda houses: tuple(map(int, houses.xyxy[0])), houses))
    # 지붕을 너무 크게 그렸다면

    for roof_x1, roof_y1, roof_x2, roof_y2 in roofs_xyxy:
        for house_x1, house_y1, house_x2, house_y2 in houses_xyxy:
            if roof_x2 - roof_x1 >= 50 * house_x1 - house_x2 and roof_y2 - roof_y1 >= 50 * house_y2 - house_y1:
                stat["우울감"] += 50

    # 태양, 나무, 꽃, 잔디 있는 경우
    if any(label in labels for label in ['태양', '나무', '꽃', '잔디']):
        stat["의존성"] += 30

    # 길 있는 경우
    if path_count > 0:
        stat["사회성"] += 60

    # 울타리, 산 있는 경우
    if mountain_count > 0:
        stat["소심함"] += 10

    return stat


def stat_evaluater(bd):
    # house_boxes = bd['집']
    # house_score = house_stat(house_boxes, LABELS['집'])
    house_boxes = bd['여자사람']
    house_score = house_stat(house_boxes, LABELS['여자사람'])

    tree_boxes = bd['나무']
    tree_score = tree_stat(tree_boxes, LABELS['나무'])

    woman_boxes = bd['여자사람']
    woman_score = woman_stat(woman_boxes, LABELS['여자사람'])

    # man_boxes = bd['남자사람']
    # man_score = man_stat(man_boxes, LABELS['남자사람'])
    man_boxes = bd['여자사람']
    man_score = man_stat(man_boxes, LABELS['여자사람'])

    stat_type = ['공격성', '불안감', '의존성', '스트레스', '소심함', '사회성', '우울감', '독립성', '성취감', '이기적인']
    total_score = dict()
    for stat in stat_type:
        total_score[stat] = (house_score.get(stat, 0) + woman_score.get(stat, 0)
                             + man_score.get(stat, 0) + tree_score.get(stat, 0))
    return total_score


def analyzer(images):
    boxes_dict = dict()
    for category, image in zip(DATA_CATEGORY, images):
        label = LABELS[category]
        model = models[category]
        if not (image and model): continue
        result = model.predict(image.path)[0]
        boxes = result.boxes
        boxes_dict[category] = (boxes)
    total_score = stat_evaluater(boxes_dict)
    return total_score
