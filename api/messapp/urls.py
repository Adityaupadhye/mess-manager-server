from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('login/',views.login),
    path('', views.getUsers),
    path('post/', views.postData),
    path('weekly/', views.getWeekdata),
]