from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Distributor, Tariff
from .serializers import DistributorSerializer, DistributorSerializerForDocs, BlueAndGreenTariffsSerializer, BlueTariffSerializer, GreenTariffSerializer


class DistributorViewSet(ModelViewSet):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer

    def destroy(self, request, *args, **kwargs):
        distributor: Distributor = self.get_object()
        dependent_tariffs = Tariff.objects.all().filter(distributor_id=distributor.id)
        if len(dependent_tariffs) != 0:
            return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        Distributor.objects.filter(pk=distributor.id).delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={200: DistributorSerializerForDocs()})
    def list(self, request: Request, *args, **kwargs):
        # Essa parte do ID da universidade é temporária
        university_id = 1
        distributors = Distributor.objects.filter(university_id=university_id).order_by('name')
        ser = DistributorSerializer(distributors, many=True, context={'request': request})
        for dist in ser.data:
            dist['consumer_units'] = 0 # valor temporário
            tariffs = dist['tariffs']
            dist['tariffs'] = []
            for i in range(0, len(tariffs), 2):
                t = tariffs[i]
                blue = tariffs[i]
                green = tariffs[i+1]
                dist['tariffs'].append({
                    'start_date': t['start_date'],
                    'end_date': t['end_date'],
                    'overdue': t['overdue'],
                    'subgroup': t['subgroup'],
                    'distributor': t['distributor'],
                    'blue': BlueTariffSerializer(blue).data,
                    'green': GreenTariffSerializer(green).data,
                })
        
        return Response(ser.data)

class TariffViewSet(ViewSet):
    queryset = Tariff.objects.all()
    serializer_class = BlueAndGreenTariffsSerializer

    @swagger_auto_schema(request_body=BlueAndGreenTariffsSerializer)
    def create(self, request: Request):
        ser = BlueAndGreenTariffsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = ser.validated_data
        try:
            Tariff.objects.get(subgroup=data['subgroup'], distributor_id=data['distributor'])
        except Tariff.MultipleObjectsReturned:
            return Response({'error': ['There is already a tariff with given the subgroup and distributor']}, status=status.HTTP_403_FORBIDDEN)
        except Tariff.DoesNotExist:
            pass

        start_date = data['start_date']
        end_date = data['end_date']
        distributor = data['distributor']
        subgroup = data['subgroup']
        Tariff.objects.create(**data['blue'], subgroup=subgroup, flag=Tariff.BLUE, start_date=start_date, end_date=end_date, distributor=distributor)
        Tariff.objects.create(**data['green'], subgroup=subgroup, flag=Tariff.GREEN, start_date=start_date, end_date=end_date, distributor=distributor)
        return Response(ser.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=BlueAndGreenTariffsSerializer)
    def update(self, request: Request, pk=None):
        '''Essa rota de fato foge um pouco do padrão REST: ```PUT /api/tariffs/id```. 
        Nesse caso, `id` NÃO É USADO, de maneira que `id` pode ser setado para 
        qualquer coisa. Ainda assim, é possível identificar as tarifas pelo 
        _subgrupo_ e _distribuidora_.'''
        
        ser = BlueAndGreenTariffsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = ser.validated_data
        tariffs = Tariff.objects.filter(subgroup=data['subgroup'], distributor=data['distributor'])
        if 0 == tariffs.count():
            return Response({'error': [f'Could not find tariffs with '
            f'subgroup={data["subgroup"]} and distributor_id={data["distributor"].id}']}, status=status.HTTP_404_NOT_FOUND)
        assert 2 == tariffs.count()

        start_date = data['start_date']
        end_date = data['end_date']

        tariffs.filter(flag=Tariff.BLUE).update(**data['blue'], start_date=start_date, end_date=end_date)
        tariffs.filter(flag=Tariff.GREEN).update(**data['green'], start_date=start_date, end_date=end_date)

        blue_tariff = Tariff.objects.filter(subgroup=data['subgroup'], distributor=data['distributor'], flag=Tariff.BLUE).first()
        green_tariff = Tariff.objects.filter(subgroup=data['subgroup'], distributor=data['distributor'], flag=Tariff.GREEN).first()

        ser = BlueAndGreenTariffsSerializer({
            'start_date': start_date,
            'end_date': end_date,
            'distributor': data['distributor'],
            'subgroup': data['subgroup'],
            'blue': blue_tariff,
            'green': green_tariff
        })
        return Response(ser.data)
        
        