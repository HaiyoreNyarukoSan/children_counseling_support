from pathlib import Path
from typing import Tuple, List, Union

import ultralytics.engine.results
from django.shortcuts import render
import numpy as np
from ultralytics import YOLO

from analyzer.evaluator import ModelEvaluator
from analyzer.legacy_evaluator import FunctionEvaluator
from analyzer.utils import find_static_file, fetch_pickle
from children_counseling_support.settings import STATICFILES_DIRS

BoundingBoxType = ultralytics.engine.results.Boxes
YOLOResultType = ultralytics.engine.results.Results
MAX_SCORE = 10

DATA_CATEGORY = ['나무', '남자사람', '여자사람', '집']
LABELS = {
    '나무': ['나무전체', '기둥', '수관', '가지', '뿌리', '나뭇잎', '꽃', '열매', '그네', '새', '다람쥐', '구름', '달', '별'],
    '남자사람': ['사람전체', '머리', '얼굴', '눈', '코', '입', '귀', '머리카락', '목', '상체', '팔', '손', '다리', '발', '단추', '주머니', '운동화',
             '남자구두'],
    '여자사람': ['사람전체', '머리', '얼굴', '눈', '코', '입', '귀', '머리카락', '목', '상체', '팔', '손', '다리', '발', '단추', '주머니', '운동화',
             '여자구두'],
    '집': ['집전체', '지붕', '집벽', '문', '창문', '굴뚝', '연기', '울타리', '길', '연못', '산', '나무', '꽃', '잔디', '태양']
}

agreeableness = '우호성'
conscientiousness = '성실성'
extraversion = '외향성'
neuroticism = '신경성'
openness_to_experience = '경험에 대한 개방성'

STAT_TYPE = (agreeableness, conscientiousness, extraversion, neuroticism, openness_to_experience)


# Create your views here.
def yolo_model_fetcher(category):
    model_path = f'model/checkpoint_{category}.pt'
    fullpath = find_static_file(model_path)
    return YOLO(fullpath)


def update(category):
    models[category] = yolo_model_fetcher(category)


model_path = STATICFILES_DIRS
models = dict((category, yolo_model_fetcher(category)) for category in DATA_CATEGORY)
IMAGE_SIZE = 1280
image_area = IMAGE_SIZE * IMAGE_SIZE

