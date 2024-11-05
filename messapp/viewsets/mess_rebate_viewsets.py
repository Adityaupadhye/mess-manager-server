from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from messapp.models import MessRebates
from messapp.serializers import MessRebateSerializer


class MessRebateViewSet(viewsets.ModelViewSet):
    queryset = MessRebates.objects.all()
    serializer_class = MessRebateSerializer

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

