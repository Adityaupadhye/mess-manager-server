from rest_framework import serializers
from .models import FoodMenu, User,FoodLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User 
        fields=('name','roll_no','hostel','role')

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodLog 
        fields='__all__'

class FoodMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodMenu 
        fields = '__all__'

class FoodWastageSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodMenu
        fields=('food_category', 'food_wastage', 'date')