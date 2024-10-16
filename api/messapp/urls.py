from django.urls import include, path
from messapp.viewsets.foodmenu_viewsets import FoodMenuViewSet
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'foodmenu', FoodMenuViewSet)

urlpatterns = [
    path('login/',views.login),
    path('', views.getUsers),
    path('post/', views.postData),
    path('weekly/', views.getWeekdata),
    path('menu/', include(router.urls))
]