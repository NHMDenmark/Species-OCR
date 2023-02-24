import math
from difflib import SequenceMatcher


def most_frequent(list):
    counter = 0
    element = list[0]
     
    for i in list:
        curr_frequency = list.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            element = i
 
    return element


def word_combinations(list_of_words):
    amount = len(list_of_words)
    list_of_combinations = []
    for index1, word in enumerate(list_of_words):
        for index2 in range(amount - index1):
            combination = ' '.join(list_of_words[index1:index1+index2+1])
            list_of_combinations.append(combination)

    return list_of_combinations


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def merge_rects_by_distance(rects, threshold):
    amount_of_rects_before = 0
    amount_of_rects_after = 1
    merged_rects = rects
    while amount_of_rects_before != amount_of_rects_after:
        grouped_rects = group_rects_by_distance(merged_rects, threshold)
        amount_of_rects_before = len(merged_rects)
        merged_rects = []
        for group in grouped_rects:
            x = min([rect[0] for rect in group])
            y = min([rect[1] for rect in group])
            w = max([rect[0] + rect[2] for rect in group]) - x
            h = max([rect[1] + rect[3] for rect in group]) - y
            merged_rects.append((x, y, w, h))
        amount_of_rects_after = len(merged_rects)
    return merged_rects


def group_rects_by_distance(rects, threshold):
    grouped_rects = []
    for index, rect in enumerate(rects):
        group = set([rect])
        for other_rect in rects[index+1:]:
            distance = rect_distance(rect, other_rect)
            if distance < threshold:
                group.add(other_rect)
        
        matching_group = False
        for index, existing_group in enumerate(grouped_rects):
            if not existing_group.isdisjoint(group):
                grouped_rects[index] = existing_group.union(group)
                matching_group = True
                break
        if not matching_group:
            grouped_rects.append(group)

    return grouped_rects


def rect_distance(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    x1b = x1+w1
    y1b = y1+h1
    x2b = x2+w2
    y2b = y2+h2
    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return math.dist((x1, y1b), (x2b, y2))
    elif left and bottom:
        return math.dist((x1, y1), (x2b, y2b))
    elif bottom and right:
        return math.dist((x1b, y1), (x2, y2b))
    elif right and top:
        return math.dist((x1b, y1b), (x2, y2))
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
    else:             # rectangles intersect
        return 0.