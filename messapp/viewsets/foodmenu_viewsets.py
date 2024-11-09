from collections import defaultdict
import datetime
from rest_framework import viewsets
from messapp.models import FoodMenu
from messapp.serializers import FoodMenuSerializer, FoodWastageSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend



class FoodMenuViewSet(viewsets.ModelViewSet):
    queryset = FoodMenu.objects.all()
    serializer_class = FoodMenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'food_category']

    @action(detail=False, methods=['get'])
    def search_by_date(self, request):
        """get food menus, wastage for a particular date for each category"""

        date_param = request.query_params.get('date')

        if not date_param:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                'data': None,
                "error": "Missing date parameter."
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            search_date = datetime.strptime(date_param, '%Y-%m-%d').date()  # Expecting format YYYY-MM-DD
        except ValueError:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                'data': None,
                "error": "Invalid date format. Expected format: YYYY-MM-DD."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter the queryset based on the parsed date
        datewise_food_menu = self.queryset.filter(date=search_date)

        if not datewise_food_menu.exists():
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": "No food menus found for this date.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        # Serialize the filtered queryset
        serializer = self.get_serializer(datewise_food_menu, many=True)
        
        # Return the response with status code and data
        return Response({
            "status_code": status.HTTP_200_OK,
            "data": serializer.data,
            "error": None  
        }, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'])
    def get_weekly(self, request):

        today = timezone.now()
        last_seven_days_delta = today - timedelta(days=7)

        last_seven_days_data = FoodMenu.objects.filter(date__range=(last_seven_days_delta, today))

        if not last_seven_days_data.exists():

            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": "No food menus found in the last 7 days.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Group data by date
        grouped_data = defaultdict(list)
        for entry in last_seven_days_data:

            date_str = str(entry.date)
            grouped_data[date_str].append({
                'food_wastage': entry.food_wastage,
                'food_category': entry.food_category
            })

        # Sort the grouped data by date
        sorted_grouped_data = dict(sorted(grouped_data.items()))

        # Serialize the filtered queryset
        wastage_serializer = FoodWastageSerializer(last_seven_days_data, many=True)
        # serializer = self.get_serializer(last_seven_days_data, many=True)


        return Response({
            "status_code": status.HTTP_200_OK,
            "data": sorted_grouped_data,
            "error": None 
        }, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['GET'], url_path='monthly_avg_food_wastage')
    def get_monthly_avg_food_wastage(self, request):

        today = timezone.now()
        start_of_month = today.replace(day=1)

        # get current month data
        current_month_data = FoodMenu.objects.filter(date__gte=start_of_month)

        # Annotate and calculate average food wastage per day
        averages = (
            current_month_data
            .values('date')  # Group by date
            .annotate(avg_wastage=Avg('food_wastage'))  # Calculate average food_wastage
            .order_by('date')  # Order by date
        )

        return Response({
            "status_code": status.HTTP_200_OK,
            "data": averages,
            "error": None
        }, status=status.HTTP_200_OK)
    
