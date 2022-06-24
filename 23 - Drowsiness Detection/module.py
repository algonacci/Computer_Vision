import math

def check_focus(list_z):
    for z in list_z:
        if (z<-0.027 or z>0.027):
            return False
    return True

def check_close_eyes(distance_left, distance_right):
    if (distance_left<0.01 or distance_right<0.01):
        return True
    return False

def euclaideanDistance(point, point1):
    x = point.x
    y = point.y
    x1 = point1.x
    y1 = point1.y
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance