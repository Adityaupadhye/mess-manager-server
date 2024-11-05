
from rest_framework import viewsets
from messapp.models import MessRebates
from messapp.serializers import MessRebateSerializer


class MessRebateViewSet(viewsets.ModelViewSet):
    queryset = MessRebates.objects.all()
    serializer_class = MessRebateSerializer

