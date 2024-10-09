from rest_framework import serializers
from .models import User,FoodLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User 
        fields=('name','roll_no','hostel','role')

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodLog 
        fields=('type','roll_no','food_category','timestamp')