'''
def change_score(stat, condition, value):
    if condition: stat.append(value)
    # stat.append(value if condition else default_stat)


def person_stat(boxes, labels):
    necks = BoxData(boxes, labels, '목')
    bodys = BoxData(boxes, labels, '사람전체')
    chests = BoxData(boxes, labels, '상체')
    arms = BoxData(boxes, labels, '팔')
    hands = BoxData(boxes, labels, '손')
    legs = BoxData(boxes, labels, '다리')
    eyes = BoxData(boxes, labels, '눈')
    noses = BoxData(boxes, labels, '코')
    faces = BoxData(boxes, labels, '얼굴')
    foots = BoxData(boxes, labels, '발')
    shoes = BoxData(boxes, labels, ('운동화', '남자구두', '여자구두'))

    stat = [default_stat]

    # 목을 너무 길게 그린 경우	자신의 행동조절에 대한 자신감 부족	3,3,3,8,3
    neck_h_threshold = 0.721
    chest_w_threshold = 0.872
    chest_h_threshold = 0.763
    chest_wh_small_threshold = 0.742
    chest_wh_large_threshold = 0.802
    chest_area_threshold = 0.648
    hands_area_small_threshold = 0.952
    hands_area_large_threshold = 1.168
    leg_wh_small_threshold = 1.776
    leg_wh_large_threshold = 1.855
    foot_area_small_threshold = 1.477
    foot_area_large_threshold = 1.651
    shoe_area_threshold = 2.857
    eye_area_threshold = 1.391
    nose_area_threshold = 0.730
    neck_area_threshold = 0.640
    change_score(stat, necks.h_sum > neck_h_threshold * chests.h_sum, (3, 3, 3, 8, 3))
    # 몸통을 너무 길게 그리면	지나친 행동성	5,5,7,7,6
    change_score(stat, chests.h_sum > chest_h_threshold * bodys.h_sum, (5, 5, 7, 7, 6))
    # 몸통을 너무 넓게 그리면	주변 사람들에게 요구를 많이 하거나 권위적 태도를 취함	4,6,7,6,4
    change_score(stat, chests.w_sum > chest_w_threshold * bodys.w_sum, (4, 6, 7, 6, 4))
    # 가슴을 너무 크게 그렸다면	성적능력이나 매력을 너무 강조. 의존욕구 충족에 대한 불안감을 과잉보상하고자 함	6,5,7,7,5
    change_score(stat, chests.area_sum > chest_area_threshold * bodys.area_sum, (6, 5, 7, 7, 5))
    # 팔을 크게 그리는 경우	공격적 태도를 통해 자신의 힘을 과시적으로 강조하려 함	4,6,7,6,5
    change_score(stat, arms.wh_sum > chest_wh_large_threshold * bodys.wh_sum,
                 (4, 6, 7, 6, 5))
    # 팔을 작게 그리는 경우	스스로의 대처능력이 부족. 수동적	3,3,3,8,3
    change_score(stat, arms.wh_sum < chest_wh_small_threshold * bodys.wh_sum,
                 (3, 3, 3, 8, 3))
    # 손을 그리지 않을 경우	통제감이나 효능감이 없음	2,3,2,9,2
    change_score(stat, hands.count == 0, (2, 3, 2, 9, 2))
    # 손을 너무 크게 그린 경우	과행동성이 주장성	5,6,7,7,6
    change_score(stat, hands.area_sum > hands_area_large_threshold * bodys.area_sum, (5, 6, 7, 7, 6))
    # 손을 너무 작게 그린 경우	수동성, 통제력 부족	2,3,3,9,3
    change_score(stat, hands.area_sum < hands_area_small_threshold * bodys.area_sum, (2, 3, 3, 9, 3))
    # 다리를 너무 길게 그린 경우	자율성, 독립성에 대한 욕구, 과잉행동성	7,6,7,6,7
    change_score(stat, legs.wh_sum > leg_wh_small_threshold * bodys.wh_sum, (7, 6, 7, 6, 7))
    # 다리를 너무 짧고 가늘게 그린 경우	억제 경향성, 수동적 태도	3,3,3,8,3
    change_score(stat, legs.wh_sum < leg_wh_large_threshold * bodys.wh_sum, (3, 3, 3, 8, 3))
    # 발을 그리지 않은 경우	자율성과 독립성에 대한 내적 양가감정	5,5,5,7,5
    change_score(stat, foots.count == 0, (5, 5, 5, 7, 5))
    # 발을 너무 크게 그린 경우	자신의 독립성을 지나치게 강조	7,7,7,6,7
    change_score(stat, foots.area_sum > foot_area_large_threshold * bodys.area_sum, (7, 7, 7, 6, 7))
    # 발을 너무 작게 그린 경우	자율성에 대한 두려움	4,4,3,8,3
    change_score(stat, foots.area_sum < foot_area_small_threshold * bodys.area_sum, (4, 4, 3, 8, 3))
    # 신발 크기를 크게 그리는경우	한쪽 편향과 의존성이 강함	5,4,5,7,4
    change_score(stat, shoes.area_sum > shoe_area_threshold * legs.area_sum, (5, 4, 5, 7, 4))
    # 눈 강조하는 경우, 크게 그리는 경우	현재 상태에 대한 기분	6,5,5,7,5
    change_score(stat, eyes.area_sum > eye_area_threshold * faces.area_sum, (6, 5, 5, 7, 5))
    # 코 강조하는 경우, 크게 그리는 경우	외모에 대한 강한 욕구	7,6,6,6,6
    change_score(stat, noses.area_sum > nose_area_threshold * faces.area_sum, (7, 6, 6, 6, 6))
    # 목 강조하는 경우, 크게 그리는 경우	충동적으로 하는 경향	5,4,7,7,6
    change_score(stat, necks.area_sum > neck_area_threshold * faces.area_sum, (5, 4, 7, 7, 6))

    return stat


def woman_stat(boxes, labels):
    return person_stat(boxes, labels)


def man_stat(boxes, labels):
    return person_stat(boxes, labels)


def tree_stat(boxes, labels):
    trunks = BoxData(boxes, labels, '기둥')
    roots = BoxData(boxes, labels, '뿌리')
    branchs = BoxData(boxes, labels, '가지')
    leaves = BoxData(boxes, labels, '나뭇잎')
    clouds = BoxData(boxes, labels, '구름')
    fruits = BoxData(boxes, labels, '열매')

    stat = [default_stat]

    root_area_threshold = 1.473
    leaf_wh_threshold = 2.383
    branch_area_large_threshold = 1.275
    branch_area_small_threshold = 0.620
    # 뿌리를 크게 그리는 경우	불안정 및 그에 대한 과도한 보상	4,5,6,8,4
    change_score(stat, roots.area_sum > root_area_threshold * trunks.area_sum, (4, 5, 6, 8, 4))
    # 뿌리가 없는 경우	현실에서의 불안정감	5,4,4,9,3
    change_score(stat, roots.count == 0, (5, 4, 4, 9, 3))
    # 가지가 없는 경우	대인관계에 대한 두려움, 우울증 경향	3,3,3,9,2
    change_score(stat, branchs.count == 0, (3, 3, 3, 9, 2))
    # 나무에 잎을 그리는 경우	사교성, 명량한 성격을 추구함	8,6,7,5,6
    change_score(stat, leaves.count > 0, (8, 6, 7, 5, 6))
    # 잎이 가지에 비해 큰 경우	과도한 욕구	6,6,6,7,5
    change_score(stat, leaves.wh_sum > leaf_wh_threshold * branchs.wh_sum, (6, 6, 6, 7, 5))
    # 구름과 그림자 있는 경우	불안감, 사회에 대한 두려움	2,3,3,9,2
    change_score(stat, clouds.count > 0, (2, 3, 3, 9, 2))
    # 큰 기둥에 작은 가지를 그린 경우	성취좌절, 부적절감	3,4,4,8,3
    change_score(stat, branchs.area_sum < branch_area_small_threshold * trunks.area_sum, (3, 4, 4, 8, 3))
    # 작은 기둥에 큰 가지를 그린 경우	과도한 성취성향	5,7,6,6,5
    change_score(stat, branchs.area_sum > branch_area_large_threshold * trunks.area_sum, (5, 7, 6, 6, 5))
    # 가지의 열매가 떨어진 경우	대인관계 실패, 정서적 어려움	2,3,3,9,2
    change_score(stat, fruits.ymax_ave > trunks.ymax_ave - trunks.h_sum * 0.1, (2, 3, 3, 9, 2))

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

    stat = [default_stat]

    door_area_large_threshold = 0.874
    door_area_small_threshold = 0.665
    window_count_threshold = 1.500
    roof_area_threshold = 0.685
    window_ratio_threshold = 0.951
    # 문을 크게 그린 경우	사회적 접근 가능성이 과다함. 사회적인 인정이나 수용에 의존적이거나 예민함.	6,5,8,7,4
    change_score(stat, doors.area_sum >= door_area_large_threshold * houses.area_sum, (6, 5, 8, 7, 4))
    # 문을 작게 그린 경우	사회적인 관계 자체가 적고 위축되어 있거나 대인관계능력이나 기술이 부족함.	2,3,2,8,3
    change_score(stat, doors.area_sum <= door_area_small_threshold * houses.area_sum, (2, 3, 2, 8, 3))
    # 문이 없는 경우	고독감, 외로워하는 경향	3,4,3,9,3
    change_score(stat, doors.count == 0, (3, 4, 3, 9, 3))
    # 창문을 많이 그리는 경우	타인에게 인정받고 싶고 보여주고 싶은 욕구나 소망	7,5,7,6,5
    change_score(stat, windows.count > window_count_threshold, (7, 5, 7, 6, 5))
    # 창문수가 많은 경우	타인에 대한 의존성이 강함	6,4,6,7,3
    change_score(stat, windows.count == 0, (6, 4, 6, 7, 3))
    # 창문과 문이 없는 경우	대인관계를 기피하는 경향	1,3,2,8,2
    change_score(stat, windows.count == 0 and doors.count == 0, (1, 3, 2, 8, 2))
    # 창문을 지붕에 그렸다면	내적인 고립감과 위축감	2,3,2,9,2
    change_score(stat, windows.count_of_is_inside(roofs) > window_ratio_threshold * windows.count, (2, 3, 2, 9, 2))
    # 굴뚝에 연기가 나는 경우	가정내 갈등, 애정 결핍	3,4,4,8,3
    change_score(stat, smokes.count > 0, (3, 4, 4, 8, 3))
    # 지붕을 너무 크게 그렸다면	환상과 공상에 몰두가 심하며, 대인관계 무관심	2,4,3,6,8
    change_score(stat, roofs.area_sum > roof_area_threshold * houses.area_sum, (2, 4, 3, 6, 8))
    # 해,나무,꽃,수풀 있는 경우	의존성이 강한 경향	5,4,5,7,3
    change_score(stat, suns.count + trees.count + flowers.count + grasses.count > 0, (5, 4, 5, 7, 3))
    # 길 있는 경우	대인관계 기피하는 경향	1,3,2,8,2
    change_score(stat, roads.count > 0, (1, 3, 2, 8, 2))
    # 울타리, 산 있는 경우	자기 방어 욕구가 강함	1,6,5,7,3
    change_score(stat, mountains.count > 0, (1, 6, 5, 7, 3))

    return stat

'''


