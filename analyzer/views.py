from typing import Tuple

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
IMAGE_SIZE = 1280
image_area = IMAGE_SIZE * IMAGE_SIZE

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


class BoxData:
    def __int__(self, boxes, labels, target):
        if isinstance(target, str):
            index = labels.index(target)
            self._boxes = [box for box in boxes if int(box.cls) == index]
        else:
            indices = [labels.index(t) for t in target]
            self._boxes = [box for box in boxes if int(box.cls) in indices]
        self._count = len(self._boxes)
        self._xyxys = get_xyxys(self._boxes)
        self._whs = get_whs(self._boxes)

    @property
    def count(self):
        return self._count

    @property
    def xyxys(self):
        return self._xyxys

    @property
    def whs(self):
        return self._whs

    @property
    def area_sum(self):
        return sum(wh[0] * wh[1] for wh in self._whs)

    @property
    def xmin_ave(self):
        return sum(xyxy[0] for xyxy in self._xyxys) / self._count

    @property
    def ymin_ave(self):
        return sum(xyxy[1] for xyxy in self._xyxys) / self._count

    @property
    def xmax_ave(self):
        return sum(xyxy[2] for xyxy in self._xyxys) / self._count

    @property
    def ymax_ave(self):
        return sum(xyxy[3] for xyxy in self._xyxys) / self._count

    @property
    def w_sum(self):
        return sum(wh[0] for wh in self._whs)

    @property
    def h_sum(self):
        return sum(wh[1] for wh in self._whs)

    def ratio_of_is_inside(self, boxdata):
        return xyxys_in_xyxys(self._xyxys, boxdata.xyxys, (('xy', 'in'),)) / len(self._xyxys)

    def ratio_of_is_above(self, boxdata):
        return xyxys_in_xyxys(self._xyxys, boxdata.xyxys, (('x', 'in'), ('y', 'lt'))) / len(self._xyxys)


def xyxy_in_xyxy(window_xyxy, roof_xyxy, target):
    windows_x1, windows_y1, windows_x2, windows_y2 = window_xyxy
    roof_x1, roof_y1, roof_x2, roof_y2 = roof_xyxy
    r1 = ('x' not in target) or (windows_x1 >= roof_x1 and windows_x2 <= roof_x2)
    r2 = ('y' not in target) or (windows_y1 >= roof_y1 and windows_y2 <= roof_y2)
    return int(r1 and r2)


def xyxy_lt_xyxy(window_xyxy, roof_xyxy, target):
    windows_x1, windows_y1, windows_x2, windows_y2 = window_xyxy
    roof_x1, roof_y1, roof_x2, roof_y2 = roof_xyxy
    r1 = ('x' not in target) or (windows_x2 < roof_x1)
    r2 = ('y' not in target) or (windows_y2 < roof_y1)
    return int(r1 and r2)


def xyxy_gt_xyxy(window_xyxy, roof_xyxy, target):
    windows_x1, windows_y1, windows_x2, windows_y2 = window_xyxy
    roof_x1, roof_y1, roof_x2, roof_y2 = roof_xyxy
    r1 = ('x' not in target) or (windows_x2 > roof_x1)
    r2 = ('y' not in target) or (windows_y2 > roof_y1)
    return int(r1 and r2)


def xyxy_within_xyxy(window_xyxy, roof_xyxy, target):
    windows_x1, windows_y1, windows_x2, windows_y2 = window_xyxy
    roof_x1, roof_y1, roof_x2, roof_y2 = roof_xyxy
    r1 = ('x' not in target) or (windows_x1 >= roof_x1 and windows_x2 <= roof_x2)
    r2 = ('y' not in target) or (windows_y1 >= roof_y1 and windows_y2 <= roof_y2)
    return int(r1 and r2)


def xyxy_in_xyxys(window_xyxy, roofs_xyxy, options: Tuple[Tuple[str, str]]):
    for roof_xyxy in roofs_xyxy:
        res = 1
        for option in options:
            operation, target = option
            op = operation if operation in ('in', 'lt', 'gt') else 'in'
            func = {'in': xyxy_in_xyxy, 'lt': xyxy_lt_xyxy, 'gt': xyxy_gt_xyxy}[op]
            if not func(window_xyxy, roof_xyxy, target):
                res = 0
                break
        if res: return 1
    return 0


def xyxys_in_xyxys(windows_xyxy, roofs_xyxy, options: Tuple[Tuple[str, str]]):
    return sum(xyxy_in_xyxys(window_xyxy, roofs_xyxy, options) for window_xyxy in windows_xyxy)


def w_sum(boxes):
    return sum(get_wh(box)[0] for box in boxes)


def h_sum(boxes):
    return sum(get_wh(box)[1] for box in boxes)


def area_sum(boxes):
    return sum(get_areas(boxes))


def change_score(stat, if_change, elif_change=None, else_change=None):
    if if_change:
        condition, stype, svalue = if_change
        stat[stype] += svalue
    elif elif_change:
        condition, stype, svalue = elif_change
        if condition:
            stat[stype] += svalue
    elif else_change:
        stype, svalue = else_change
        stat[stype] += svalue


