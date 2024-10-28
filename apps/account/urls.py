from django.urls import path
from .views import index, LoginAPIView, RegisterAPIView

urlpatterns = [
    path('',index, name='index'),
    path('login_api/',LoginAPIView.as_view(), name="login_api"),
    path('register_api/',RegisterAPIView.as_view(), name="register_api"),

]