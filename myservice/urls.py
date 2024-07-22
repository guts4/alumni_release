from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='myservice'),
    path('test/', views.test),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    path('kakaoLogout/', views.kakaoLogout, name='kakaoLogout'),
    # GET | POST - Methods / Params | QueryString
    path('methodsCheck/<int:id>', views.methodsCheck),
]