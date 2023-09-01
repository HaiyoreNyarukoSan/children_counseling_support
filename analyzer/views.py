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

aggression = '공격성'
anxiety = '불안감'
dependency = '의존성'
stress = '스트레스'
timidity = '소심함'
sociability = '사회성'
depression = '우울감'
independence = '독립성'
achievement = '성취감'
selfish = '이기적인'

stat_type = (aggression, anxiety, dependency, stress, timidity, sociability, depression, independence, achievement,
             selfish)


def get_wh(box):
    _, _, w, h = map(int, box.xyxy[0])
    return w, h


def get_area(box):
    w, h = get_wh(box)
    return w * h


def get_xyxys(boxes):
    return map(lambda box: tuple(map(int, box.xyxy[0])), boxes)


def get_whs(boxes):
    return map(lambda box: tuple(map(int, box.xywh[0]))[2:], boxes)


def get_areas(boxes):
    whs = get_whs(boxes)
    return map(lambda wh: wh[0] * wh[1], whs)


def xyxy_in_xyxy(window_xyxy, roof_xyxy):
    windows_x1, windows_y1, windows_x2, windows_y2 = window_xyxy  # =(0,0,1,1)
    roof_x1, roof_y1, roof_x2, roof_y2 = roof_xyxy
    return windows_x1 >= roof_x1 and windows_y1 >= roof_y1 and windows_x2 <= roof_x2 and windows_y2 <= roof_x2


# 지붕이 여러개라면 어떻게 하지?
def xyxy_in_xyxys(window_xyxy, roofs_xyxy):
    for roof_xyxy in roofs_xyxy:
        if xyxy_in_xyxy(window_xyxy, roof_xyxy):
            return True
    return False


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
        dependency: 0,
        anxiety: 0,
        timidity: 0,
        selfish: 0,
        aggression: 0,
        independence: 0,
    }

    if len(necks) > 50:
        stat[timidity] += 30

    if sum(get_area(box) for box in shoulders) > 50:
        stat[selfish] += 60

    if sum(get_wh(box)[1] for box in bodys) > 50:
        stat[selfish] += 10

    if sum(get_wh(box)[0] for box in bodys) > 50:
        stat[selfish] += 10

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in chests) > 50:
        stat[anxiety] += 20

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in arms) > 50:
        stat[aggression] += 30
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in arms) < 50:
        stat[timidity] += 40
    else:
        stat[anxiety] += 20

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in hands) > 50:
        stat[selfish] += 10
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in hands) < 50:
        stat[timidity] += 30
    else:
        stat[anxiety] += 10

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in legs) > 50:
        stat[anxiety] += 50
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in legs) < 50:
        stat[timidity] += 20

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in foots) > 50:
        stat[independence] += 20
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in foots) < 50:
        stat[anxiety] += 10
    else:
        stat[selfish] += 30

    if sum(get_wh(box)[0] * get_wh(box)[1] for box in shoes) > 50:
        stat[dependency] += 40
    elif sum(get_wh(box)[0] * get_wh(box)[1] for box in shoes) < 50:
        stat[timidity] += 10
    else:
        stat[selfish] += 10

    return stat


def woman_stat(boxes, labels):
    return person_stat(boxes, labels)


def man_stat(boxes, labels):
    return person_stat(boxes, labels)


def tree_stat(boxes, labels):
    stat = {
        dependency: 0,
        depression: 0,
        anxiety: 0,
        sociability: 0,
    }

    root_count = len([box for box in boxes if labels[int(box.cls)] == '뿌리'])
    branch_count = len([box for box in boxes if labels[int(box.cls)] == '가지'])
    leaves = [box for box in boxes if labels[int(box.cls)] == '나뭇잎']
    cloud_count = len([box for box in boxes if labels[int(box.cls)] == '구름'])

    if root_count == 0 >= 50:
        stat[anxiety] += 20

    if not root_count:
        stat[anxiety] += 20

    if branch_count == 0:
        stat[depression] += 30

    if leaves:
        stat[sociability] += 50

    if cloud_count > 0:
        stat[dependency] += 60

    if len(leaves) > branch_count:
        stat[anxiety] += 20

    return stat


