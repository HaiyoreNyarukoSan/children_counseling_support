from collections import defaultdict, Counter

from django.test import TestCase

# Create your tests here.

import views

from pathlib import Path
import json
import statistics
import pandas as pd
import pickle
from typing import List, DefaultDict, Dict, Callable, Tuple
from scipy.stats import norm
import math

from analyzer.utils import fetch_pickle, write_pickle

base_path = Path("C:/jupyter_home/data/ccs")
categories = views.DATA_CATEGORY
stats = views.STAT_TYPE
LABELS = views.LABELS
MAX_SCORE = views.MAX_SCORE
PERCENTILES = tuple((norm().ppf(i / (MAX_SCORE + 1)) * 3.31 + 5) / 10 for i in range(1, MAX_SCORE + 1))


class Box:
    def __init__(self, category: str, label: str, x: int, y: int, w: int, h: int):
        self.cls = LABELS[category].index(label)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def xyxy(self):
        return ((self.x, self.y, self.x + self.w, self.y + self.h),)

    @property
    def xywh(self):
        return ((
                    self.x + self.w // 2,
                    self.y + self.h // 2,
                    self.x + self.w,
                    self.y + self.h,
                ),)


class CategoryData:
    def __init__(self, category):
        self.category = category
        path = base_path / category
        cpl = path / "labels"
        jsons = sorted([p for p in cpl.iterdir() if p.suffix == ".json"])
        cpi = path / "images"
        images = sorted(p for p in cpi.iterdir() if p.suffix == ".jpg")
        cpb = base_path / f'{self.category}_boxes.pkl'
        # bboxes: List[views.BoundingBoxType] = fetch_pickle(cpb)
        self._jsons = jsons
        self._labels = [bboxes_from_json(file, category) for file in jsons]
        self._images = images
        # self._bboxes = bboxes

    @property
    def jsons(self):
        return self._jsons

    @property
    def images(self):
        return self._images

    @property
    def bboxes(self):
        return self._bboxes

    @property
    def labels(self):
        return self._labels


def bboxes_from_json(file: Path, category: str):
    with open(file, "r", encoding="utf-8") as f:
        l = f.read()
    data = json.loads(l)
    df = pd.DataFrame(data["annotations"]["bbox"])
    converter = lambda r: Box(category, r['label'], r['x'], r['y'], r['w'], r['h'])
    return [converter(r) for _, r in df.iterrows()]


def analyze(vs: List[float]):
    mean = statistics.mean(vs)
    stdev = statistics.stdev(vs)
    return mean, stdev


def get_percentile(vs: List[float]):
    l = len(vs)
    new_percentiles = [int(percentile * l) for percentile in PERCENTILES]
    if l < MAX_SCORE: return []
    vs = sorted(vs)
    return tuple(round((vs[percentile - 1] + vs[percentile]) / 2, 5) for percentile in new_percentiles)


def threshold(vs: List[float], tv: float):
    print(f"for v>{tv}")
    print(len([v for v in vs if v > tv]) / len(vs))


def create_or_get_category_data(category) -> CategoryData:
    pkl_path = base_path / f'{category}_data.pkl'
    if pkl_path.exists():
        cdata: CategoryData = fetch_pickle(pkl_path)
    else:
        cdata = CategoryData(category)
        write_pickle(cdata, pkl_path)
    return cdata


def get_category_bboxes_dict(n):
    cbboxes_list = dict()
    for category in categories:
        cdata = create_or_get_category_data(category)
        cbboxes_list[category] = cdata.bboxes[:n]
    return cbboxes_list


def get_category_labels_dict(n):
    labels_dict = dict()
    for category in categories:
        cdata = create_or_get_category_data(category)
        labels_dict[category] = cdata.labels[:n]
    return labels_dict


def get_category_images_dict(n):
    cimages_dict = dict()
    for category in categories:
        cdata = create_or_get_category_data(category)
        cimages_dict[category] = cdata.images[:n]
    return cimages_dict


def review(mental_stats: List[Dict[str, float]]):
    for stat in stats:
        print(stat)
        rec = [mental_stat[stat] for mental_stat in mental_stats]
        mean, std = analyze(rec)
        print(round(mean, 2), round(std, 2), min(rec), max(rec))
    return mental_stats


def create_category_datas():
    master_category_datas = [create_or_get_category_data(category) for category in categories]
    return master_category_datas


