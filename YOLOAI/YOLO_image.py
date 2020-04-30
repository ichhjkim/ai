from pydarknet import Detector, Image
import cv2
import os

def YOLO(image):
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8"))

    img = cv2.imread(image)

    # img2 = Image(img)

    # r = net.classify(img2)
    results = net.detect(img)
    return results