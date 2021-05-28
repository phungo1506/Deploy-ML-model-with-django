from PIL import Image
import cv2
import time
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
