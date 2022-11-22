from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import JsonResponse

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

        if not data.get("consumer_unit") or not data.get("contract"):
            raise Exception("Is necessary the data for create Consumer Unit and/or Contract")

        try:
            obj.create_consumer_unit_and_contract(data['consumer_unit'], data['contract'])
            
            return Response({'Consumer Unit and Contract created'})
        except Exception as error:
            raise Exception(str(error))


class ConsumerUnitViewSet(viewsets.ModelViewSet):
    queryset = ConsumerUnit.objects.all()
    serializer_class = ConsumerUnitSerializer
    http_method_names = ['get', 'post', 'put']

    @action(detail=True, methods=['get'], url_path='energy-bills-list')
    def list_energy_bills(self, request: Request, pk=None):
        consumer_unit = self.get_object()
        year = request.GET.get('year')

        if year:
            energy_bills = consumer_unit.get_energy_bills_by_year(int(year))
        else:
            energy_bills = consumer_unit.get_energy_bills_pending()

        return JsonResponse(energy_bills, safe=False)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConsumerUnitInRetrieveUniversitySerializer
        return ConsumerUnitSerializer