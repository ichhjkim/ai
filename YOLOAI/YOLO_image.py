from pydarknet import Detector, Image
import cv2
import os

def YOLO(image):
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))

    net = Detector(bytes("cfg/yolov3_sub3", encoding="utf-8"), bytes("weights/yolov3_sub3.weights", encoding="utf-8"), 0, bytes("cfg/obj.data",encoding="utf-8"))
    print(os.path.abspath(__file__), 'yolo image 경로')
    img = cv2.imread(image)

    img2 = Image(img)

    #r = net.classify(img2)
    results = net.detect(img2,thresh=0.05)
    return results
