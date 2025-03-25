from django.urls import include, path
from messapp.viewsets.foodmenu_viewsets import FoodMenuViewSet
from messapp.viewsets.mess_rebate_viewsets import MessRebateViewSet
from messapp.viewsets.user_viewsets import UserViewSet
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'foodmenu', FoodMenuViewSet)
router.register(r'rebates', MessRebateViewSet)

urlpatterns = [
    path("signup/", views.create_user,),
    path('login/',views.login),
    path('', views.getUsers),
    path('post/', views.postData),
    path('weekly/', views.getWeekdata),
    path('monthly/', views.getMontlyAverage),
    path('pie/', views.getDayData),
    path('menu/', include(router.urls)),
    path('', include(router.urls))
]