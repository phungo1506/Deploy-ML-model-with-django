import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage

class predict_Image:
    """
        perform some functions like:
            1. get the link of the image from the wed
            2. draw the bounding box
            3. perform object prediction from models
            4. draw bounding box after prediction   
        Arg:
    """

    def __init__(self):
        super().__init__()

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
        testimage='.' + filePathName
        return testimage

    def draw_bbox(self,classes,COLORS, img,class_id, bbox):
        """Args:
                classes: name of object
                COLORS: random color in (0,255)
                img: image input
                bbox: a list of x_center, y_center, Width, Height
            Return
                the image has been drawn bounding box after prediction
        """
        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 2)

        cv2.putText(img, label, (bbox[0] - 10, bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) 

    def predict_object(self,outs,image):
        """
            Arg:
                outs: Numpy ndarray as output which you can use it to plot box on the given input image.
                image: input image
            Return:
                boxes: A list containing the bboxes of the predicted object
                confidences: A list containing the object's accuracy
                class_ids: A list containing the ids to which the object belongs
        """
        class_ids = []
        confidences = []
        boxes = []
        Width = image.shape[1]
        Height = image.shape[0]
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

    def draw_bbox_prediction(self,indices,COLORS,image,classes,class_ids,boxes):
        """
            Arg:
                indices: Numpy ndarray as output which you can use it to plot box on the given input image.
                COLORS : A nparray of color codes
                image : input image
                classes: list class of object
                class_ids: A list containing the ids to which the object belongs
                boxes: A list containing the bboxes of the predicted object

            Return:
                image: the image has been drawn bounding box after prediction
        """
        for i in indices:
            i = i[0]
            box = boxes[i]
            box[0] = round(box[0])
            box[1] = round(box[1])
            box[2] = round(box[2])
            box[3] = round(box[3])
            self.draw_bbox(classes,COLORS,image, class_ids[i], box)
        return image