def house_stat(boxes, labels):
    stat = {
        depression: 0,
        dependency: 0,
        sociability: 0,
        selfish: 0,
        anxiety: 0,
        timidity: 0
    }

    door_area = [box for box in boxes if labels[int(box.cls)] == '문']
    door_count = len(door_area)

    roofs = [box for box in boxes if labels[int(box.cls)] == '창문']
    roofs_xyxy = list(get_xyxys(roofs))

    windows = [box for box in boxes if labels[int(box.cls)] == '지붕']
    windows_xyxy = list(get_xyxys(windows))
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
        stat[depression] += 20

    # 문의 넓이가 전체 이미지의 넓이의 50% 이상인지 확인
    if sum(get_areas(door_area)) >= 50:
        stat[dependency] += 30
    else:
        stat[sociability] += 30

    if window_count == sum(1 for box in boxes if labels[int(box.cls)] == '창문'):
        stat[selfish] += 10
    elif window_count > 0 and door_count == 0:
        stat[dependency] += 40
    elif window_count == 0 and door_count == 0:
        stat[sociability] += 20

    # 창문이 지붕 안에 있을 경우
    window_in_roof = [xyxy_in_xyxys(window_xyxy, roofs_xyxy) for window_xyxy in windows_xyxy]
    stat[selfish] += 10 * sum(window_in_roof) / len(window_in_roof)

    # 창문과 문이 없는 경우
    if window_count == 0 and door_count == 0:
        stat[sociability] += 50

    # 굴똑에연기
    smokes_xyxy = get_xyxys(smokes)
    chimneys_xyxy = get_xyxys(chimneys)

    # 굴뚝에 연기가 나는 경우
    for smoke_x1, smoke_y1, smoke_x2, smoke_y2 in smokes_xyxy:
        for chimney_x1, chimney_y1, chimney_x2, chimney_y2 in chimneys_xyxy:
            if smoke_x1 >= chimney_x1 and smoke_y1 >= chimney_y1:
                stat[anxiety] += 20

    # w, h = x2 - x1, y2 - y1
    houses_xyxy = [house.xyxy[0] for house in houses]
    [tuple(map(int, house.xyxy[0])) for house in houses]
    list(map(lambda houses: tuple(map(int, houses.xyxy[0])), houses))
    # 지붕을 너무 크게 그렸다면

    counter = 0
    for roof_w, roof_h in get_whs(roofs):
        for house_w, house_h in get_whs(houses):
            if roof_w >= 50 * house_w and roof_h >= 50 * house_h:
                counter += 1
    stat[depression] += 50 * counter // (len(roofs_xyxy) * len(houses_xyxy))

    # 태양, 나무, 꽃, 잔디 있는 경우
    if any(label in labels for label in ['태양', '나무', '꽃', '잔디']):
        stat[dependency] += 30

    # 길 있는 경우
    if path_count > 0:
        stat[sociability] += 60

    # 울타리, 산 있는 경우
    if mountain_count > 0:
        stat[timidity] += 10

    return stat


def stat_evaluater(bd):
    total_score = dict()

    category_scores = []
    DATA_CATEGORY = ['나무', '남자사람', '여자사람', '집']
    stats = {'나무': tree_stat, '남자사람': man_stat, '여자사람': woman_stat, '집': house_stat}
    for category in DATA_CATEGORY:
        box, label = bd[category], LABELS[category]
        category_scores.append(stats[category](box, label))
    for stat in stat_type:
        total_score[stat] = sum(category_score.get(stat, 0) for category_score in category_scores)

    # house_boxes = bd['집']
    # house_score = house_stat(house_boxes, LABELS['집'])
    #
    # tree_boxes = bd['나무']
    # tree_score = tree_stat(tree_boxes, LABELS['나무'])
    #
    # woman_boxes = bd['여자사람']
    # woman_score = woman_stat(woman_boxes, LABELS['여자사람'])
    #
    # man_boxes = bd['남자사람']
    # man_score = man_stat(man_boxes, LABELS['남자사람'])
    #
    # for stat in stat_type:
    #     total_score[stat] = (house_score.get(stat, 0) + woman_score.get(stat, 0)
    #                          + man_score.get(stat, 0) + tree_score.get(stat, 0))
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