def get_bounding_boxes_single_category(model: YOLO, images: List[Path]):
    result_list: List[YOLOResultType] = []
    i, batch_size = 0, 32
    while sub_images := images[i:i + batch_size]:
        result_list.extend(model.predict(sub_images))
        i += batch_size
    return list(result.boxes for result in result_list)


def get_bounding_boxes(containers: Tuple[List[Path]]):
    # containers : ([t1,t2],[m1,m2],[w1,w2],[h1,h2])
    assert (len(containers) == len(DATA_CATEGORY))
    boxes_list_categorized = []
    for category, images in zip(DATA_CATEGORY, containers):
        model: YOLO = models[category]
        if not (images and model): continue
        cboxes: List[BoundingBoxType] = get_bounding_boxes_single_category(model, images)
        boxes_list_categorized.append(cboxes)
    return tuple(boxes_list_categorized)


# def analyzer(images_list: Union[Tuple[Path], List[Tuple[Path]]]):
#     # images_list : (tree,man,woman,house) or [(t1,m1,w1,h1),(t2,m2,w2,h2)]
#     if isinstance(images_list[0], Path):
#         images_list: List[Tuple[Path]] = [images_list]
#     containers: Tuple[List[Path]] = tuple(list(r) for r in zip(*images_list))
#     boxes_list_categorized: Tuple[List[BoundingBoxType]] = get_bounding_boxes(containers)
#     total_score = FunctionEvaluator.stat_evaluater(boxes_list_categorized)
#     return total_score


def analyzer(images_list: Union[Tuple[Path], List[Tuple[Path]]]):
    # images_list : (tree,man,woman,house) or [(t1,m1,w1,h1),(t2,m2,w2,h2)]
    if isinstance(images_list[0], Path):
        images_list: List[Tuple[Path]] = [images_list]
    containers: Tuple[List[Path]] = tuple(list(r) for r in zip(*images_list))
    boxes_list_categorized: Tuple[List[BoundingBoxType]] = get_bounding_boxes(containers)
    total_score = ModelEvaluator.stat_evaluater(boxes_list_categorized)
    return total_score
