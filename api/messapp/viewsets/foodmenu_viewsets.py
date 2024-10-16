from rest_framework import viewsets
from messapp.models import FoodMenu
from messapp.serializers import FoodMenuSerializer


class FoodMenuViewSet(viewsets.ModelViewSet):
    queryset = FoodMenu.objects.all()
    serializer_class = FoodMenuSerializer