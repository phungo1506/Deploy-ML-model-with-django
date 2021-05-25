from django.db import  models

class Model_predict(models.Model):
    img = models.CharField(max_length=100000000000)
    img_predict = models.CharField(max_length=100000000000)