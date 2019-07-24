from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^index', views.IndexPage, name='indexPage'),
    url(r'^v1/upload$', views.uploadpdf, name='parser'),
    url(r'^v1/getdata$', views.fetchdata, name='fetch'),

]
