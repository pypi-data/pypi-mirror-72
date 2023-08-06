from PyQt5 import QtGui
from PIL import Image
import math
import copy


def trunc(val):
    if val > 255:
        return 255
    elif val < 0:
        return 0
    return val

# debug method
def green(arr):
    im_qt = QtGui.QImage(len(arr[0]), len(arr), QtGui.QImage.Format_ARGB32)
    for x in range(0, len(arr[0])):
        for y in range(0, len(arr)):
            im_qt.setPixel(x, y, QtGui.qRgba(0, 255, 0, 255))
    return im_qt

# there is probably a 1 liner for this
def rgba2QImage(arr):
    im_qt = QtGui.QImage(len(arr[0]), len(arr), QtGui.QImage.Format_ARGB32)
    for x in range(0, len(arr[0])):
        for y in range(0, len(arr)):
            im_qt.setPixel(x, y, QtGui.qRgba(arr[y][x][0],
                                             arr[y][x][1],
                                             arr[y][x][2],
                                             arr[y][x][3]))
    return im_qt

def AdjustBrightness(arr, val):
    im_qt = QtGui.QImage(len(arr[0]), len(arr), QtGui.QImage.Format_ARGB32)

    for x in range(0, len(arr[0])):
        for y in range(0, len(arr)):
            arr[y][x] = (trunc(arr[y][x][0] + val),
                         trunc(arr[y][x][1] + val),
                         trunc(arr[y][x][2] + val),
                         arr[y][x][3])

            im_qt.setPixel(x, y, QtGui.qRgba(arr[y][x][0],
                                             arr[y][x][1],
                                             arr[y][x][2],
                                             arr[y][x][3]))

    return im_qt

def AdjustTransparency(arr, val):
    im_qt = QtGui.QImage(len(arr[0]), len(arr), QtGui.QImage.Format_ARGB32)

    for x in range(0, len(arr[0])):
        for y in range(0, len(arr)):
            arr[y][x] = (arr[y][x][0],
                         arr[y][x][1],
                         arr[y][x][2],
                         trunc(arr[y][x][3] - val))

            im_qt.setPixel(x, y, QtGui.qRgba(arr[y][x][0],
                                             arr[y][x][1],
                                             arr[y][x][2],
                                             arr[y][x][3]))

    return im_qt

def Swirl(arr):
    w = len(arr[0])
    h = len(arr)
    im_qt = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32)
    x0 = (w - 1) / 2
    y0 = (h - 1) / 2

    for x in range(0, w):
        for y in range(0, h):
            im_qt.setPixel(x, y, QtGui.qRgba(0, 0, 0, 255))

    arr2=[]
    count=-1
    for i in arr:
        arr2.append([])
        count+=1
        for j in i:
            arr2[count].append((j[0], j[1], j[2], j[3]))

    for x in range(0, w):
        for y in range(0, h):
            dx = x - x0
            dy = y - y0
            r = math.sqrt(dx * dx + dy * dy)
            angle = math.pi / 256 * r
            tx = int(dx * math.cos(angle) - dy * math.sin(angle) + x0)
            ty = int(dx * math.sin(angle) + dy * math.cos(angle) + y0)
            if (tx >= 0 and tx < w and ty >= 0 and ty < h):
                im_qt.setPixel(x, y, QtGui.qRgba(arr2[ty][tx][0],
                                                 arr2[ty][tx][1],
                                                 arr2[ty][tx][2],
                                                 arr2[ty][tx][3]))
                arr[y][x] = (arr2[ty][tx][0], arr2[ty][tx][1], arr2[ty][tx][2], arr2[ty][tx][3])
            else:
                arr[y][x] = (0, 0, 0, 255)

    return im_qt

def LRotate(arr):
    w = len(arr[0])
    h = len(arr)
    im_qt = QtGui.QImage(h, w, QtGui.QImage.Format_ARGB32)
    barr = list(zip(*arr[::-1]))
    carr = []
    for i in range(0, w):
        carr.append([])
    for y in range(0, w):
        for x in range(0, h):
            im_qt.setPixel(x, y, QtGui.qRgba(barr[w - y - 1][h - x - 1][0],
                                             barr[w - y - 1][h - x - 1][1],
                                             barr[w - y - 1][h - x - 1][2],
                                             barr[w - y - 1][h - x - 1][3]))
            carr[y].append((barr[w - y - 1][h - x - 1][0], barr[w - y - 1][h - x - 1][1],
                            barr[w - y - 1][h - x - 1][2],
                            barr[w - y - 1][h - x - 1][3]))
    return [im_qt, carr]

def RRotate(arr):
    w = len(arr[0])
    h = len(arr)
    im_qt = QtGui.QImage(h, w, QtGui.QImage.Format_ARGB32)
    barr = list(zip(*arr[::-1]))
    carr = []
    for y in range(0, w):
        carr.append([])
        for x in range(0, h):
            im_qt.setPixel(x, y, QtGui.qRgba(barr[y][x][0],
                                             barr[y][x][1],
                                             barr[y][x][2],
                                             barr[y][x][3]))
            carr[y].append((barr[y][x][0], barr[y][x][1],
                            barr[y][x][2],
                            barr[y][x][3]))

    return [im_qt, carr]

def invert_filter(arr):
    im_qt = QtGui.QImage(len(arr[0]), len(arr), QtGui.QImage.Format_ARGB32)

    for x in range(0, len(arr[0])):
        for y in range(0, len(arr)):
                arr[y][x] = (trunc(255-(arr[y][x][0])),
                             trunc(255-(arr[y][x][1])),
                             trunc(255-(arr[y][x][2])),
                             arr[y][x][3])

                im_qt.setPixel(x, y, QtGui.qRgba(arr[y][x][0],
                                                 arr[y][x][1],
                                                 arr[y][x][2],
                                                 arr[y][x][3]))

    return im_qt


def yellow_tint_filter(arr):
    im_qt = QtGui.QImage(len(arr[0]), len(arr), QtGui.QImage.Format_ARGB32)

    for x in range(0, len(arr[0])):
        for y in range(0, len(arr)):
                arr[y][x] = (trunc(25+(arr[y][x][0])),
                             trunc(25+(arr[y][x][1])),
                             trunc((arr[y][x][2])),
                             arr[y][x][3])

                im_qt.setPixel(x, y, QtGui.qRgba(arr[y][x][0],
                                                 arr[y][x][1],
                                                 arr[y][x][2],
                                                 arr[y][x][3]))

    return im_qt

def redwood_filter(arr):
    im_qt = QtGui.QImage(len(arr[0]), len(arr), QtGui.QImage.Format_ARGB32)

    for x in range(0, len(arr[0])):
        for y in range(0, len(arr)):
                arr[y][x] = (trunc(40+(arr[y][x][0])),
                             trunc(10+(arr[y][x][1])),
                             trunc((arr[y][x][2])),
                             arr[y][x][3])

                im_qt.setPixel(x, y, QtGui.qRgba(arr[y][x][0],
                                                 arr[y][x][1],
                                                 arr[y][x][2],
                                                 arr[y][x][3]))

    return im_qt
