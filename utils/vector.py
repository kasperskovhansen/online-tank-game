import math

def points_to_vec(point1, point2):
    return [point2[0] - point1[0], point2[1] - point1[1]]

def len_vec(vec):
    return math.sqrt(vec[0]**2+vec[1]**2)


def dot(vec, s):
    return [vec[0] * s, vec[1] * s]

def add(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]


def subtract(vec1, vec2):
    return [vec2[0] - vec1[0], vec2[1] - vec1[1]]