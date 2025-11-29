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

#for parsing the .xlsx file to JSON format
from messapp.utils.parse_menu import parse_menu_csv

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
    

    #uploading menu by .xlsx file
    @action(detail=False,methods=['post','put'])
    def uploadbulkmenu(self,request):
        print("inside bulk menu")
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Save uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            for chunk in csv_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        # Parse the Excel
        weekly_data = parse_menu_csv(tmp_path)
        # Save data into DB
        try: 
            for entry in weekly_data:
                print(entry,'\n')
                FoodMenu.objects.update_or_create(
                    date=entry['date'],
                    food_category=entry['meal_type'],
                    defaults={
                        "menu": entry['items']   # <-- FIXED
                    }
                )
            return Response({"message": "Menu uploaded successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    MEALS = ["breakfast", "lunch", "snacks", "dinner", "milk"]

    @action(detail=False, methods=['get'])
    def weekly_menu(self, request):
        """
        GET /foodmenu/weekly_menu/?start=2025-11-17
        If no start date given → choose Monday of current week
        """


        today = datetime.today().date()
        start_date = today - timedelta(days=today.weekday())  # get current Monday

        # Create an ordered week: Mon → Sun
        dates = [(start_date + timedelta(days=i)) for i in range(7)]

        # Fetching all menu items for this week
        q = FoodMenu.objects.filter(date__in=dates).order_by("date", "food_category")

        result = []
        WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        date_to_day = {}

        for i, dt in enumerate(dates):
            day = WEEKDAYS[i]
            date_to_day[dt] = day

            result.append({
                "day": day,
                "date": dt.isoformat(),
                "breakfast": [],
                "lunch": [],
                "snacks": [],
                "dinner": [],
            })

        result_map = {entry["day"]: entry for entry in result}

        for row in q:
            day_name = date_to_day[row.date]
            result_map[day_name][row.food_category] = row.menu

        return Response(result, status=200)



        
