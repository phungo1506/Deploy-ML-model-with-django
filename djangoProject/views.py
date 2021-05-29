from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
from predict import predictImage,get_output_layers

from database.models import Model_predict

def index(request):
    """
        Arg:
            request:receive request from browser
        Return:
            render request,'index.html'
    """
    return render(request,'index.html')


def predict(request):
    """
            Arg:
                request:receive request from browser
            Return:
                render request,'index.html',context
                (context:
                    filePathName is name of input image
                    name_img is name of output image
                )
    """
    classes = None
    with open('./models/yolov4.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    session = predictImage.predict_Image()
    testimage = session.get_url_img(request)
    img = testimage
    image = cv2.imread(testimage)
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    net = cv2.dnn.readNet('./models/yolov4.weights', './models/yolov4.cfg')
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers.get_output_layers(net))
    conf_threshold = 0.5
    nms_threshold = 0.4
    boxes = session.predict_object(outs,Width,Height)[0]
    confidences = session.predict_object(outs,Width,Height)[1]
    class_ids = session.predict_object(outs,Width,Height)[2]
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold) #non maximum suppression
    image = session.draw_bbox_prediction(indices,COLORS,image,classes,class_ids,boxes,confidences)
    name_img = testimage[:-4] + '_predict.jpg'
    
    cv2.imwrite(name_img, image)
    img_predict = name_img
    model = Model_predict(img=img, img_predict = img_predict)
    model.save()
    context={'filePathName':testimage[1:],'name_img':name_img}
    return render(request,'index.html',context)