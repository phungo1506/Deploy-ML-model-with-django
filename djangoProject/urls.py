
from django.contrib import admin
from django.urls import  path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views
urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),
    path('/',views.index,name = 'homepage'),
    # url('^$',views.index,name='homepage'),
    # path('',views.home,name='home'),
    path('result/',views.result,name='result'),
    url('^$/predictImage',views.predictImage,name='predictImage'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)