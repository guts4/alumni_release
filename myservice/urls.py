from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='kakao'),
    path('test/', views.test),
    path('kakaoLoginLogic/', views.kakaoLoginLogic),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect),
    # GET | POST - Methods / Params | QueryString
    path('methodsCheck/<int:id>', views.methodsCheck),
]