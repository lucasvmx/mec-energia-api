from rest_framework import serializers
from . import models
from users.models import CustomUser

class LoggerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Logger
        fields = ['id', 'operation', 'time_stamp', 'user', 'item_type', 'id_item_type']