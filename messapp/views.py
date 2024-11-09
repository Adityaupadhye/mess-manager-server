from datetime import datetime as dt, timedelta 
from django.utils import timezone
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import User, FoodLog
from .serializers import UserSerializer, FoodLogSerializer
from rest_framework import status
from collections import defaultdict , OrderedDict
from django.db.models import Avg
from django.db.models.functions import TruncDate

@csrf_exempt 
@api_view(['POST'])
def postData(request):
    foodlogs_data = request.data.get('foodlogs')
    print(foodlogs_data)

    if not foodlogs_data:
        return Response({'error': 'Request must contain an array of foodlogs'}, status=status.HTTP_400_BAD_REQUEST)

    created_foodlogs = []

    for foodlog_entry in foodlogs_data:
        roll_no = foodlog_entry.get('roll_no')
        food_category = foodlog_entry.get('food_category')
        unix_timestamp = foodlog_entry.get('timestamp')
        type = foodlog_entry.get('type')
        print(roll_no,food_category,unix_timestamp,type)

        if not roll_no or not food_category or not unix_timestamp or not type:
            return Response({'error': 'Each foodlog entry must contain roll_no, food_category, timestamp, and type'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            timestamp = dt.fromtimestamp(unix_timestamp)
            
            foodlog = FoodLog(
                roll_no=roll_no,
                food_category=food_category,
                timestamp=timestamp,
                type=type
            )
            created_foodlogs.append(foodlog)

        except (ValueError, TypeError):
            return Response({'error': 'Invalid timestamp format in one of the entries'}, status=status.HTTP_400_BAD_REQUEST)
        
    FoodLog.objects.bulk_create(created_foodlogs)
    
    return Response({"message" : "Logs created successfully!!"}, status=status.HTTP_201_CREATED)


@csrf_exempt 
@api_view(['POST'])
def login(request):
    if not request.data.get('username') or not request.data.get('password'):
        return Response({"error":"Either password or username not provided!!"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(pk=request.data.get('username'))
            
        if user.password == request.data['password'] :
            serializer = UserSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response({'error':"Wrong Credentials!!"},status=status.HTTP_401_UNAUTHORIZED)
        
    except User.DoesNotExist:
        return Response({"error":"User doesn't exists!!"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUsers(request):
    hostel = request.query_params.get('hostel')
    role = request.query_params.get('role')
    
    if not role or not hostel:
        return Response({'error': 'Both role and hostel are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    users = User.objects.filter(role=role, hostel=hostel)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def getWeekdata(request):

    logs = FoodLog.objects.filter(timestamp__date__gte=(timezone.now() - timedelta(7)))
    serializer = FoodLogSerializer(logs,many=True) 

    data = serializer.data

    for obj in data:
        obj['timestamp'] = obj['timestamp'].split('T')[0]

    weekly_count = defaultdict(lambda: defaultdict(set))

    for entry in data:
        foodtype = entry['food_category'] 
        date = entry['timestamp']
        rollno = entry['roll_no']
        weekly_count[date][foodtype].add(rollno)

    result = {
        date: {foodtype: len(rollnos) for foodtype, rollnos in foodtypes.items()} for date, foodtypes in weekly_count.items()
    }
        
    return Response({"result"  : OrderedDict(sorted(result.items()))},status=status.HTTP_200_OK)

@api_view(['GET'])
def getDayData(request):
    date = dt.strptime(request.query_params.get('date'),'%d-%m-%Y')
    date = dt.strftime(date,'%Y-%m-%d')
    logs = FoodLog.objects.filter(timestamp__date = date)
    serializer = FoodLogSerializer(logs,many=True) 

    data = serializer.data
    
    for obj in data:
        obj['timestamp'] = obj['timestamp'].split('T')[0]

    day_count = defaultdict(set)

    for entry in data:
        foodtype = entry['food_category'] 
        rollno = entry['roll_no']
        day_count[foodtype].add(rollno)

    print(day_count)
    
    res = {
        foodtype : len(rollnos) for foodtype , rollnos in day_count.items()
    }
        
    return Response({"result"  : res},status=status.HTTP_200_OK)

@api_view(["GET"])
def getMontlyAverage(request):
    today = dt.now()
    first_day_of_this_month = today.replace(day=1)
    print(first_day_of_this_month,today)
    data = FoodLog.objects.filter(timestamp__date__range=(first_day_of_this_month, today)).annotate(date=TruncDate('timestamp')).values('date').annotate(average=Count('roll_no')/4)
    print(data)
    return Response({"data":data},status=status.HTTP_200_OK)

 


