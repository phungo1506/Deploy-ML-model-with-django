from PIL import Image
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from . import get_output_layers

class predict_Image:
    
    def __init__(self):
        super().__init__()

    def draw_prediction(self,classes,COLORS, img,class_id, confidence, x, y, x_plus_w, y_plus_h):
        """Args:
                classes: name of object
                COLORS: random color in (0,255)
                img: image input
                confidence: accuracy predict
                x: x center
                y: y center
                x_plus_w: x + width
                y_plus_h: y + height
            Return
                the image has been drawn bounding box after prediction
        """
        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    def get_url_img(self,request):
        """
            Arg:
                request:receive request from browser
            Return:
                link of input image use preidct
        """
        fileObj=request.FILES['filePath']
        fs=FileSystemStorage()
        filePathName=fs.save(fileObj.name,fileObj)
        filePathName=fs.url(filePathName)
        testimage='.'+filePathName
        return testimage
    def predict_object(self,outs,Width,Height):
        """
            Arg:
                outs: Numpy ndarray as output which you can use it to plot box on the given input image.
                Width : Width of image
                Height : Height of image
            Return:
                boxes: A list containing the bboxes of the predicted object
                confidences: A list containing the object's accuracy
                class_ids: A list containing the ids to which the object belongs
        """
        class_ids = []
        confidences = []
        boxes = []
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
        return boxes,confidences,class_ids
    def draw_bbox_prediction(self,indices,COLORS,image,classes,class_ids,boxes,confidences):
        """
            Arg:
                indices: Numpy ndarray as output which you can use it to plot box on the given input image.
                COLORS : A nparray of color codes
                image : input image
                classes: list class of object
                class_ids: A list containing the ids to which the object belongs
                boxes: A list containing the bboxes of the predicted object
                confidences: A list containing the object's accuracy
            Return:
                image: the image has been drawn bounding box after prediction
        """
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            self.draw_prediction(classes,COLORS,image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
        return image