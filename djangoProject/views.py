from django.http import  HttpResponse
from django.shortcuts import render
import joblib
from sklearn.preprocessing import OneHotEncoder
#from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
import cv2
import time
import numpy as np
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request,'home.html')
def result(request):
    model = joblib.load('gia_nha.sav')
    list_test = []
    list_test.append((request.GET['toipham']))
    list_test.append((request.GET['huyhoach']))
    list_test.append((request.GET['khongdung']))
    list_test.append((request.GET['hoboi']))
    # list_test.append(int(request.GET['luong']))

    print(list_test)
    ans = model.predict([list_test])
    return render(request,'result.html',{'ans':int(ans[0])*1000})

def index(request):
    context={'a':1}
    return render(request,'index.html',context)

def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def predictImage(request):
    def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    print (request)
    print (request.POST.dict())
    fileObj=request.FILES['filePath']
    print('fileObj:',fileObj)
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    print('filePathName:',filePathName)
    filePathName=fs.url(filePathName)
    print('filePathName:',filePathName)
    testimage='.'+filePathName
    print('testimage:',testimage)


    image = cv2.imread(testimage)
    print(image.shape)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open('./models/yolov4.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet('./models/yolov4.weights', './models/yolov4.cfg')

    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    # Thực hiện xác định bằng HOG và SVM
    start = time.time()

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
    name_img = testimage[:-4] + '_predict.jpg'
    cv2.imwrite(name_img, image)
    print('name_img',name_img)
    context={'filePathName':filePathName,'name_img':name_img}
    return render(request,'index.html',context)