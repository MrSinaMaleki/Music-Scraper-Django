from django.urls import path
from .views import index,LoginAPIView

urlpatterns = [
    path('',index, name='index'),
    path('login_api/',LoginAPIView.as_view(), name="login_api"),

]