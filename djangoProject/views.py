from django.http import  HttpResponse
from django.shortcuts import render
import joblib
from sklearn.preprocessing import OneHotEncoder
#from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

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