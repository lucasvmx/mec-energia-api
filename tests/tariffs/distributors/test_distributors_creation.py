import pytest
import json
from rest_framework import status
from rest_framework.test import APIClient

from tariffs.models import Distributor

from tests.test_utils.create_objects_util import CreateObjectsUtil

ENDPOINT = '/api/distributors/'

@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.university, self.user = CreateObjectsUtil.create_university_and_user()
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_university_user['email'], 
            password = CreateObjectsUtil.login_university_user['password'])

        self.distributor_for_create = {
            'name': 'Distribuidora',
            'cnpj': '00038174000143',
            'university': self.university.id
        }

    def test_creates_distributor(self):
        response = self.client.post(ENDPOINT, self.distributor_for_create)

        created_distributor = json.loads(response.content)

        assert 'Distribuidora' == created_distributor['name']

    def test_cannot_create_distributors_with_same_cnpj(self):
        dis_1 = {'name': 'Dis 1', 'cnpj': '00038174000143', 'university': self.university}
        dis_2 = {'name': 'Dis 2', 'cnpj': '00038174000143', 'university': self.university.id}

        Distributor.objects.create(**dis_1)
        response = self.client.post(ENDPOINT, dis_2)

        assert status.HTTP_400_BAD_REQUEST == response.status_code