'''
n = 1024
tree, man, woman, house = '나무', '남자사람', '여자사람', '집'
cbboxes_list = get_category_bboxes_dict(n)
tree_bboxes_list = cbboxes_list[tree]
man_bboxes_list = cbboxes_list[man]
woman_bboxes_list = cbboxes_list[woman]
house_bboxes_list = cbboxes_list[house]
category = tree


def get_list(category, target):
    return [views.BoxData(bboxes, LABELS[category], target) for bboxes in cbboxes_list[category]]


def get_target_list(formula, lists):
    return [formula(*subs) for subs in zip(*lists)]


def analyze_threshold(target_count_list: List[float], sigma=0.5):
    mean, std = analyze(target_count_list)
    print(mean, std)
    percentile = get_percentile(target_count_list)
    print(percentile)
    threshold(target_count_list, mean)
    # threshold(target_count_list, mean + std * sigma)
    # threshold(target_count_list, mean - std * sigma)


class RatioFunction:
    ratio_function_type = Callable[[views.BoxData, views.BoxData], float]
    w_ratio: ratio_function_type = lambda first, second: first.w_sum / second.w_sum
    h_ratio: ratio_function_type = lambda first, second: first.h_sum / second.h_sum
    wh_ratio: ratio_function_type = lambda first, second: first.wh_sum / second.wh_sum
    wh_ratio2: ratio_function_type = lambda first, second: (first.wh_sum / second.wh_sum) if second.count else 0
    area_ratio: ratio_function_type = lambda first, second: first.area_sum / second.area_sum
    count_ratio: ratio_function_type = lambda first: first.count
    is_inside_ratio: ratio_function_type = lambda first, second: (
            first.count_of_is_inside(second) / first.count) if first.count else 0


def try_person():
    necks_list = get_list(man, '목') + get_list(woman, '목')
    hands_list = get_list(man, '손') + get_list(woman, '손')
    chests_list = get_list(man, '상체') + get_list(woman, '상체')
    bodys_list = get_list(man, '사람전체') + get_list(woman, '사람전체')
    legs_list = get_list(man, '다리') + get_list(woman, '다리')
    foots_list = get_list(man, '발') + get_list(woman, '발')
    shoes_list = get_list(man, ('운동화', '남자구두', '여자구두')) + get_list(woman, ('운동화', '남자구두', '여자구두'))
    eyes_list = get_list(man, '눈') + get_list(woman, '눈')
    noes_list = get_list(man, '코') + get_list(woman, '코')
    faces_list = get_list(man, '얼굴') + get_list(woman, '얼굴')
    neck_h_threshold = get_target_list(RatioFunction.h_ratio, [necks_list, chests_list])
    chest_w_threshold = get_target_list(RatioFunction.w_ratio, [chests_list, bodys_list])
    chest_h_threshold = get_target_list(RatioFunction.h_ratio, [chests_list, bodys_list])
    chest_area_threshold = get_target_list(RatioFunction.area_ratio, [chests_list, bodys_list])
    chest_wh_threshold = get_target_list(RatioFunction.wh_ratio, [chests_list, bodys_list])
    hand_area_threshold = get_target_list(RatioFunction.area_ratio, [hands_list, bodys_list])
    leg_wh_threshold = get_target_list(RatioFunction.wh_ratio, [legs_list, bodys_list])
    foot_area_threshold = get_target_list(RatioFunction.area_ratio, [foots_list, bodys_list])
    shoe_area_threshold = get_target_list(RatioFunction.area_ratio, [shoes_list, legs_list])
    eye_area_threshold = get_target_list(RatioFunction.area_ratio, [eyes_list, faces_list])
    nose_area_threshold = get_target_list(RatioFunction.area_ratio, [noes_list, faces_list])
    neck_area_threshold = get_target_list(RatioFunction.area_ratio, [necks_list, faces_list])
    analyze_threshold(neck_h_threshold)
    analyze_threshold(chest_w_threshold)
    analyze_threshold(chest_h_threshold)
    analyze_threshold(chest_area_threshold)
    analyze_threshold(chest_wh_threshold)
    analyze_threshold(hand_area_threshold)
    analyze_threshold(leg_wh_threshold)
    analyze_threshold(foot_area_threshold)
    analyze_threshold(shoe_area_threshold)
    analyze_threshold(eye_area_threshold)
    analyze_threshold(nose_area_threshold)
    analyze_threshold(neck_area_threshold)


def try_tree():
    roots_list = get_list(tree, '뿌리')
    trunks_list = get_list(tree, '기둥')
    leaves_list = get_list(tree, '나뭇잎')
    branchs_list = get_list(tree, '가지')
    root_area_threshold = get_target_list(RatioFunction.area_ratio, [roots_list, trunks_list])
    leaf_wh_threshold = get_target_list(RatioFunction.wh_ratio2, [leaves_list, branchs_list])
    branch_area_threshold = get_target_list(RatioFunction.area_ratio, [branchs_list, trunks_list])
    analyze_threshold(root_area_threshold)
    analyze_threshold(leaf_wh_threshold, 0.2)
    analyze_threshold(branch_area_threshold)


def try_house():
    doors_list = get_list(house, '문')
    houses_list = get_list(house, '집전체')
    windows_list = get_list(house, '창문')
    roofs_list = get_list(house, '지붕')
    door_area_threshold = get_target_list(RatioFunction.area_ratio, [doors_list, houses_list])
    window_count_threshold = get_target_list(RatioFunction.count_ratio, [windows_list])
    roof_area_threshold = get_target_list(RatioFunction.area_ratio, [roofs_list, houses_list])
    window_ratio_threshold = get_target_list(RatioFunction.is_inside_ratio, [windows_list, roofs_list])
    analyze_threshold(door_area_threshold)
    analyze_threshold(window_count_threshold)
    analyze_threshold(roof_area_threshold)
    analyze_threshold(window_ratio_threshold, 0.7)


# try_person()
# try_tree()
# try_house()
# '''
'''
n = 1024
cbboxes_dict = get_category_labels_dict(n)
cbboxes_dict = get_category_bboxes_dict(n)
containers: Tuple[List[List[Box]]] = tuple(cbboxes_dict[category] for category in categories)
mental_stats = views.stat_evaluater(containers)
for stat in stats:
    print(stat)
    rec = [mental_stat[stat] for mental_stat in mental_stats]
    mean, std = analyze(rec)
    print(round(mean, 2), round(std, 2), min(rec), max(rec))
    percentile = get_percentile(rec)
    print(percentile)

cbboxes_list = []
for category in categories:
    cbboxes_list.append(cbboxes_dict[category])
cbboxes_list = list(cbboxes for cbboxes in zip(*cbboxes_list))
mental_stats = views.stat_evaluater(cbboxes_list)
review(mental_stats)
# '''
'''
print('YOLO 결과로 계산시')
n = 1024
cbboxes_list = []
for category in categories:
    data_path = base_path
    bboxes: List[views.BoundingBoxType] = fetch_pickle(data_path / f'{category}_boxes.pkl')
    cbboxes_list.append(bboxes[:100])
mental_stats = views.stat_evaluater(cbboxes_list)
review(mental_stats)
# '''
'''
print('Label 데이터로 계산시')
n = 1024
clabels_dict = get_category_labels_dict(n)
clabels_list = []
for category in categories:
    clabels_list.append(clabels_dict[category])
clabels_list = list(images for images in zip(*clabels_list))
mental_stats = views.stat_evaluater(clabels_list)
review(mental_stats)
# '''
'''
test_path = base_path / 'test'
files = [p for p in test_path.iterdir()]
images_list = list(zip(files[:3], files[3:6], files[6:9], files[9:]))
scores_list = [views.analyzer(images) for images in images_list[:100]]

scores = [tuple(score for stat, score in zip(stats, scores)) for scores in scores_list]
for file, score in zip(files, scores):
    print(file.name)
    print(score)
# '''
'''
house_path = r'C:\jupyter_home\data\ccs\test\집_7_남_06605.jpg'
model = views.models['집']
labels = LABELS['집']
result_list = model.predict([house_path, house_path])
result = result_list[0]
print(type(result))
boxes = result.boxes
box = views.BoxData(boxes, labels, '집전체')
print(box.count)
print(list(box.xyxys))
print(list(box.whs))
print(list(wh[0] * wh[1] for wh in box.whs))
print(box.area_sum)
print(box.xmin_ave)
print(box.xmax_ave)
print(box.ymin_ave)
print(box.ymax_ave)
print(sum(wh[0] * wh[1] for wh in box.whs))
print(views.house_stat(boxes, labels))
# '''
'''
arguments: 63 types

tree_branchs.area_sum
tree_branchs.count
tree_branchs.wh_sum
tree_clouds.count
tree_fruits.ymax_ave
tree_leaves.count
tree_leaves.wh_sum
tree_roots.area_sum
tree_roots.count
tree_trunks.area_sum
tree_trunks.h_sum
tree_trunks.ymax_ave
man_arms.wh_sum
man_bodys.area_sum
man_bodys.h_sum
man_bodys.w_sum
man_bodys.wh_sum
man_chests.area_sum
man_chests.h_sum
man_chests.w_sum
man_eyes.area_sum
man_faces.area_sum
man_foots.area_sum
man_foots.count
man_hands.area_sum
man_hands.count
man_legs.area_sum
man_legs.wh_sum
man_necks.area_sum
man_noses.area_sum
man_shoes.area_sum
woman_arms.wh_sum
woman_bodys.area_sum
woman_bodys.h_sum
woman_bodys.w_sum
woman_bodys.wh_sum
woman_chests.area_sum
woman_chests.h_sum
woman_chests.w_sum
woman_eyes.area_sum
woman_faces.area_sum
woman_foots.area_sum
woman_foots.count
woman_hands.area_sum
woman_hands.count
woman_legs.area_sum
woman_legs.wh_sum
woman_necks.area_sum
woman_noses.area_sum
woman_shoes.area_sum
house_doors.area_sum
house_doors.count
house_flowers.count
house_grasses.count
house_houses.area_sum
house_mountains.count
house_roads.count
house_roofs.area_sum
house_smokes.count
house_suns.count
house_trees.count
house_windows.count
house_windows.count_of_is_inside(roofs)

stat: 5 types
agreeableness, conscientiousness, extraversion, neuroticism, openness_to_experience
'''
