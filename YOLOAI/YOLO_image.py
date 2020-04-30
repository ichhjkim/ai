from pydarknet import Detector, Image
import cv2
import os

def YOLO(image):
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))
    print(os.path.abspath(__file__), 'yolo image 경로')
    print(os.path.join("cfg/yolov3_sub3"))
    net = Detector(bytes(os.path.join("cfg/yolov3_sub3.cfg"), encoding="utf-8"), bytes(os.path.join("weights/yolov3_sub3.weights"), encoding="utf-8"), 0, bytes(os.path.join("cfg/obj.data"),encoding="utf-8"))
    img = cv2.imread(image)

    img2 = Image(img)

    #r = net.classify(img2)
    results = net.detect(img2,thresh=0.05)
    return results
