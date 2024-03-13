import statistics
import math

def classify_contour(all_contours_with_labels): # 해당 contour 가 person 인지 handrail 인지 수정
    handrail_list = []
    person_list = []

    for i in all_contours_with_labels:
        if (i["label"] == "handrail"):
            handrail_list.append(i)
        else:
            person_list.append(i)
    return handrail_list, person_list

def make_one_handrail_degree(handrail_tensor): # 난간의 기울기값과 그 기울기에 수직인 기울기 산출
    left_last_point, right_last_point = last_point_handrail(handrail_tensor)

    final_degree = (left_last_point[0] - right_last_point[0]) / (left_last_point[1] - right_last_point[1])
    reverse_degree = -1 / final_degree

    return final_degree, reverse_degree

def is_handrail_right_up(handrail_tensor): # 난간이 우상향인지 좌상향인지를 판단
    degree_list = []
    for i in range(len(handrail_tensor)-2):
        w_pre, h_pre = handrail_tensor[i][0]
        w_post, h_post = handrail_tensor[i+2][0]

        if (h_pre != h_post):
            i_degree = (w_post - w_pre)/(h_post - h_pre)
            degree_list.append(i_degree)

    final_degree = statistics.mean(degree_list)
    
    if (final_degree < 0):
        return True
    return False


def last_point_handrail(handrail_tensor): # 난간의 왼쪽 아래, 오른쪽 위 또는 왼쪽 위, 오른쪽 아래의 끝점 산출
    handrail_right_up = is_handrail_right_up(handrail_tensor)

    if (handrail_right_up): # 난간이 오른쪽 위로 상승하는 경우
        left_down_w, left_down_h, right_up_w, right_up_h = float("inf"), 0, 0, float("inf")
        for i in handrail_tensor:
            if(i[0][0] < left_down_w):
                left_down_w = i[0][0]
            if(i[0][1] > left_down_h):
                left_down_h = i[0][1]
            if(i[0][0] > right_up_w ):
                right_up_w = i[0][0]
            if(i[0][1] < right_up_h ):
                right_up_h = i[0][1]
        result = [(left_down_w, left_down_h), (right_up_w, right_up_h)]

    else: # 난간이 오른쪽 아래로 하강하는 경우
        left_up_w, left_up_h, right_down_w, right_down_h = float("inf"), float("inf"), 0, 0
        for i in handrail_tensor:
            if(i[0][0] < left_up_w):
                left_up_w = i[0][0]
            if(i[0][1] < left_up_h):
                left_up_h = i[0][1]
            if(i[0][0] > right_down_w):
                right_down_w = i[0][0]
            if(i[0][1] > right_down_h):
                right_down_h = i[0][1]
        result = [(left_up_w, left_up_h), (right_down_w, right_down_h)]

    return result

def rep_point_person(person_tensor): # 사람 Seg 의 대표값을 설정
    all_points_len = len(person_tensor)
    sum_w, max_h = 0, 0
    for i in person_tensor:
        sum_w = sum_w + i[0][0]
        if ( max_h < i[0][1]):
            max_h = i[0][1]
    result = (sum_w//all_points_len, max_h)
    return result

def calc_weight(degree, point): # 가중치(w 절편)
    weight = point[0] - degree * point[1]
    return weight

def judge_in_this_fence(handrail_tensor, person_tensor): # 해당 난간이 사람이 접근할 수 있는 난간인지를 판단, True: 난간의 주안 범위, False: 난간의 범위 밖
    result = False

    _, reverse_handrail_degree = make_one_handrail_degree(handrail_tensor)
    handrail_left_point, handrail_right_point = last_point_handrail(handrail_tensor)
    person_point = rep_point_person(person_tensor)

    weight_min = calc_weight(reverse_handrail_degree, handrail_left_point)
    weight_max = calc_weight(reverse_handrail_degree, handrail_right_point)
    weight_person = calc_weight(reverse_handrail_degree, person_point)

    if(weight_person > weight_min) and (weight_person < weight_max):
        result = True

    return result

def distance_between_handrail_person(handrail_tensor, person_tensor): # 한 난간과 사람 사이의 거리
    if not judge_in_this_fence(handrail_tensor, person_tensor):
        return float("inf")
    weight, _ = make_one_handrail_degree(handrail_tensor)
    weight_use = abs(weight)
    person_point = rep_point_person(person_tensor)

    horizontal_equal_w = weight_use * (person_point[1] - handrail_tensor[0][0][1]) + handrail_tensor[0][0][0]
    horizontal_distance = abs(person_point[0] - horizontal_equal_w)

    result = horizontal_distance * math.sqrt((5 * (weight_use ** 2) - 4 * weight_use + 4) / ( 4 * (weight_use ** 2) + 4))
    return result

def min_distance_handrail(handrail_list, person_tensor): # 거리 측정 기반 + 해당 난간 자살 가능 여부로 사람에게 유효한 가장 가까운 난간만을 정의하도록 설정
    min_dist_handrail = handrail_list[0]
    min_dist = float("inf")
    for i in handrail_list:
        if judge_in_this_fence(i["contour"], person_tensor):
            dist = distance_between_handrail_person(i["contour"], person_tensor)
            if ( dist < min_dist):
                min_dist = dist
                min_dist_handrail = i
    return min_dist_handrail

def deadline_distance_person(person_tensor): # 난간과 사람 사이의 거리의 마지노선
    max_h, min_h = 0, float("inf")

    for i in person_tensor:
        if(max_h < i[0][1]):
            max_h = i[0][1]
        if(min_h > i[0][1]):
            min_h = i[0][1]

    # 0.77
    deadline= (max_h - min_h) / 0.7765
    return deadline

def select_danger_points(all_contours_with_labels):
    handrail_list, person_list = classify_contour(all_contours_with_labels)

    danger_points=[]

    for i in person_list:
        if len(i["contour"]) != 0:    
            person_tensor = i["contour"]
            target_handrail_tensor = min_distance_handrail(handrail_list, person_tensor)["contour"]
            deadline_distance = deadline_distance_person(person_tensor)
            target_distance = distance_between_handrail_person(target_handrail_tensor, person_tensor)

            if(deadline_distance > target_distance):
                danger_point = rep_point_person(person_tensor)
                danger_points.append(danger_point)

    return danger_points
