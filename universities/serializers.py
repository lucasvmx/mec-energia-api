from rest_framework import serializers

from utils.cnpj_validator_util import CnpjValidator

from .models import ConsumerUnit, University


class ConsumerUnitInRetrieveUniversitySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConsumerUnit
        fields = [
            'id', 'url', 'name', 'code', 'is_active', 'date', 'is_current_energy_bill_filled', 'pending_energy_bills_number'
        ]


class RetrieveUniversitySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    consumer_units = ConsumerUnitInRetrieveUniversitySerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = University
        fields = '__all__'

    def validate_cnpj(self, cnpj: str):
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            raise serializers.ValidationError(str(e.args))
        return cnpj


class UniversitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = University
        fields = ['url', 'id', 'name', 'acronym', 'cnpj']

    def validate_cnpj(self, cnpj: str):
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            raise serializers.ValidationError(str(e.args))
        return cnpj


class ConsumerUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConsumerUnit
        fields = ['id', 'url', 'name', 'code', 'is_active', 'date', 'university']
