# -*- coding: utf-8 -*-
"""
    王者荣耀自动刷经验
    先给自己的电脑装上adb,确保adb能够正常运行,用你已知的手段把手机连上adb(不会就百度).
    将下面的"Path"变量修改成你自己的路径  你电脑里的“sgb_wzry_sjy”文件夹绝对路径
    (路径不能有中文),否则会炸. 
    本文件的第82行：os.system("adb shell input swipe 1000 500 1000 510 8000")
                                                                        ↑
    这个是进入关卡时的加载时间，一般情况下,21世纪产的手机加载时间不会超过八秒
    超了当我没说，自行修改这个数值，单位毫秒
    author: Sugobet
    Time: 2020/8/15
    QQ:321355478
    Github: https://github.com/Sugobet/wzry_sjy
    有问题联系我
"""
import os
import cv2

Path = "D:/sugo_python/sgb_wzry_sjy"

Cache = "sgb_wzry_cache/test.png"
MyResImgPath = f"{Path}/ResourcesImage"

PassImage = f"{Path}/TemplateImage/pass.png"
StartImage = f"{Path}/TemplateImage/start.png"
ReStartImage = f"{Path}/TemplateImage/restart.png"


def InTGame():
    # 跳过剧情
    GetImage()
    i1, i2 = LoadImage(MyResImgPath+"/test.png", PassImage)
    x, y = Img_I(i1, i2)
    print("跳过剧情")
    os.system(f"adb shell input tap {x} {y}")
    # 人物自动行走
    print("自动跑路")
    os.system("adb shell input swipe 307 776 156 510 26500")
    # 启用自动攻击
    print("自动攻击")
    os.system("adb shell input tap 2121 57")
    # 跳过剧情
    i = 0
    while True:
        os.system(f"adb shell input tap 1000 500")
        os.system(f"adb shell input tap 1000 500")
        os.system(f"adb shell input tap 1000 500")
        os.system(f"adb shell input tap 1000 500")
        if i == 7:
            break
        i += 1
    # 再次挑战
    GetImage()
    i1, i2 = LoadImage(MyResImgPath+"/test.png", ReStartImage)
    x, y = Img_I(i1, i2)
    print("再次挑战")
    os.system(f"adb shell input tap {x} {y}")
    # 开始闯关
    GetImage()
    i1, i2 = LoadImage(MyResImgPath+"/test.png", StartImage)
    x, y = Img_I(i1, i2)
    print("开始闯关")
    os.system(f"adb shell input tap {x} {y}")


def GetImage():
    os.system(f"adb shell screencap -p /sdcard/{Cache}")
    os.system(f"adb pull /sdcard/{Cache} {MyResImgPath}")


def LoadImage(img1, img2):
    i1 = cv2.imread(img1)
    i2 = cv2.imread(img2)
    return i1, i2


def Img_I(src, mp):
    w, h = mp.shape[::2]
    res = cv2.matchTemplate(src,mp,cv2.TM_CCOEFF)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    bottom_right = (max_loc[0] + w, max_loc[1] + h)
    x = (max_loc[0] + bottom_right[0])/2
    y = (max_loc[1] + bottom_right[1])/2
    return (x, y, )


if __name__ == "__main__":
    while True:
        InTGame()
        os.system("adb shell input swipe 1000 500 1000 510 8000")
