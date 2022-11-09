from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ConsumerUnit, University
from .serializers import ConsumerUnitSerializer, UniversitySerializer, RetrieveUniversitySerializer, ConsumerUnitInRetrieveUniversitySerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveUniversitySerializer
        return UniversitySerializer

    @action(detail=True, methods=['post'])
    def create_consumer_unit_and_contract(self, request, pk=None):
        obj = self.get_object()
        data = request.data

        if not data.get("consumer_unit"):
            raise Exception("Is necessary the data for create Consumer Unit")

        if not data.get("contract"):
            raise Exception("Is necessary the data for create Contract")

        try:
            obj.create_consumer_unit_and_contract(data['consumer_unit'], data['contract'])
            
            return Response({'Consumer Unit and Contract created'})
        except Exception as error:
            raise Exception(str(error))


class ConsumerUnitViewSet(viewsets.ModelViewSet):
    queryset = ConsumerUnit.objects.all()
    serializer_class = ConsumerUnitSerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConsumerUnitInRetrieveUniversitySerializer
        return ConsumerUnitSerializer