def person_stat(boxes, labels):
    necks = BoxData(boxes, labels, '목')
    shoulders = BoxData(boxes, labels, '어깨')
    bodys = BoxData(boxes, labels, '사람전체')
    chests = BoxData(boxes, labels, '상체')
    arms = BoxData(boxes, labels, '팔')
    hands = BoxData(boxes, labels, '손')
    legs = BoxData(boxes, labels, '다리')
    foots = BoxData(boxes, labels, '발')
    shoes = BoxData(boxes, labels, ('운동화', '남자구두', '여자구두'))

    stat = {
        dependency: 0,
        anxiety: 0,
        timidity: 0,
        selfish: 0,
        aggression: 0,
        independence: 0,
    }

    # 목이 너무 길면 -> 자신의 행동조절에 대한 자신감 부족
    change_score(stat, (necks.h_sum + necks.w_sum > 50, timidity, 20))
    # 어깨가 너무 크면 -> 책임감이 강하고 과도하게 권위를 내세우고자 하는 태도
    change_score(stat, (shoulders.area_sum > 0.1 * image_area, selfish, 10))
    change_score(stat, (bodys.w_sum > 50, selfish, 20))
    change_score(stat, (bodys.h_sum > 50, selfish, 20))
    change_score(stat, (chests.area_sum > 50, anxiety, 20))
    change_score(stat,
                 (arms.area_sum > 50, aggression, 30),
                 else_change=(anxiety, 20))
    change_score(stat,
                 (hands.area_sum > 50, selfish, 10),
                 (hands.area_sum < 50, timidity, 20),
                 (anxiety, 10))
    change_score(stat,
                 (legs.area_sum > 50, anxiety, 50),
                 (legs.area_sum < 50, timidity, 20))
    change_score(stat,
                 (foots.area_sum > 50, independence, 20),
                 (foots.area_sum < 50, anxiety, 10),
                 (selfish, 20))
    change_score(stat,
                 (shoes.area_sum > 50, dependency, 40),
                 (area_sum(shoes) < 50, timidity, 20),
                 (selfish, 20))

    return stat


def woman_stat(boxes, labels):
    return person_stat(boxes, labels)


def man_stat(boxes, labels):
    return person_stat(boxes, labels)


def tree_stat(boxes, labels):
    roots = BoxData(boxes, labels, '뿌리')
    branchs = BoxData(boxes, labels, '가지')
    leaves = BoxData(boxes, labels, '나뭇잎')
    clouds = BoxData(boxes, labels, '구름')

    stat = {
        dependency: 0,
        depression: 0,
        anxiety: 0,
        sociability: 0,
    }

    change_score(stat, (roots.count > 50, anxiety, 20), else_change=(anxiety, 20))
    change_score(stat, (branchs.count == 0, depression, 30))
    change_score(stat, (leaves.count > 0, sociability, 50))
    change_score(stat, (clouds.count > 0, dependency, 60))
    change_score(stat, (leaves.count > branchs.count, anxiety, 20))

    return stat


def house_stat(boxes, labels):
    doors = BoxData(boxes, labels, '문')
    roofs = BoxData(boxes, labels, '지붕')
    windows = BoxData(boxes, labels, '창문')
    smokes = BoxData(boxes, labels, '연기')
    chimneys = BoxData(boxes, labels, '굴뚝')
    houses = BoxData(boxes, labels, '집전체')
    roads = BoxData(boxes, labels, '길')
    mountains = BoxData(boxes, labels, '산')
    walls = BoxData(boxes, labels, '집벽')
    fences = BoxData(boxes, labels, '울타리')
    ponds = BoxData(boxes, labels, '연못')
    trees = BoxData(boxes, labels, '나무')
    flowers = BoxData(boxes, labels, '꽃')
    grasses = BoxData(boxes, labels, '잔디')
    suns = BoxData(boxes, labels, '태양')

    stat = {
        depression: 0,
        dependency: 0,
        sociability: 0,
        selfish: 0,
        anxiety: 0,
        timidity: 0
    }

    door_area_threshold = 0.12
    roof_area_threshold = 0.54
    change_score(stat,
                 (doors.area_sum >= door_area_threshold * houses.area_sum, dependency, 30),
                 else_change=(sociability, 30))
    change_score(stat, (doors.count == 0, depression, 20))
    change_score(stat, (windows.count > 0, selfish, 20))
    change_score(stat, (windows.count > 0, dependency, 40))
    change_score(stat, (windows.count == 0 and doors.count == 0, sociability, -20))

    # 창문이 지붕 안에 있을 경우
    windows_ratio_in_roofs = windows.ratio_of_is_inside(roofs)
    change_score(stat, (windows_ratio_in_roofs > 0, selfish, int(20 * windows_ratio_in_roofs)))

    # 굴뚝에 연기가 나는 경우
    change_score(stat, (smokes.count > 0, anxiety, 20))

    # 지붕을 너무 크게 그렸다면
    roofs_ratio_area_houses = roofs.area_sum / houses.area_sum
    change_score(stat, (roofs_ratio_area_houses > roof_area_threshold, anxiety, 20 * roofs_ratio_area_houses))

    # 태양, 나무, 꽃, 잔디 있는 경우
    change_score(stat, (suns.count + trees.count + flowers.count + grasses.count > 0, dependency, 30))

    # 길 있는 경우
    change_score(stat, (roads.count > 0, sociability, 60))

    # 울타리, 산 있는 경우
    change_score(stat, (mountains.count > 0, timidity, 20))

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
