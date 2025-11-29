from rest_framework import serializers
from .models import FoodMenu, MessRebates, User,FoodLog,Feedback,Rating

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


class MessRebateSerializer(serializers.ModelSerializer):
    class Meta:
        model=MessRebates 
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'feedback_text', 'date']
        read_only_fields = ['id', 'date']


class RatingSerializer(serializers.ModelSerializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'timestamp']
        read_only_fields = ['id', 'timestamp']