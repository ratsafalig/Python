import cv2
import numpy as np
import win32gui
import win32ui
import win32
import win32con
from PIL import Image
import time
import pyautogui

def grab_screen(region=None):
    
    hwin = win32gui.GetDesktopWindow()
    # hwin = win32gui.GetForegroundWindow()
    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)


    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

def grab_foreground_screen():
    # 获取前台窗口
    hwin = win32gui.GetForegroundWindow()
    # 获取窗口尺寸
    left, top, right, bottom = win32gui.GetWindowRect(hwin)

    width = right - left
    height = bottom - top

    # !!! 更换到 desktop 句柄 !!!
    hwin = win32gui.GetDesktopWindow()

    # 根据窗口创建 device context
    hwindc = win32gui.GetWindowDC(hwin)
    # 根据 device context 创建 device context obj
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    # 根据 device context obj 创建 memory device context obj
    memdc = srcdc.CreateCompatibleDC()

    # 创建 bmp obj
    bmp = win32ui.CreateBitmap()
    # 扩展成 memory bmp
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    # 把 bmp 放进 memory device context
    memdc.SelectObject(bmp)
    # 把 device context 的 bmp 复制到 memory device context 的 bmp
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

def get_foreground_window_text():
    hwin = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwin)

# print("\n---\n")
# print(get_foreground_window_text())

# Image.fromarray(grab_foreground_screen(), 'RGB').show()

import hid

for d in hid.enumerate():
    keys = list(d.keys())
    keys.sort()
    for key in keys:
        print("%s : %s" % (key, d[key]))
    print()

