from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from messapp.models import MessRebates
from messapp.serializers import MessRebateSerializer
from django_filters.rest_framework import DjangoFilterBackend


class MessRebateViewSet(viewsets.ModelViewSet):
    queryset = MessRebates.objects.all()
    serializer_class = MessRebateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['start_date', 'end_date', 'status', 'hostel', 'roll_no']

    def create(self, request, *args, **kwargs):
        try:
            roll_no = request.data.get("roll_no")
            status_pending = "pending"

            # Check if a rebate with the same roll_no and status 'pending' already exists
            if MessRebates.objects.filter(roll_no=roll_no, status=status_pending).exists():
                return Response({
                    "error": f'A pending rebate already exists for roll number {roll_no}.',
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                    "error": "Please try again later",
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Call the default `create` implementation if the custom check passes
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='past_rebates')
    def search_past_rebates(self, request):
        # Retrieve query parameters from the URL
        hostel = request.query_params.get('hostel')
        roll_no = request.query_params.get('roll_no')

        if not hostel or not roll_no:
            return Response({
                'error': 'Hostel and Roll no. are required',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter for expired records that match the provided hostel and roll_no
        queryset = MessRebates.objects.filter(hostel=hostel, roll_no=roll_no, status="expired")

        # Serialize the filtered data
        serializer = self.get_serializer(queryset, many=True)

        # Return the serialized data
        return Response({
            'error': '',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

