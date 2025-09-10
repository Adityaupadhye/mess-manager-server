from rest_framework import viewsets
from messapp.models import FoodLog
from messapp.serializers import FoodLogSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware, datetime, timedelta

class FoodLogViewSet(viewsets.ModelViewSet):
    queryset = FoodLog.objects.all()
    serializer_class = FoodLogSerializer

    @action(detail=False, methods=['get'], url_path='filter')
    def fetch_by_date(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'date query parameter is required.'}, status=400)
        try:
            date_obj = parse_date(date_str)
            if date_obj is None:
                raise ValueError
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        start_dt = make_aware(datetime.combine(date_obj, datetime.min.time()))
        end_dt = start_dt + timedelta(days=1)
        logs = FoodLog.objects.filter(timestamp__gte=start_dt, timestamp__lt=end_dt)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)