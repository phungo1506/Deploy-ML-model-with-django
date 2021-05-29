import pytest
from predict import predictImage, get_output_layers
import cv2
import numpy as np

def test_predict():
    """
    Test function in class predict_Image in module predictImage of package test.
    Using image xe.jpg in folder media to test.
    If predict to success then pass test case.
    Else not pass.
    """
    classes = None
    with open('./models/yolov4.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    session = predictImage.predict_Image()
    testimage = './media/xe.png'
    image = cv2.imread(testimage)
    scale = 0.00392
    net = cv2.dnn.readNet('./models/yolov4.weights', './models/yolov4.cfg')
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers.get_output_layers(net))
    conf_threshold = 0.5
    nms_threshold = 0.4
    boxes = session.predict_object(outs, image)[0]
    confidences = session.predict_object(outs, image)[1]
    class_ids = session.predict_object(outs, image)[2]
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)  # non maximum suppression
    image = session.draw_bbox_prediction(indices, COLORS, image, classes, class_ids, boxes)
    name_img = testimage[:-4] + '_predict.jpg'
    cv2.imwrite(name_img, image)
    assert  name_img == './media/xe_predict.jpg'

