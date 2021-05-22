import os
import cv2
import matplotlib.pyplot as plt
import glob2


files = []
for ext in ["*.jpg"]:
    image_files = glob2.glob(os.path.join("yolomish-ciou-test", ext))
    files += image_files

label = []
for ext in ["*.txt"]:
    label_files =glob2.glob(os.path.join("yolomish-ciou-test", ext))
    label += label_files


for i in files:
    img = cv2.imread(i)
    dh, dw, _ = img.shape
    fl = open(i[:-3]+'txt', 'r')
    data = fl.read().splitlines()
    fl.close()

    for dt in data:
        v = dt.split(" ")
        
        l = int((float(v[1]) - float(v[3]) / 2) * dw)
        r = int((float(v[1]) + float(v[3]) / 2) * dw)
        t = int((float(v[2]) - float(v[4]) / 2) * dh)
        b = int((float(v[2]) + float(v[4]) / 2) * dh)
        u = int(v[0])
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1
        if u ==0:
            img = cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 3)
            img = cv2.putText(img, 'table', (l, t-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        if u ==1:
            img = cv2.rectangle(img, (l, t), (r, b), (255, 0, 0), 3) 
            img = cv2.putText(img, 'figure', (l, t-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        if u == 2:
            img = cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 3)
            img = cv2.putText(img, 'caption', (l, t-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        if u == 3:
            img = cv2.rectangle(img, (l, t), (r, b), (0, 255, 255), 3)
            img = cv2.putText(img, 'formula', (l, t-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.imwrite(str(i).replace("yolomish-ciou-test/",""),img)