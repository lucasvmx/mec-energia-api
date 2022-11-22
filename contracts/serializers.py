from rest_framework import serializers
from . import models

class ContractSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    subgroup = serializers.CharField(read_only=True)
    
    class Meta:
        model = models.Contract
        fields = '__all__'

class EnergyBillSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.EnergyBill
        fields = '__all__'